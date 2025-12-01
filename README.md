MARINE GUARDIAN Marine Biodiversity Tracker

Description
Marine Guardian is a modernized desktop-based management system designed to support marine conservation efforts aligned with SDG 14: Life Below Water. The program helps environmental researchers and conservationists digitally track, monitor, and analyze data regarding marine species in Philippine waters.

The application serves as a comprehensive digital logbook that goes beyond simple data entry. It features a modern dark-mode interface for comfortable usage during night patrols or lab work. Users can record new sightings with automated date stamping, visualize population health through integrated bar charts, and dynamically sort records to analyze trends. By replacing manual logging systems with a secure, graphical, and analytical tool, Marine Guardian provides a potential technical solution for data-driven biodiversity preservation.

Key Programming Concepts
This project demonstrates several advanced concepts from CS 121: Advance Computer Programming:

Database Management (CRUD)
Create: The system allows users to insert new species records into a persistent SQL database, automatically capturing the date of the sighting.
Read: Data is retrieved and displayed dynamically in a scrollable table view.
Update: Existing records can be modified to reflect changes in conservation status or location.
Delete: The system includes functionality to safely remove erroneous or duplicate entries with user confirmation.

Graphical User Interface (GUI)
Widget Implementation: Utilizes Tkinter and Ttk to create a professional flat design interface with custom styling, color-coding, and split-panel layouts.
Data Visualization: Integrates the Matplotlib library to render real-time statistical graphs within the application.
Event Handling: Uses advanced event binding to handle list selections, button clicks, and window management.

Data Persistence and Integrity
SQLite Integration: Connects to a local SQLite database (marine_life.db) to ensure data remains saved permanently.
Automated Logic: The system automatically generates timestamps using the datetime module, reducing human error during data entry.

Program Structure
The application follows a modular architecture with clear separation of duties:

Core Modules and Their Roles
MarineDatabase (Backend Logic)
Role: Manages all direct interactions with the SQLite database.
Key Methods:
connect(): Establishes the link to the database file.
insert_species(): Saves new data and the current date.
fetch_all(): Retrieves rows, with logic to sort by name, date, or ID.
get_status_counts(): Analyzes the data to count how many species are in each conservation category for the graph.

MarineGUI (Frontend Interface)
Role: Manages the visual presentation, user interaction, and data visualization.
Key Features:
Modern Input Form: A resized, user-friendly panel for typing species details.
Smart Toolbar: Buttons to sort the list by Date Recorded or Common Name.
Analytics Dashboard: A specific function that generates a pop-up bar chart showing the balance of endangered vs. stable species.
SDG Header: Visually promotes the project's alignment with Goal 14.

Class Relationships
MarineGUI initializes MarineDatabase.
MarineGUI calls fetch_all() to populate the table.
When the View Graph button is clicked, MarineGUI calls get_status_counts() and uses Matplotlib to draw the chart.

How to Run the Program
Prerequisites
Python 3.x installed on your system.
Tkinter Library (Included with Python).
Matplotlib Library (Must be installed).

Step-by-Step Instructions
1. Open your terminal or command prompt.
2. Install the required graphing library:
python -m pip install matplotlib
3. Run the program:
python marine_guardian.py

Important Notes
If you have an old database file from a previous version, delete it before running this version so the new date columns can be created.

SAMPLE GUI VISUALIZATION

```text
+-------------------------------------------------------------+
|  MARINE GUARDIAN                                            |
|  SDG 14: Life Below Water - Digital Logbook                 |
+-------------------------------------------------------------+
|  NEW SIGHTING               |  SIGHTING HISTORY             |
|                             |                               |
|  Common Name:               |  [Date Sort]   [Name Sort]    |
|  [__________________]       |                               |
|                             |  +----+--------+------------+ |
|  Scientific Name:           |  | ID | Name   | Date       | |
|  [__________________]       |  |----|--------|------------| |
|                             |  | 1  | Dory   | 2025-12-01 | |
|  Location:                  |  | 2  | Nemo   | 2025-12-01 | |
|  [__________________]       |  +----+--------+------------+ |
|                             |                               |
|  [ Add Record    ] (Green)  |                               |
|  [ Update Record ] (Blue)   |                               |
|  [ Delete Record ] (Red)    |                               |
|  [ Clear Form    ] (Grey)   |                               |
+-------------------------------------------------------------+

Author and Acknowledgement
Author:
Martinez, Maricris M.

Course: CS 121: Advance Computer Programming
Institution: Batangas State University - The National Engineering University

Acknowledgements
This project was developed as a final requirement for CS 121. It adheres to the university's academic guidelines and integrates Sustainable Development Goals into technical application development.

Future Enhancements
Potential improvements for future versions:
Image Upload: Allow users to attach photos of the sighted species.
Map Integration: Visualize sighting locations on a GPS map.
Export Data: Ability to export the database to CSV or Excel for reporting.
Search Filter: Advanced search bar to filter by Conservation Status.

References
Python Documentation: https://docs.python.org/3/
Matplotlib Documentation: https://matplotlib.org/
SDG 14 Guidelines: United Nations Sustainable Development Goals