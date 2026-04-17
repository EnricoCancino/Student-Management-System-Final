from tkinter import *
from tkinter import ttk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from datetime import datetime
import time
import mysql.connector
from mysql.connector import Error
import csv
import os

window = Tk()
window.geometry("1280x700+0+0")
window.resizable(False, False)
window.title("Student Management System")

# ============== GLOBAL VARIABLES ==============
DB_CONNECTION = None
table = None

# ============== DATABASE CONNECTION ==============
def connect_database(host, user, password):
    global DB_CONNECTION
    try:
        DB_CONNECTION = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database="student_management"
        )
        messagebox.showinfo("Success", "Connected to Database Successfully!")
        ensure_student_columns()
        load_students()
    except Error as err:
        messagebox.showerror("Error", f"Connection Failed: {err}")
        messagebox.showinfo("Troubleshooting", "Make sure MySQL is running and the credentials are correct.")

def open_connection_window():
    conn_window = Toplevel(window)
    conn_window.title("Database Authorization")
    conn_window.geometry("380x250")
    conn_window.resizable(False, False)

    Label(conn_window, text="Host:", font=("Arial", 10)).pack(pady=5)
    host_entry = Entry(conn_window, width=30, font=("Arial", 10))
    host_entry.pack()
    host_entry.insert(0, "localhost")

    Label(conn_window, text="Username:", font=("Arial", 10)).pack(pady=5)
    user_entry = Entry(conn_window, width=30, font=("Arial", 10))
    user_entry.pack()

    Label(conn_window, text="Password:", font=("Arial", 10)).pack(pady=5)
    password_entry = Entry(conn_window, width=30, font=("Arial", 10), show="*")
    password_entry.pack()

    def do_connect():
        host = host_entry.get().strip()
        user = user_entry.get().strip()
        password = password_entry.get().strip()

        if not host or not user or not password:
            messagebox.showwarning("Warning", "Host, username, and password are all required!", parent=conn_window)
            return

        connect_database(host, user, password)
        conn_window.destroy()

    Button(conn_window, text="Connect", font=("Arial", 11), bg="#4CAF50", fg="white", command=do_connect).pack(pady=15, ipadx=10, ipady=5)
    conn_window.grab_set()


def disconnect_database():
    global DB_CONNECTION
    if DB_CONNECTION and DB_CONNECTION.is_connected():
        DB_CONNECTION.close()
        messagebox.showinfo("Success", "Disconnected from Database")

def execute_query(query, params=None, fetch=False):
    global DB_CONNECTION
    try:
        if not DB_CONNECTION or not DB_CONNECTION.is_connected():
            messagebox.showerror("Error", "Not connected to database. Click 'Connect To Database' first!")
            return None
        
        cursor = DB_CONNECTION.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch:
            result = cursor.fetchall()
        else:
            DB_CONNECTION.commit()
            result = cursor.rowcount
        
        cursor.close()
        return result
    except Error as err:
        messagebox.showerror("Error", f"Query Failed: {err}")
        return None


def ensure_student_columns():
    global DB_CONNECTION
    if not DB_CONNECTION or not DB_CONNECTION.is_connected():
        return

    cursor = DB_CONNECTION.cursor()
    try:
        cursor.execute("SHOW COLUMNS FROM students")
        existing_columns = {row[0] for row in cursor.fetchall()}

        if "birthday" not in existing_columns:
            cursor.execute("ALTER TABLE students ADD COLUMN birthday VARCHAR(20) NULL")
        if "address" not in existing_columns:
            cursor.execute("ALTER TABLE students ADD COLUMN address VARCHAR(255) NULL")
        if "gender" not in existing_columns:
            cursor.execute("ALTER TABLE students ADD COLUMN gender VARCHAR(10) NULL")

        DB_CONNECTION.commit()
    except Error:
        pass
    finally:
        cursor.close()

# ============== STUDENT MANAGEMENT FUNCTIONS ==============
def load_students():
    """Load all students from database to table"""
    if table is None:
        return
    
    for item in table.get_children():
        table.delete(item)
    
    query = "SELECT id, name, mobile, email, birthday, address, gender FROM students"
    students = execute_query(query, fetch=True)
    
    if students:
        for student in students:
            table.insert("", END, values=student)

