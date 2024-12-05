import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

# File to store data
FILE_NAME = "exam_centers.csv"

# Ensure the CSV file exists with headers
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "CENTER CODE", "CENTER NAME", "DISTRICT", "STATE", 
            "ALLOTTED STUDENTS", "STUDENT ROLL NO", 
            "STUDENT NAME", "SCHOOL", "CLASS (10/12)"
        ])

# Function to read data from the CSV
def read_data():
    with open(FILE_NAME, "r") as file:
        reader = csv.DictReader(file)
        return list(reader)

# Function to write data to the CSV
def write_data(data):
    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "CENTER CODE", "CENTER NAME", "DISTRICT", "STATE", 
            "ALLOTTED STUDENTS", "STUDENT ROLL NO", 
            "STUDENT NAME", "SCHOOL", "CLASS (10/12)"
        ])
        writer.writeheader()
        writer.writerows(data)

# Admin panel
def admin_panel():
    def refresh_table():
        for row in tree.get_children():
            tree.delete(row)
        for row in read_data():
            tree.insert("", "end", values=list(row.values()))
    
    def add_record():
        new_record = {
            "CENTER CODE": entry_center_code.get(),
            "CENTER NAME": entry_center_name.get(),
            "DISTRICT": entry_district.get(),
            "STATE": entry_state.get(),
            "ALLOTTED STUDENTS": entry_allotted_students.get(),
            "STUDENT ROLL NO": entry_student_rollno.get(),
            "STUDENT NAME": entry_student_name.get(),
            "SCHOOL": entry_school.get(),
            "CLASS (10/12)": entry_class.get(),
        }
        data = read_data()
        data.append(new_record)
        write_data(data)
        refresh_table()
        messagebox.showinfo("Success", "Record added successfully!")
        clear_fields()

    def delete_record():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Select a record to delete!")
            return
        data = read_data()
        selected_index = tree.index(selected_item[0])
        data.pop(selected_index)
        write_data(data)
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

    frame = tk.Frame(admin_window)
    frame.pack(fill="both", expand=True)

    # Entry fields for new data
    labels = [
        "Center Code", "Center Name", "District", "State", 
        "Allotted Students", "Student Roll No", 
        "Student Name", "School", "Class (10/12)"
    ]
    entries = []
    for i, label in enumerate(labels):
        lbl = tk.Label(frame, text=label)
        lbl.grid(row=i, column=0, padx=5, pady=5)
        entry = tk.Entry(frame)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries.append(entry)
    (entry_center_code, entry_center_name, entry_district, entry_state, 
     entry_allotted_students, entry_student_rollno, 
     entry_student_name, entry_school, entry_class) = entries

    # Buttons for operations
    btn_add = tk.Button(frame, text="Add Record", command=add_record)
    btn_add.grid(row=0, column=2, padx=5, pady=5)
    btn_delete = tk.Button(frame, text="Delete Selected", command=delete_record)
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
        tree.insert("", "end", values=list(row.values()))

# Login screen
root = tk.Tk()
root.title("Exam Center Management")
root.geometry("300x200")

frame = tk.Frame(root)
frame.pack(pady=20)

btn_admin = tk.Button(frame, text="Admin Login", width=15, command=admin_panel)
btn_admin.grid(row=0, column=0, padx=5, pady=10)

btn_student = tk.Button(frame, text="Student Login", width=15, command=student_panel)
btn_student.grid(row=1, column=0, padx=5, pady=10)

root.mainloop()
