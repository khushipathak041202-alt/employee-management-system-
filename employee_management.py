"""
Employee Management System
A beginner-friendly Python CLI project using SQLite.

Run:
    python employee_management.py
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("employees.db")


def connect_db():
    """Connect to the SQLite database and ensure the employees table exists."""
    connection = sqlite3.connect(DB_PATH)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            salary REAL NOT NULL CHECK (salary >= 0)
        )
    """)
    connection.commit()
    return connection


def add_employee():
    print("\n--- Add Employee ---")
    name = input("Employee name: ").strip()
    department = input("Department: ").strip()
    email = input("Email: ").strip()
    salary_text = input("Monthly salary: ").strip()

    if not all([name, department, email, salary_text]):
        print("Error: All fields are required.")
        return

    try:
        salary = float(salary_text)
        if salary < 0:
            print("Error: Salary cannot be negative.")
            return
    except ValueError:
        print("Error: Salary must be a number.")
        return

    try:
        with connect_db() as connection:
            connection.execute(
                "INSERT INTO employees (name, department, email, salary) VALUES (?, ?, ?, ?)",
                (name, department, email, salary),
            )
        print("Employee added successfully.")
    except sqlite3.IntegrityError:
        print("Error: This email already exists. Use a unique email address.")


def view_employees():
    print("\n--- Employee List ---")
    with connect_db() as connection:
        rows = connection.execute(
            "SELECT employee_id, name, department, email, salary "
            "FROM employees ORDER BY employee_id"
        ).fetchall()

    if not rows:
        print("No employee records found.")
        return

    print("-" * 90)
    print(f"{'ID':<5} {'Name':<20} {'Department':<16} {'Email':<30} {'Salary':>12}")
    print("-" * 90)
    for employee_id, name, department, email, salary in rows:
        print(f"{employee_id:<5} {name[:19]:<20} {department[:15]:<16} {email[:29]:<30} {salary:>12.2f}")
    print("-" * 90)


def search_employee():
    print("\n--- Search Employee ---")
    search_id = input("Enter employee ID: ").strip()
    if not search_id.isdigit():
        print("Error: Employee ID must be a whole number.")
        return

    with connect_db() as connection:
        row = connection.execute(
            "SELECT employee_id, name, department, email, salary "
            "FROM employees WHERE employee_id = ?",
            (int(search_id),),
        ).fetchone()

    if row:
        print(f"\nID: {row[0]}\nName: {row[1]}\nDepartment: {row[2]}\nEmail: {row[3]}\nSalary: {row[4]:.2f}")
    else:
        print("No employee found with that ID.")


def update_employee():
    print("\n--- Update Employee ---")
    employee_id = input("Enter employee ID to update: ").strip()
    if not employee_id.isdigit():
        print("Error: Employee ID must be a whole number.")
        return

    with connect_db() as connection:
        existing = connection.execute(
            "SELECT employee_id, name, department, email, salary "
            "FROM employees WHERE employee_id = ?",
            (int(employee_id),),
        ).fetchone()

    if not existing:
        print("No employee found with that ID.")
        return

    print("Press Enter to keep the current value.")
    name = input(f"Name [{existing[1]}]: ").strip() or existing[1]
    department = input(f"Department [{existing[2]}]: ").strip() or existing[2]
    email = input(f"Email [{existing[3]}]: ").strip() or existing[3]
    salary_text = input(f"Salary [{existing[4]:.2f}]: ").strip()

    try:
        salary = float(salary_text) if salary_text else existing[4]
        if salary < 0:
            print("Error: Salary cannot be negative.")
            return
    except ValueError:
        print("Error: Salary must be a number.")
        return

    try:
        with connect_db() as connection:
            connection.execute(
                "UPDATE employees SET name = ?, department = ?, email = ?, salary = ? "
                "WHERE employee_id = ?",
                (name, department, email, salary, int(employee_id)),
            )
        print("Employee updated successfully.")
    except sqlite3.IntegrityError:
        print("Error: That email address is already used by another employee.")


def delete_employee():
    print("\n--- Delete Employee ---")
    employee_id = input("Enter employee ID to delete: ").strip()
    if not employee_id.isdigit():
        print("Error: Employee ID must be a whole number.")
        return

    confirm = input(f"Delete employee ID {employee_id}? Type yes to confirm: ").strip().lower()
    if confirm != "yes":
        print("Deletion cancelled.")
        return

    with connect_db() as connection:
        cursor = connection.execute(
            "DELETE FROM employees WHERE employee_id = ?",
            (int(employee_id),),
        )
        deleted = cursor.rowcount

    print("Employee deleted successfully." if deleted else "No employee found with that ID.")


def show_menu():
    print("""
========== Employee Management System ==========
1. Add employee
2. View all employees
3. Search employee by ID
4. Update employee
5. Delete employee
6. Exit
""")


def main():
    connect_db().close()
    while True:
        show_menu()
        choice = input("Choose an option (1-6): ").strip()
        actions = {
            "1": add_employee,
            "2": view_employees,
            "3": search_employee,
            "4": update_employee,
            "5": delete_employee,
        }

        if choice in actions:
            actions[choice]()
        elif choice == "6":
            print("Thank you for using Employee Management System!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
