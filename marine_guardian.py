import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class MarineDatabase:
    def __init__(self, db_file="marine_life.db"):
        self.db_file = db_file
        self.conn = None
        self.create_table()

    def connect(self):
        """Establish connection to the SQLite database."""
        try:
            self.conn = sqlite3.connect(self.db_file)
            return self.conn
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Connection failed: {e}")
            return None

    def create_table(self):
        """Initialize the database table if it doesn't exist."""
        conn = self.connect()
        if conn:
            cursor = conn.cursor()
            # Creating a table to store species data
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS species (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    common_name TEXT NOT NULL,
                    scientific_name TEXT,
                    conservation_status TEXT,
                    location_sighted TEXT
                )
            """)
            conn.commit()
            conn.close()

    def insert_species(self, common, scientific, status, location):
        """CREATE: Add a new record to the database."""
        conn = self.connect()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO species VALUES (NULL, ?, ?, ?, ?)", 
                               (common, scientific, status, location))
                conn.commit()
                return True
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Could not add record: {e}")
                return False
            finally:
                conn.close()

    def fetch_all(self):
        """READ: Retrieve all records from the database."""
        conn = self.connect()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM species")
            rows = cursor.fetchall()
            conn.close()
            return rows
        return []

    def update_species(self, id, common, scientific, status, location):
        """UPDATE: Modify an existing record."""
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
                messagebox.showerror("Error", f"Could not update record: {e}")
                return False
            finally:
                conn.close()

    def delete_species(self, id):
        """DELETE: Remove a record from the database."""
        conn = self.connect()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM species WHERE id=?", (id,))
                conn.commit()
                return True
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Could not delete record: {e}")
                return False
            finally:
                conn.close()

class MarineGUI:
    def __init__(self, root):
        self.db = MarineDatabase()
        self.root = root
        self.root.title("MarineGuardian: Biodiversity Tracker")
        self.root.geometry("800x600")
        
        self.header_frame = tk.Frame(self.root, bg="#006994", pady=10)
        self.header_frame.pack(fill=tk.X)
        
        self.title_label = tk.Label(
            self.header_frame, 
            text="MarineGuardian - Supporting SDG 14: Life Below Water", 
            font=("Helvetica", 16, "bold"), 
            bg="#006994", 
            fg="white"
        )
        self.title_label.pack()

        self.input_frame = tk.LabelFrame(self.root, text="Manage Species Records", padx=10, pady=10)
        self.input_frame.pack(fill=tk.X, padx=20, pady=10)

        self.common_name_var = tk.StringVar()
        self.sci_name_var = tk.StringVar()
        self.status_var = tk.StringVar()
        self.location_var = tk.StringVar()
        self.selected_id = None 

        tk.Label(self.input_frame, text="Common Name:").grid(row=0, column=0, sticky=tk.W)
        tk.Entry(self.input_frame, textvariable=self.common_name_var, width=30).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.input_frame, text="Scientific Name:").grid(row=0, column=2, sticky=tk.W)
        tk.Entry(self.input_frame, textvariable=self.sci_name_var, width=30).grid(row=0, column=3, padx=5, pady=5)

        tk.Label(self.input_frame, text="Conservation Status:").grid(row=1, column=0, sticky=tk.W)
        self.status_combo = ttk.Combobox(self.input_frame, textvariable=self.status_var, width=27, 
                                         values=["Least Concern", "Vulnerable", "Endangered", "Critically Endangered"])
        self.status_combo.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.input_frame, text="Location Sighted:").grid(row=1, column=2, sticky=tk.W)
        tk.Entry(self.input_frame, textvariable=self.location_var, width=30).grid(row=1, column=3, padx=5, pady=5)

        self.btn_frame = tk.Frame(self.input_frame)
        self.btn_frame.grid(row=2, column=0, columnspan=4, pady=10)

        tk.Button(self.btn_frame, text="Add Record", command=self.add_record, bg="#4CAF50", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(self.btn_frame, text="Update Selected", command=self.update_record, bg="#2196F3", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(self.btn_frame, text="Delete Selected", command=self.delete_record, bg="#f44336", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(self.btn_frame, text="Clear Form", command=self.clear_inputs, width=12).pack(side=tk.LEFT, padx=5)

        self.tree_frame = tk.Frame(self.root)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.scrollbar = tk.Scrollbar(self.tree_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        columns = ("ID", "Common Name", "Scientific Name", "Status", "Location")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings", yscrollcommand=self.scrollbar.set)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        self.tree.column("ID", width=30)

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.tree.yview)

        self.tree.bind('<<TreeviewSelect>>', self.select_item)

        self.populate_table()
    
    def populate_table(self):
        """Clear table and reload all data from database."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        rows = self.db.fetch_all()
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def add_record(self):
        """Validate input and add new record."""
        if not self.common_name_var.get() or not self.location_var.get():
            messagebox.showwarning("Input Error", "Common Name and Location are required!")
            return

        success = self.db.insert_species(
            self.common_name_var.get(),
            self.sci_name_var.get(),
            self.status_var.get(),
            self.location_var.get()
        )
        if success:
            messagebox.showinfo("Success", "Species record added successfully.")
            self.clear_inputs()
            self.populate_table()

    def select_item(self, event):
        """Populate input fields when a row is clicked."""
        try:
            selected_row = self.tree.selection()[0]
            row_values = self.tree.item(selected_row, 'values')
            
            self.selected_id = row_values[0]
            self.common_name_var.set(row_values[1])
            self.sci_name_var.set(row_values[2])
            self.status_var.set(row_values[3])
            self.location_var.set(row_values[4])
        except IndexError:
            pass

    def update_record(self):
        """Update the currently selected record."""
        if not self.selected_id:
            messagebox.showwarning("Selection Error", "Please select a record to update.")
            return

        success = self.db.update_species(
            self.selected_id,
            self.common_name_var.get(),
            self.sci_name_var.get(),
            self.status_var.get(),
            self.location_var.get()
        )
        if success:
            messagebox.showinfo("Success", "Record updated successfully.")
            self.clear_inputs()
            self.populate_table()

    def delete_record(self):
        """Delete the currently selected record."""
        if not self.selected_id:
            messagebox.showwarning("Selection Error", "Please select a record to delete.")
            return
        
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?")
        if confirm:
            success = self.db.delete_species(self.selected_id)
            if success:
                messagebox.showinfo("Deleted", "Record removed from database.")
                self.clear_inputs()
                self.populate_table()

    def clear_inputs(self):
        """Clear all entry fields and reset selection."""
        self.common_name_var.set("")
        self.sci_name_var.set("")
        self.status_var.set("")
        self.location_var.set("")
        self.selected_id = None
        self.tree.selection_remove(self.tree.selection())

if __name__ == "__main__":
    root = tk.Tk()
    app = MarineGUI(root)
    root.mainloop()