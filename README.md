# Restaurant Menu GUI (TESTING)

A Python-based graphical user interface (GUI) application for managing a restaurant menu. Built using **CustomTkinter (CTk)**, this program allows users to view menu items, add new items, and save changes to a JSON file. The application emphasizes a responsive and interactive single-window experience with live updates.

---

## Table of Contents

- [Restaurant Menu GUI (TESTING)](#restaurant-menu-gui-testing)
  - [Table of Contents](#table-of-contents)
  - [Project Structure](#project-structure)
  - [Features](#features)
  - [Installation](#installation)
  - [Dependencies](#dependencies)
  - [How it Works](#how-it-works)

---

## Project Structure
```
restaurant_gui/
│
├── src/
│ ├── gui_main.py # Main application GUI
│ ├── options_menu.py # Handles menu options and backend logic
│ └── utils.py # Helper functions (load, save, exit)
│
├── data/
│ └── restaurant_data.json # JSON file storing restaurant menu
│
├── venv/ # Python virtual environment
├── requirements.txt # Project dependencies
└── README.md # Project documentation
```

---

## Features

- Single-window GUI for all operations (no pop-ups).  
- Scrollable, responsive menu display.  
- Add new menu items dynamically.  
- Save changes to a JSON file.  
- Visual feedback via frame highlighting on successful operations.  
- Out-of-stock items clearly labeled.  
- Resizable window with dynamically adjusting layout.  

---

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd restaurant_gui
```

2. Create a Python virtual environment (if not already created):
```
python -m venv venv
```
3. Activate the virtual environment

* Mac Activation
```
source venv/bin/activate
```

* Windows Activation
```
source venv/bin/activate
```

4. Install Dependencies
```
pip install -r requirements.txt
```

5. Run program
```
python src/gui_main.py
```

---

## Dependencies

* Python 3.10+
* CustomTkinter
* Standard Py Libraries: json, time, os
* All requirements listed in requirements.txt

---

## How it Works

1. Initialization: Loads restaurant data from data/restaurant_data.json.
2. Sidebar Buttons:
   * View Menu: Displays categories and items in a scrollable frame.
   * Add Item: Adds new menu items directly in the main window.
   * Save Data: Writes changes back to JSON and highlights the frame.
   * Exit: Closes the program safely.
3. Menu Display:
   * Scrollable canvas with an inner frame to hold menu items.
   * Resizes dynamically with window width.
   * Out-of-stock items are clearly marked.
4. Add Items: Category selection, item name, and price input with validation.
5. Highlight Feedback: Temporary color change on successful operations.