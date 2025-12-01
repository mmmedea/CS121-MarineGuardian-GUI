import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
import sqlite3
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ==========================================
# MODULE 1: DATABASE MANAGEMENT (Backend)
# Requirement: Data Handling & Database Integration 
# ==========================================
class MarineDatabase:
    def __init__(self, db_file="marine_life.db"): # Renamed back to marine_life.db
        self.db_file = db_file
        self.create_table()

    def connect(self):
        """Establish connection to the SQLite database."""
        try:
            conn = sqlite3.connect(self.db_file)
            return conn
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Connection failed: {e}")
            return None

    def create_table(self):
        """Initialize the database table."""
        conn = self.connect()
        if conn:
            cursor = conn.cursor()
            # Requirement: CRUD - The structure allows Creating and Reading data 
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS species (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    common_name TEXT NOT NULL,
                    scientific_name TEXT,
                    conservation_status TEXT,
                    location_sighted TEXT,
                    date_recorded TEXT
                )
            """)
            conn.commit()
            conn.close()

    def insert_species(self, common, scientific, status, location):
        """CREATE: Add a new record """
        conn = self.connect()
        current_date = datetime.datetime.now().strftime("%Y-%m-%d") # Auto-generate date
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO species VALUES (NULL, ?, ?, ?, ?, ?)", 
                               (common, scientific, status, location, current_date))
                conn.commit()
                return True
            except sqlite3.Error as e:
                # Requirement: Error Handling 
                messagebox.showerror("Error", f"Could not add record: {e}")
                return False
            finally:
                conn.close()

    def fetch_all(self, sort_by="id"):
        """READ: Retrieve data with sorting options """
        conn = self.connect()
        if conn:
            cursor = conn.cursor()
            if sort_by == "name":
                cursor.execute("SELECT * FROM species ORDER BY common_name ASC")
            elif sort_by == "date":
                cursor.execute("SELECT * FROM species ORDER BY date_recorded DESC")
            else:
                cursor.execute("SELECT * FROM species ORDER BY id DESC")
            rows = cursor.fetchall()
            conn.close()
            return rows
        return []

    def get_status_counts(self):
        """Analytics: Data for the graph."""
        conn = self.connect()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT conservation_status, COUNT(*) FROM species GROUP BY conservation_status")
            data = cursor.fetchall()
            conn.close()
            return dict(data)
        return {}

    def update_species(self, id, common, scientific, status, location):
        """UPDATE: Modify existing record """
        conn = self.connect()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE species SET 
                    common_name=?, scientific_name=?, conservation_status=?, location_sighted=? 
                    WHERE id=?
                """, (common, scientific, status, location, id))
                conn.commit()
                return True
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Update failed: {e}")
                return False
            finally:
                conn.close()

    def delete_species(self, id):
        """DELETE: Remove record """
        conn = self.connect()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM species WHERE id=?", (id,))
                conn.commit()
                return True
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Delete failed: {e}")
                return False
            finally:
                conn.close()