def add_student():
    """Open dialog to add new student"""
    if DB_CONNECTION is None or not DB_CONNECTION.is_connected():
        messagebox.showerror("Error", "Not connected to database!")
        return
    
    add_window = Toplevel(window)
    add_window.title("Add Student")
    add_window.geometry("500x460")
    add_window.resizable(False, False)
    
    Label(add_window, text="Name:", font=("Arial", 10)).pack(pady=5)
    name_entry = Entry(add_window, width=40, font=("Arial", 10))
    name_entry.pack(pady=5)
    
    Label(add_window, text="Mobile No:", font=("Arial", 10)).pack(pady=5)
    mobile_entry = Entry(add_window, width=40, font=("Arial", 10))
    mobile_entry.pack(pady=5)
    
    Label(add_window, text="Email:", font=("Arial", 10)).pack(pady=5)
    email_entry = Entry(add_window, width=40, font=("Arial", 10))
    email_entry.pack(pady=5)
    
    Label(add_window, text="Birthday (YYYY-MM-DD):", font=("Arial", 10)).pack(pady=5)
    birthday_entry = Entry(add_window, width=40, font=("Arial", 10))
    birthday_entry.pack(pady=5)
    
    Label(add_window, text="Address:", font=("Arial", 10)).pack(pady=5)
    address_entry = Entry(add_window, width=40, font=("Arial", 10))
    address_entry.pack(pady=5)
    
    Label(add_window, text="Gender:", font=("Arial", 10)).pack(pady=5)
    gender_combobox = ttk.Combobox(add_window, values=["Male", "Female"], state="readonly", width=38)
    gender_combobox.pack(pady=5)
    gender_combobox.current(0)
    
    def save_student():
        name = name_entry.get().strip()
        mobile = mobile_entry.get().strip()
        email = email_entry.get().strip()
        birthday = birthday_entry.get().strip()
        address = address_entry.get().strip()
        gender = gender_combobox.get().strip()
        
        if not name or not mobile or not email or not birthday or not address or not gender:
            messagebox.showwarning("Warning", "All fields are required!")
            return
        
        query = "INSERT INTO students (name, mobile, email, birthday, address, gender) VALUES (%s, %s, %s, %s, %s, %s)"
        result = execute_query(query, (name, mobile, email, birthday, address, gender))
        
        if result is not None:
            messagebox.showinfo("Success", "Student added successfully!")
            load_students()
            add_window.destroy()
    
    Button(add_window, text="Save", font=("Arial", 12), width=18, height=2, bg="#4CAF50", fg="white", command=save_student).pack(pady=18, ipadx=6, ipady=5, padx=100)

def search_student():
    """Search student by ID"""
    if DB_CONNECTION is None or not DB_CONNECTION.is_connected():
        messagebox.showerror("Error", "Not connected to database!")
        return
    
    search_window = Toplevel(window)
    search_window.title("Search Student")
    search_window.geometry("350x150")
    search_window.resizable(False, False)
    
    Label(search_window, text="Enter Student ID:", font=("Arial", 10)).pack(pady=10)
    id_entry = Entry(search_window, width=30, font=("Arial", 10))
    id_entry.pack(pady=10)
    
    def perform_search():
        student_id = id_entry.get().strip()
        if not student_id:
            messagebox.showwarning("Warning", "Please enter Student ID!")
            return
        
        query = "SELECT id, name, mobile, email, birthday, address, gender FROM students WHERE id = %s"
        result = execute_query(query, (student_id,), fetch=True)
        
        if result:
            student = result[0]
            messagebox.showinfo(
                "Found",
                f"ID: {student[0]}\nName: {student[1]}\nMobile: {student[2]}\nEmail: {student[3]}\nBirthday: {student[4]}\nAddress: {student[5]}\nGender: {student[6]}"
            )
        else:
            messagebox.showinfo("Not Found", "Student not found!")
    
    Button(search_window, text="Search", font=("Arial", 10), bg="#2196F3", fg="white", command=perform_search).pack(pady=10)

def delete_student():
    """Delete student by ID"""
    if DB_CONNECTION is None or not DB_CONNECTION.is_connected():
        messagebox.showerror("Error", "Not connected to database!")
        return
    
    selected = table.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a student to delete!")
        return
    
    student_id = table.item(selected[0])['values'][0]
    
    if messagebox.askyesno("Confirm", "Are you sure you want to delete this student?"):
        query = "DELETE FROM students WHERE id = %s"
        result = execute_query(query, (student_id,))
        
        if result is not None and result > 0:
            messagebox.showinfo("Success", "Student deleted successfully!")
            load_students()

