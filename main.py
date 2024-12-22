import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
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

# Function to change background image
def change_background():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
    if file_path:
        bg_image = Image.open(file_path)
        bg_image = bg_image.resize((root.winfo_width(), root.winfo_height()), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        background_label.config(image=bg_photo)
        background_label.image = bg_photo

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
        write_data([new_record])  # Add the record to the database
        refresh_table()
        messagebox.showinfo("Success", "Record added successfully!")
        clear_fields()

    def delete_record():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Select a record to delete!")
            return
        selected_id = tree.item(selected_item[0])['values'][0]
        try:
            connection = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            cursor = connection.cursor()
            cursor.execute("DELETE FROM exam_centers WHERE id = %s", (selected_id,))
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
    admin_window.geometry("900x600")

    input_frame = tk.Frame(admin_window, bg='#d9f2e6', relief='ridge', bd=5)
    input_frame.pack(side="top", fill="x", padx=10, pady=10)

    # Input fields
    labels = [
        "Center Code", "Center Name", "District", "State",
        "Allotted Students", "Student Roll No",
        "Student Name", "School", "Class (10/12)"
    ]
    entries = {}
    for i, label in enumerate(labels):
        tk.Label(input_frame, text=label, bg='#d9f2e6').grid(row=i, column=0, padx=5, pady=5, sticky="w")
        entry = tk.Entry(input_frame, width=30)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries[label] = entry
    (entry_center_code, entry_center_name, entry_district, entry_state,
     entry_allotted_students, entry_student_rollno, 
     entry_student_name, entry_school, entry_class) = entries.values()

    tk.Button(input_frame, text="Add Record", command=add_record, bg='#28a745', fg='white').grid(row=0, column=2, padx=5, pady=5)
    tk.Button(input_frame, text="Delete Selected", command=delete_record, bg='#dc3545', fg='white').grid(row=1, column=2, padx=5, pady=5)

    # Table
    columns = ["ID"] + labels
    tree = ttk.Treeview(admin_window, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(fill="both", expand=True)
    refresh_table()

# Student panel
def student_panel():
    student_window = tk.Toplevel(root)
    student_window.title("Student Panel")
    student_window.geometry("900x500")

    columns = ["ID", "Center Code", "Center Name", "District", "State", "Allotted Students",
               "Student Roll No", "Student Name", "School", "Class (10/12)"]
    tree = ttk.Treeview(student_window, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(fill="both", expand=True)

    for row in read_data():
        tree.insert("", "end", values=list(row.values()))

# Main window
root = tk.Tk()
root.title("Exam Center Management")
root.geometry("800x600")

bg_image = Image.open("default_bg.jpg").resize((800, 600), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)
background_label = tk.Label(root, image=bg_photo)
background_label.place(relwidth=1, relheight=1)

frame = tk.Frame(root, bg="#ffffff", relief="ridge", bd=10)
frame.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(frame, text="Exam Center Management", font=("Arial", 20), bg="#ffffff").grid(row=0, column=0, columnspan=2, pady=10)
tk.Button(frame, text="Admin Login", command=admin_panel, bg="#007bff", fg="white", width=15).grid(row=1, column=0, padx=10, pady=10)
tk.Button(frame, text="Student Login", command=student_panel, bg="#007bff", fg="white", width=15).grid(row=1, column=1, padx=10, pady=10)

tk.Button(root, text="Change Background", command=change_background, bg="#ffc107", fg="black").pack(side="bottom", pady=10)

create_table()
root.mainloop()