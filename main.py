import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

# MySQL connection details
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Vicky0604@#$"
DB_NAME = "exam_center_db"

# Function to create the table if it doesn't exist
def create_table():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exam_centers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                center_code VARCHAR(50),
                center_name VARCHAR(100),
                district VARCHAR(100),
                state VARCHAR(100),
                allotted_students INT,
                student_rollno VARCHAR(50),
                student_name VARCHAR(100),
                school VARCHAR(100),
                class_type VARCHAR(10)
            )
        """)
        connection.commit()
        cursor.close()
        connection.close()
    except Error as e:
        print(f"Error: {e}")

# Function to read data from the database
def read_data():
    data = []
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM exam_centers")
        data = cursor.fetchall()
        cursor.close()
        connection.close()
    except Error as e:
        print(f"Error: {e}")
    return data

# Function to write data to the database
def write_data(data):
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = connection.cursor()
        cursor.executemany("""
            INSERT INTO exam_centers (
                center_code, center_name, district, state, allotted_students, 
                student_rollno, student_name, school, class_type
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, data)
        connection.commit()
        cursor.close()
        connection.close()
    except Error as e:
        print(f"Error: {e}")

# Admin panel
def admin_panel():
    def refresh_table():
        for row in tree.get_children():
            tree.delete(row)
        for row in read_data():
            tree.insert("", "end", values=list(row.values()))
    
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
        data = read_data()
        data.append(new_record)
        write_data([new_record])  # Pass a list of one new record
        refresh_table()
        messagebox.showinfo("Success", "Record added successfully!")
        clear_fields()

    def delete_record():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Select a record to delete!")
            return
        selected_index = tree.index(selected_item[0])
        row = read_data()[selected_index]
        try:
            connection = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            cursor = connection.cursor()
            cursor.execute("DELETE FROM exam_centers WHERE id = %s", (row["id"],))
            connection.commit()
            cursor.close()
            connection.close()
            refresh_table()
            messagebox.showinfo("Success", "Record deleted successfully!")
        except Error as e:
            print(f"Error: {e}")

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
    admin_window.configure(bg='sky blue')

    frame = tk.Frame(admin_window, bg='sky blue')
    frame.pack(fill="both", expand=True)

    labels = [
        "Center Code", "Center Name", "District", "State", 
        "Allotted Students", "Student Roll No", 
        "Student Name", "School", "Class (10/12)"
    ]
    entries = []
    for i, label in enumerate(labels):
        lbl = tk.Label(frame, text=label, fg='white', bg='sky blue')
        lbl.grid(row=i, column=0, padx=5, pady=5)
        entry = tk.Entry(frame)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries.append(entry)
    (entry_center_code, entry_center_name, entry_district, entry_state, 
     entry_allotted_students, entry_student_rollno, 
     entry_student_name, entry_school, entry_class) = entries

    btn_add = tk.Button(frame, text="Add Record", command=add_record, bg='white', fg='black')
    btn_add.grid(row=0, column=2, padx=5, pady=5)
    btn_delete = tk.Button(frame, text="Delete Selected", command=delete_record, bg='white', fg='black')
    btn_delete.grid(row=1, column=2, padx=5, pady=5)

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
    student_window.configure(bg='sky blue')

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
root.configure(bg='sky blue')


frame = tk.Frame(root, bg='sky blue')
frame.pack(pady=20)

btn_admin = tk.Button(frame, text="Admin Login", width=15, command=admin_panel, bg='white', fg='black')
btn_admin.grid(row=0, column=0, padx=5, pady=10)

btn_student = tk.Button(frame, text="Student Login", width=15, command=student_panel, bg='white', fg='black')
btn_student.grid(row=1, column=0, padx=5, pady=10)

# Create table when the program starts
create_table()

root.mainloop()