def update_student():
    """Update student details"""
    if DB_CONNECTION is None or not DB_CONNECTION.is_connected():
        messagebox.showerror("Error", "Not connected to database!")
        return
    
    selected = table.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a student to update!")
        return
    
    student_data = table.item(selected[0])['values']
    student_id = student_data[0]
    
    update_window = Toplevel(window)
    update_window.title("Update Student")
    update_window.geometry("500x460")
    update_window.resizable(False, False)
    
    Label(update_window, text="Name:", font=("Arial", 10)).pack(pady=5)
    name_entry = Entry(update_window, width=40, font=("Arial", 10))
    name_entry.pack(pady=5)
    name_entry.insert(0, student_data[1])
    
    Label(update_window, text="Mobile No:", font=("Arial", 10)).pack(pady=5)
    mobile_entry = Entry(update_window, width=40, font=("Arial", 10))
    mobile_entry.pack(pady=5)
    mobile_entry.insert(0, student_data[2])
    
    Label(update_window, text="Email:", font=("Arial", 10)).pack(pady=5)
    email_entry = Entry(update_window, width=40, font=("Arial", 10))
    email_entry.pack(pady=5)
    email_entry.insert(0, student_data[3])
    
    Label(update_window, text="Birthday (YYYY-MM-DD):", font=("Arial", 10)).pack(pady=5)
    birthday_entry = Entry(update_window, width=40, font=("Arial", 10))
    birthday_entry.pack(pady=5)
    birthday_entry.insert(0, student_data[4])
    
    Label(update_window, text="Address:", font=("Arial", 10)).pack(pady=5)
    address_entry = Entry(update_window, width=40, font=("Arial", 10))
    address_entry.pack(pady=5)
    address_entry.insert(0, student_data[5])
    
    Label(update_window, text="Gender:", font=("Arial", 10)).pack(pady=5)
    gender_combobox = ttk.Combobox(update_window, values=["Male", "Female"], state="readonly", width=38)
    gender_combobox.pack(pady=5)
    if student_data[6] in ["Male", "Female"]:
        gender_combobox.set(student_data[6])
    else:
        gender_combobox.current(0)
    
    def save_update():
        name = name_entry.get().strip()
        mobile = mobile_entry.get().strip()
        email = email_entry.get().strip()
        birthday = birthday_entry.get().strip()
        address = address_entry.get().strip()
        gender = gender_combobox.get().strip()
        
        if not name or not mobile or not email or not birthday or not address or not gender:
            messagebox.showwarning("Warning", "All fields are required!")
            return
        
        query = "UPDATE students SET name = %s, mobile = %s, email = %s, birthday = %s, address = %s, gender = %s WHERE id = %s"
        result = execute_query(query, (name, mobile, email, birthday, address, gender, student_id))
        
        if result is not None:
            messagebox.showinfo("Success", "Student updated successfully!")
            load_students()
            update_window.destroy()
    
    Button(update_window, text="Update", font=("Arial", 12), width=18, height=2, bg="#FF9800", fg="white", command=save_update).pack(pady=18, ipadx=6, ipady=5, padx=100)

def show_student():
    """Show all students (reload table)"""
    load_students()
    messagebox.showinfo("Success", "All students displayed!")

def export_data():
    """Export student data to CSV"""
    if DB_CONNECTION is None or not DB_CONNECTION.is_connected():
        messagebox.showerror("Error", "Not connected to database!")
        return
    
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    
    if file_path:
        query = "SELECT * FROM students"
        students = execute_query(query, fetch=True)
        
        if students:
            try:
                with open(file_path, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['ID', 'Name', 'Mobile', 'Email', 'Birthday', 'Address', 'Gender'])
                    writer.writerows(students)
                messagebox.showinfo("Success", f"Data exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {e}")
        else:
            messagebox.showwarning("Warning", "No data to export!")

# ============== LEFT SIDEBAR ==============
left_frame = Frame(window, bg="#f0f0f0", width=200)
left_frame.pack(side=LEFT, fill=BOTH, padx=10, pady=10)

# Date and Time Display
date_label = Label(left_frame, text="", font=("Arial", 10, "bold"), bg="#f0f0f0", fg="#4169E1")
date_label.pack(pady=5)

time_label = Label(left_frame, text="", font=("Arial", 10, "bold"), bg="#f0f0f0", fg="#4169E1")
time_label.pack(pady=5)

