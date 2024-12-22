import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Database setup
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Vicky0604@#$"  # Replace with your MySQL root password
DB_NAME = "exam_center_management"
TABLE_NAME = "exam_centers"

# Connect to MySQL and create database and table if they don't exist
def init_db():
    conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    conn.close()

    conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            center_code VARCHAR(255),
            center_name VARCHAR(255),
            district VARCHAR(255),
            state VARCHAR(255),
            allotted_students INT,
            student_roll_no VARCHAR(255),
            student_name VARCHAR(255),
            school VARCHAR(255),
            class VARCHAR(10)
        )
    ''')
    conn.close()

init_db()

# Function to read data from the database
def read_data():
    conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {TABLE_NAME}")
    data = cursor.fetchall()
    conn.close()
    return data

# Function to add a new record to the database
def add_data(record):
    conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f'''
        INSERT INTO {TABLE_NAME} (
            center_code, center_name, district, state, allotted_students, 
            student_roll_no, student_name, school, class
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', record)
    conn.commit()
    conn.close()

# Function to delete a record from the database
def delete_data(center_code):
    conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE center_code = %s", (center_code,))
    conn.commit()
    conn.close()

# Admin panel
def admin_panel():
    def refresh_table():
        for row in tree.get_children():
            tree.delete(row)
        for row in read_data():
            tree.insert("", "end", values=row)

    def add_record():
        new_record = (
            entry_center_code.get(),
            entry_center_name.get(),
            entry_district.get(),
            entry_state.get(),
            entry_allotted_students.get(),
            entry_student_rollno.get(),
            entry_student_name.get(),
            entry_school.get(),
            entry_class.get()
        )
        add_data(new_record)
        refresh_table()
        messagebox.showinfo("Success", "Record added successfully!")
        clear_fields()

    def delete_record():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Select a record to delete!")
            return
        center_code = tree.item(selected_item[0], "values")[0]
        delete_data(center_code)
        refresh_table()
        messagebox.showinfo("Success", "Record deleted successfully!")

    def clear_fields():
        entry_center_code.delete(0, tk.END)
        entry_center_name.delete(0, tk.END)
        entry_district.delete(0, tk.END)
        entry_state.delete(0, tk.END)
        entry_allotted_students.delete(0, tk.END)
        entry_student_rollno.delete(0, tk.END)
        entry_student_name.delete(0, tk.END)
        entry_school.delete(0, tk.END)
        entry_class.delete(0, tk.END)

    admin_window = tk.Toplevel(root)
    admin_window.title("Admin Panel")
    admin_window.geometry("900x500")

    # Set background color
    admin_window.configure(bg="#f0f8ff")

    frame = tk.Frame(admin_window, bg="#f0f8ff")
    frame.pack(fill="both", expand=True)

    # Entry fields for new data
    labels = [
        "Center Code", "Center Name", "District", "State", 
        "Allotted Students", "Student Roll No", 
        "Student Name", "School", "Class (10/12)"
    ]
    entries = []
    for i, label in enumerate(labels):
        lbl = tk.Label(frame, text=label, bg="#f0f8ff", font=("Helvetica", 10, "bold"))
        lbl.grid(row=i, column=0, padx=5, pady=5)
        entry = tk.Entry(frame)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries.append(entry)
    (entry_center_code, entry_center_name, entry_district, entry_state, 
     entry_allotted_students, entry_student_rollno, 
     entry_student_name, entry_school, entry_class) = entries

    # Buttons for operations
    btn_add = tk.Button(frame, text="Add Record", bg="#20b2aa", fg="white", font=("Helvetica", 10, "bold"), command=add_record)
    btn_add.grid(row=0, column=2, padx=5, pady=5)
    btn_delete = tk.Button(frame, text="Delete Selected", bg="#dc143c", fg="white", font=("Helvetica", 10, "bold"), command=delete_record)
    btn_delete.grid(row=1, column=2, padx=5, pady=5)

    # Treeview for displaying data
    columns = [
        "CENTER CODE", "CENTER NAME", "DISTRICT", "STATE", 
        "ALLOTTED STUDENTS", "STUDENT ROLL NO", 
        "STUDENT NAME", "SCHOOL", "CLASS (10/12)"
    ]
    tree = ttk.Treeview(admin_window, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(fill="both", expand=True)
    refresh_table()

# Student panel
def student_panel():
    student_window = tk.Toplevel(root)
    student_window.title("Student Panel")
    student_window.geometry("800x400")

    # Set background color
    student_window.configure(bg="#ffe4e1")

    # Treeview for displaying data
    columns = [
        "CENTER CODE", "CENTER NAME", "DISTRICT", "STATE", 
        "ALLOTTED STUDENTS", "STUDENT ROLL NO", 
        "STUDENT NAME", "SCHOOL", "CLASS (10/12)"
    ]
    tree = ttk.Treeview(student_window, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(fill="both", expand=True)

    for row in read_data():
        tree.insert("", "end", values=row)

# Login screen
root = tk.Tk()
root.title("Exam Center Management")
root.geometry("300x200")

# Set background color
root.configure(bg="#fffacd")

frame = tk.Frame(root, bg="#fffacd")
frame.pack(pady=20)

btn_admin = tk.Button(frame, text="Admin Login", width=15, bg="#4682b4", fg="white", font=("Helvetica", 10, "bold"), command=admin_panel)
btn_admin.grid(row=0, column=0, padx=5, pady=10)

btn_student = tk.Button(frame, text="Student Login", width=15, bg="#32cd32", fg="white", font=("Helvetica", 10, "bold"), command=student_panel)
btn_student.grid(row=1, column=0, padx=5, pady=10)

root.mainloop()