# ==========================================
# MODULE 2: GRAPHICAL USER INTERFACE (Frontend)
# Requirement: GUI  & Modular Code 
# ==========================================
class MarineGUI:
    def __init__(self, root):
        self.db = MarineDatabase()
        self.root = root
        self.root.title("MarineGuardian | Biodiversity Tracker")
        self.root.geometry("1100x750")
        
        # Modern Dark Theme Colors
        self.colors = {
            "bg": "#1e1e2e", "panel": "#252537", "accent": "#00aaff",
            "text": "#ffffff", "subtext": "#a0a0a0", "danger": "#ff4444", "success": "#00cc66"
        }
        self.root.configure(bg=self.colors["bg"])
        self.selected_id = None 

        self.create_header()

        # Main Layout Container
        self.main_container = tk.Frame(self.root, bg=self.colors["bg"])
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Left Panel (Inputs) - Wider for better usability
        self.left_panel = tk.Frame(self.main_container, bg=self.colors["panel"], width=380)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        self.left_panel.pack_propagate(False) 
        
        self.setup_input_form()

        # Right Panel (Treeview)
        self.right_panel = tk.Frame(self.main_container, bg=self.colors["bg"])
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.setup_treeview()
        self.populate_table()

    def create_header(self):
        """Displays SDG Integration """
        header_frame = tk.Frame(self.root, bg=self.colors["bg"], pady=10)
        header_frame.pack(fill=tk.X, padx=20)
        title = tk.Label(header_frame, text="MARINE GUARDIAN", font=("Segoe UI", 24, "bold"), bg=self.colors["bg"], fg=self.colors["accent"])
        title.pack(anchor="w")
        
        # SDG Requirement: Clearly reflect how the project contributes to the goal
        subtitle = tk.Label(header_frame, text="SDG 14: Life Below Water - Digital Logbook", font=("Segoe UI", 12), bg=self.colors["bg"], fg=self.colors["subtext"])
        subtitle.pack(anchor="w")
        tk.Frame(self.root, bg=self.colors["accent"], height=2).pack(fill=tk.X, padx=20)

    def setup_input_form(self):
        form_container = tk.Frame(self.left_panel, bg=self.colors["panel"], padx=25, pady=25)
        form_container.pack(fill=tk.BOTH, expand=True)

        tk.Label(form_container, text="NEW SIGHTING", font=("Segoe UI", 16, "bold"), bg=self.colors["panel"], fg=self.colors["text"]).pack(anchor="w", pady=(0, 25))

        self.common_name_var = tk.StringVar()
        self.sci_name_var = tk.StringVar()
        self.status_var = tk.StringVar()
        self.location_var = tk.StringVar()

        self.create_modern_entry(form_container, "Common Name", self.common_name_var)
        self.create_modern_entry(form_container, "Scientific Name", self.sci_name_var)
        self.create_modern_entry(form_container, "Location Sighted", self.location_var)
        
        tk.Label(form_container, text="Conservation Status", font=("Segoe UI", 11), bg=self.colors["panel"], fg=self.colors["subtext"]).pack(anchor="w")
        self.status_combo = ttk.Combobox(form_container, textvariable=self.status_var, font=("Segoe UI", 11),
                                         values=["Least Concern", "Vulnerable", "Endangered", "Critically Endangered"])
        self.status_combo.pack(fill=tk.X, pady=(5, 25))

        self.create_flat_button(form_container, "Add Record", self.add_record, self.colors["success"])
        self.create_flat_button(form_container, "Update Record", self.update_record, self.colors["accent"])
        self.create_flat_button(form_container, "Delete Record", self.delete_record, self.colors["danger"])
        self.create_flat_button(form_container, "Clear Form", self.clear_inputs, "#555555")

        tk.Frame(form_container, height=20, bg=self.colors["panel"]).pack() 
        self.create_flat_button(form_container, "📊 View Status Graph", self.show_graph, "#9b59b6")

    def setup_treeview(self):
        toolbar = tk.Frame(self.right_panel, bg=self.colors["bg"])
        toolbar.pack(fill=tk.X, pady=(0, 10))
        tk.Label(toolbar, text="SIGHTING HISTORY", font=("Segoe UI", 12, "bold"), bg=self.colors["bg"], fg="white").pack(side=tk.LEFT)
        
        btn_frame = tk.Frame(toolbar, bg=self.colors["bg"])
        btn_frame.pack(side=tk.RIGHT)
        tk.Button(btn_frame, text="📅 Sort Date", command=lambda: self.populate_table("date"), bg=self.colors["panel"], fg="white", relief="flat", padx=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="⬇ Sort Name", command=lambda: self.populate_table("name"), bg=self.colors["panel"], fg="white", relief="flat", padx=10).pack(side=tk.LEFT)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=self.colors["panel"], foreground="white", fieldbackground=self.colors["panel"], rowheight=30, borderwidth=0)
        style.map("Treeview", background=[('selected', self.colors["accent"])])
        style.configure("Treeview.Heading", background="#333344", foreground="white", font=("Segoe UI", 10, "bold"), relief="flat")

        columns = ("ID", "Common Name", "Scientific Name", "Status", "Location", "Date")
        self.tree = ttk.Treeview(self.right_panel, columns=columns, show="headings", selectmode="browse")
        
        widths = [40, 140, 140, 110, 140, 90]
        for col, w in zip(columns, widths):
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, width=w)

        scrollbar = tk.Scrollbar(self.right_panel, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.bind('<<TreeviewSelect>>', self.select_item)

    def show_graph(self):
        """Displays a Matplotlib bar chart sorted by conservation severity."""
        data = self.db.get_status_counts()
        order = ["Least Concern", "Vulnerable", "Endangered", "Critically Endangered"]
        counts = [data.get(status, 0) for status in order]
        
        graph_window = Toplevel(self.root)
        graph_window.title("Conservation Status Analysis")
        graph_window.geometry("600x450")
        
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        colors = ['#2ecc71', '#f1c40f', '#e67e22', '#e74c3c'] 
        bars = ax.bar(order, counts, color=colors)
        
        ax.set_title("Species Count by Conservation Status", fontsize=12, fontweight='bold')
        ax.set_ylabel("Number of Species")
        plt.xticks(rotation=15)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height, f'{int(height)}', ha='center', va='bottom')

        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_modern_entry(self, parent, label_text, variable):
        tk.Label(parent, text=label_text, font=("Segoe UI", 11), bg=self.colors["panel"], fg=self.colors["subtext"]).pack(anchor="w")
        entry = tk.Entry(parent, textvariable=variable, bg="#333344", fg="white", relief="flat", insertbackground="white", font=("Segoe UI", 11))
        entry.pack(fill=tk.X, pady=(5, 20), ipady=6)

    def create_flat_button(self, parent, text, command, color):
        tk.Button(parent, text=text, command=command, bg=color, fg="white", font=("Segoe UI", 10, "bold"), relief="flat", activebackground=color).pack(fill=tk.X, pady=6, ipady=5)

    def populate_table(self, sort_by="id"):
        for row in self.tree.get_children():
            self.tree.delete(row)
        rows = self.db.fetch_all(sort_by)
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def add_record(self):
        # Requirement: Error Handling for user inputs 
        if not self.common_name_var.get() or not self.location_var.get():
            messagebox.showwarning("Input Error", "Common Name and Location are required!")
            return
        if self.db.insert_species(self.common_name_var.get(), self.sci_name_var.get(), self.status_var.get(), self.location_var.get()):
            messagebox.showinfo("Success", "Sighting recorded successfully!")
            self.clear_inputs()
            self.populate_table()

    def select_item(self, event):
        try:
            row_values = self.tree.item(self.tree.selection()[0], 'values')
            self.selected_id = row_values[0]
            self.common_name_var.set(row_values[1])
            self.sci_name_var.set(row_values[2])
            self.status_var.set(row_values[3])
            self.location_var.set(row_values[4])
        except IndexError: pass

    def update_record(self):
        if self.selected_id and self.db.update_species(self.selected_id, self.common_name_var.get(), self.sci_name_var.get(), self.status_var.get(), self.location_var.get()):
            messagebox.showinfo("Success", "Record updated.")
            self.clear_inputs()
            self.populate_table()

    def delete_record(self):
        if self.selected_id and messagebox.askyesno("Confirm", "Delete this record?"):
            if self.db.delete_species(self.selected_id):
                messagebox.showinfo("Deleted", "Record removed.")
                self.clear_inputs()
                self.populate_table()

    def clear_inputs(self):
        self.common_name_var.set(""); self.sci_name_var.set(""); self.status_var.set(""); self.location_var.set(""); self.selected_id = None; self.tree.selection_remove(self.tree.selection())

if __name__ == "__main__":
    root = tk.Tk()
    app = MarineGUI(root)
    root.mainloop()