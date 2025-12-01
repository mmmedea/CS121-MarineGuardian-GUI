Marine Biodiversity Tracker

Description/Overview
Marine Guardian is a professional desktop-based management system designed to support marine conservation efforts aligned with SDG 14: Life Below Water. The program helps environmental researchers and conservationists digitally track, monitor, and manage data regarding marine species in Philippine waters.

The application serves as a digitized logbook that supports full data management capabilities. Users can record new species sightings, update population health statuses, view comprehensive lists of marine life, and remove outdated records. By replacing manual logging systems with a secure database-driven application, Marine Guardian raises awareness of endangered species and provides a potential solution for data-driven biodiversity preservation.

Programming Concepts Applied
This project demonstrates several key concepts from CS 121: Advance Computer Programming:
Database Management (CRUD)
  * Create: The system allows users to insert new species records into a persistent SQL database.
  * Read: Data is retrieved and displayed dynamically in a table view for easy monitoring.
  * Update: Existing records can be modified to reflect changes in conservation status or location.
  * Delete: The system includes functionality to safely remove erroneous or duplicate entries.

Graphical User Interface (GUI)
  * Event Handling: The application utilizes event-driven programming to respond to user button clicks and list selections.
  * Widget Implementation: Integrates various UI components (Labels, Entries, Buttons, Treeviews) using the Tkinter framework.
  * User Experience: Focuses on a layout that is functional, user-friendly, and aligned with the project's purpose.

Data Persistence & Integrity
  * SQLite Integration: The project moves beyond temporary memory by connecting to a local SQLite database (`marine_life.db`) to ensure data remains saved even after the program closes.
  * Error Handling: Implements `try-except` blocks and input validation to prevent crashes during database connections or invalid user inputs.

Modular Architecture
  * Separation of Concerns: The code is structured to separate the backend database logic from the frontend user interface code, ensuring maintainability and code clarity.

Program Structure
The application follows a modular architecture with clear separation of duties:

Core Modules and Their Roles
MarineDatabase (Backend Logic)
  * Role: Manages all direct interactions with the SQLite database.
  * Key Methods:
      * `connect()`: Establishes the link to the `marine_life.db` file.
      * `insert_species()`: Executes SQL commands to save new data.
      * `fetch_all()`: Retrieves all rows for display in the GUI.
      * `update_species()` & `delete_species()`: Handles modification and removal of records.

MarineGUI (Frontend Interface)
  * Role: Manages the visual presentation and user interaction.
  * Key Features:
      * Input Forms: Collects Common Name, Scientific Name, Status, and Location.
      * Data Table: Displays the database records in a scrollable Treeview.
      * SDG Header: Visually promotes the project's alignment with Goal 14.
      * Button Logic: Connects visual clicks to specific backend functions.

Class Relationships
`MarineGUI` - initializes `MarineDatabase` - calls `fetch_all()` to populate table - calls `insert/update/delete` based on user input -`MarineDatabase` executes SQL on `marine_life.db`

How to Run the Program
Prerequisites

  * Python 3.x installed on your system.
  * Tkinter Library (Usually included with Python).
  * SQLite3 (Included with Python standard library).

Step-by-Step Instructions
1.  Navigate to the project directory

    ```bash
    cd path/to/MarineGuardian
    ```
2.  Run the program

    ```bash
    python marine_guardian.py
    ```

Important Notes
  * The `marine_life.db` file will be created automatically in the same folder upon the first run.
  * Ensure you have write permissions in the folder so the database file can be saved.

SAMPLE GUI VISUALIZATION
```text
+-------------------------------------------------------+
|  MarineGuardian - Supporting SDG 14: Life Below Water |
+-------------------------------------------------------+
|  [ Manage Species Records ]                           |
|                                                       |
|  Common Name: [ Clownfish      ]  Sci Name: [.....]   |
|  Status:      [ Least Concern v]  Location: [.....]   |
|                                                       |
|  [Add Record] [Update Selected] [Delete] [Clear]      |
+-------------------------------------------------------+
| ID | Common Name  | Scientific Name | Status      |   |
|----|--------------|-----------------|-------------|   |
| 1  | Green Turtle | Chelonia mydas  | Endangered  |   |
| 2  | Dugong       | Dugong dugon    | Vulnerable  |   |
| 3  | Blue Whale   | B. musculus     | Endangered  |   |
|    |              |                 |             |   |
+-------------------------------------------------------+
```

Author and Acknowledgement
Author:
Martinez, Maricris M.
Course: CS 121 - Advance Computer Programming
Institution: Batangas State University - The National Engineering University

Acknowledgements:
This project was developed as a final requirement for CS 121. It adheres to the university's academic guidelines and integrates Sustainable Development Goals into technical application development.

Future Enhancements
Potential improvements for future versions:

  * Image Upload: Allow users to attach photos of the sighted species.
  * Map Integration: Visualize sighting locations on a GPS map.
  * Export Data: Ability to export the database to CSV or Excel for reporting.
  * Search Filter: Advanced search bar to filter by Conservation Status.
  * User Authentication: Login system for multiple researchers.
  * Cloud Sync: Sync database with a cloud server for remote access.

References
  * Python Documentation: [https://docs.python.org/3/](https://docs.python.org/3/)
  * Tkinter References: Python Standard Library GUI
  * SDG 14 Guidelines: United Nations Sustainable Development Goals