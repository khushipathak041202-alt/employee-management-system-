# Employee Management System

A beginner-friendly command-line project built with **Python** and **SQLite**. It helps manage employee records and stores them in a local database.

## Features

- Add employee records
- View all employees
- Search employees by ID
- Update employee details
- Delete employee records with confirmation
- Validate required fields and salary values
- Prevent duplicate email addresses
- Store records persistently in SQLite

## Technology Stack

- Python 3
- SQLite (included with Python's standard library)

## Requirements

Python 3.9 or newer is recommended. No third-party packages are required.

## How to Run

1. Download or clone this repository.
2. Open a terminal or Command Prompt in the project folder.
3. Run:

   ```bash
   python employee_management.py
   ```

   On some Windows systems, use:

   ```bash
   py employee_management.py
   ```

4. Choose an option from the menu.

The `employees.db` database file is created automatically the first time the program runs.

## Database Fields

| Field | Description |
|---|---|
| employee_id | Automatically generated unique ID |
| name | Employee name |
| department | Employee department |
| email | Unique email address |
| salary | Monthly salary; must be zero or greater |

## Learning Outcomes

This project demonstrates Python functions, loops, exception handling, input validation, SQL queries, parameterized database operations, and CRUD (Create, Read, Update, Delete) functionality.

## Important

Run and test the project yourself, understand how each feature works, and customize it before listing it on a resume.