def update_datetime():
    now = datetime.now()
    date_label.config(text=f"Date: {now.strftime('%d/%m/%Y')}")
    time_label.config(text=f"Time {now.strftime('%H:%M:%S')}")
    window.after(1000, update_datetime)

update_datetime()

# Image Placeholder
img_frame = Frame(left_frame, bg="white", width=120, height=120)
img_frame.pack(pady=10)

try:
    # Try multiple possible paths for the image
    possible_paths = [
        "Frontend/PhotoHouse/students.png",
        "./Frontend/PhotoHouse/students.png",
        os.path.join(os.path.dirname(__file__), "PhotoHouse/students.png"),
    ]
    
    image_loaded = False
    for img_path in possible_paths:
        if os.path.exists(img_path):
            image = Image.open(img_path)
            image = image.resize((120, 120), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            img_label = Label(img_frame, image=photo, bg="white")
            img_label.image = photo
            img_label.pack(expand=True, fill=BOTH, padx=5, pady=5)
            image_loaded = True
            break
    
    if not image_loaded:
        raise FileNotFoundError("Image file not found in any expected location")
except Exception as e:
    img_label = Label(img_frame, text="[Photo Error]", bg="white", font=("Arial", 10), fg="red")
    img_label.pack(expand=True, fill=BOTH, padx=5, pady=5)

# Buttons
button_style = {"font": ("Arial", 10), "bg": "#E8E8E8", "relief": "ridge", "width": 20}

add_btn = Button(left_frame, text="Add Student", **button_style, command=add_student)
add_btn.pack(pady=5)

search_btn = Button(left_frame, text="Search Student", **button_style, command=search_student)
search_btn.pack(pady=5)

delete_btn = Button(left_frame, text="Delete Student", **button_style, command=delete_student)
delete_btn.pack(pady=5)

update_btn = Button(left_frame, text="Update Student", **button_style, command=update_student)
update_btn.pack(pady=5)

show_btn = Button(left_frame, text="Show Student", **button_style, command=show_student)
show_btn.pack(pady=5)

export_btn = Button(left_frame, text="Export Data", **button_style, command=export_data)
export_btn.pack(pady=5)

exit_btn = Button(left_frame, text="Exit", **button_style, command=window.quit)
exit_btn.pack(pady=5)

# ============== RIGHT MAIN AREA ==============
right_frame = Frame(window, bg="white")
right_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

# Top section with title and button
top_frame = Frame(right_frame, bg="white")
top_frame.pack(fill=X, pady=(0, 10))

animated_title_text = "   Student Management System   "
title_label = Label(top_frame, text=animated_title_text, font=("Arial", 24, "bold"), fg="red", bg="white")
title_label.pack(side=LEFT, expand=True)

def animate_title():
    global animated_title_text
    animated_title_text = animated_title_text[1:] + animated_title_text[0]
    title_label.config(text=animated_title_text)
    window.after(180, animate_title)

animate_title()

connect_btn = Button(top_frame, text="Connect To Database", font=("Arial", 10), bg="#D3D3D3", relief="ridge", command=open_connection_window)
connect_btn.pack(side=RIGHT)

# Table
table_frame = Frame(right_frame)
table_frame.pack(fill=BOTH, expand=True)

columns = ("ID", "Name", "Mobile No", "Email", "Birthday", "Address", "Gender")
table = ttk.Treeview(table_frame, columns=columns, height=20)

table.column("#0", width=0, stretch=NO)
table.column("ID", anchor=CENTER, width=80)
table.column("Name", anchor=CENTER, width=180)
table.column("Mobile No", anchor=CENTER, width=120)
table.column("Email", anchor=CENTER, width=220)
table.column("Birthday", anchor=CENTER, width=120)
table.column("Address", anchor=CENTER, width=240)
table.column("Gender", anchor=CENTER, width=80)

table.heading("#0", text="", anchor=CENTER)
table.heading("ID", text="ID", anchor=CENTER)
table.heading("Name", text="Name", anchor=CENTER)
table.heading("Mobile No", text="Mobile No", anchor=CENTER)
table.heading("Email", text="Email", anchor=CENTER)
table.heading("Birthday", text="Birthday", anchor=CENTER)
table.heading("Address", text="Address", anchor=CENTER)
table.heading("Gender", text="Gender", anchor=CENTER)

# Add scrollbar
scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=table.yview)
scrollbar.pack(side=RIGHT, fill=Y)
table.configure(yscroll=scrollbar.set)
table.pack(fill=BOTH, expand=True)

window.mainloop()   