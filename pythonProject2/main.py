import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

# File to store user credentials
CREDENTIALS_FILE = "credentials.json"

# Dictionary to store students and grades
students_data = {}

# Load credentials from file
def load_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                pass  # If file is corrupted, return empty dict
    return {}

# Save credentials to file
def save_credentials(credentials):
    with open(CREDENTIALS_FILE, "w") as file:
        json.dump(credentials, file, indent=4)

# Load student data from file
def load_from_file():
    try:
        with open("student_records.json", "r") as file:
            global students_data
            students_data = json.load(file)
    except FileNotFoundError:
        pass
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load data: {e}")

# Save student data to file
def save_to_file():
    if students_data:
        try:
            with open("student_records.json", "w") as file:
                json.dump(students_data, file, indent=4)
            messagebox.showinfo("Success", "Data saved to student_records.json")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")
    else:
        messagebox.showinfo("Save Data", "No data to save.")

# Initialize credentials
credentials = load_credentials()

# Default admin and teacher accounts
if "admin" not in credentials:
    credentials["admin"] = "admin"
if "teacher1" not in credentials:
    credentials["teacher1"] = "teacher123"
save_credentials(credentials)

def teacher_dashboard(root):
    root.destroy()  # Close the current window
    print("Opening Teacher Dashboard...")  # Debug message

    teacher_window = tk.Tk()
    teacher_window.title("Teacher Dashboard")
    teacher_window.geometry("800x600")

    # Left menu frame
    menu_frame = tk.Frame(teacher_window, bg="lightgray", width=200)
    menu_frame.pack(side="left", fill="y")

    # Content frame
    content_frame = tk.Frame(teacher_window, bg="lightblue")
    content_frame.pack(side="right", expand=True, fill="both")

    def load_add_student():
        for widget in content_frame.winfo_children():
            widget.destroy()
        tk.Label(content_frame, text="Add Student", font=("Helvetica", 16), bg="lightblue").pack(pady=20)

        tk.Label(content_frame, text="Student Name:", bg="lightblue", anchor="w").pack(pady=5)
        student_name_entry = tk.Entry(content_frame, width=30)
        student_name_entry.pack(pady=5)

        tk.Label(content_frame, text="Subject:", bg="lightblue", anchor="w").pack(pady=5)
        subject_entry = tk.Entry(content_frame, width=30)
        subject_entry.pack(pady=5)

        tk.Label(content_frame, text="Grade (0-10):", bg="lightblue", anchor="w").pack(pady=5)
        grade_entry = tk.Entry(content_frame, width=30)
        grade_entry.pack(pady=5)

        def save_student():
            student_name = student_name_entry.get()
            subject = subject_entry.get()
            try:
                grade = int(grade_entry.get())
                if not (0 <= grade <= 10):
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Grade must be an integer between 0 and 10.")
                return

            if student_name and subject:
                if student_name not in students_data:
                    students_data[student_name] = {}
                if subject not in students_data[student_name]:
                    students_data[student_name][subject] = []
                students_data[student_name][subject].append(grade)
                messagebox.showinfo("Success", f"Added {student_name} with grade {grade} in {subject}.")
            else:
                messagebox.showerror("Error", "Student name and subject are required.")

        tk.Button(content_frame, text="Save", command=save_student, bg="green", fg="white", width=15).pack(pady=10)

    def load_view_students():
        for widget in content_frame.winfo_children():
            widget.destroy()
        tk.Label(content_frame, text="View Students", font=("Helvetica", 16), bg="lightblue").pack(pady=20)

        students_text = tk.Text(content_frame, wrap="word", width=70, height=20)
        students_text.pack(pady=10)

        details = ""
        for student, subjects in students_data.items():
            details += f"{student}:\n"
            for subject, grades in subjects.items():
                grades_str = ', '.join(map(str, grades))
                details += f"  {subject}: {grades_str}\n"

        students_text.insert("1.0", details if details else "No student records available.")
        students_text.config(state="disabled")

    def load_delete_student():
        for widget in content_frame.winfo_children():
            widget.destroy()
        tk.Label(content_frame, text="Delete Student", font=("Helvetica", 16), bg="lightblue").pack(pady=20)

        tk.Label(content_frame, text="Student Name:", bg="lightblue", anchor="w").pack(pady=5)
        student_name_entry = tk.Entry(content_frame, width=30)
        student_name_entry.pack(pady=5)

        def delete_student():
            student_name = student_name_entry.get()
            if student_name in students_data:
                del students_data[student_name]
                messagebox.showinfo("Success", f"Deleted record for {student_name}.")
            else:
                messagebox.showerror("Error", "Student not found.")

        tk.Button(content_frame, text="Delete", command=delete_student, bg="red", fg="white", width=15).pack(pady=10)

    def load_add_grade():
        for widget in content_frame.winfo_children():
            widget.destroy()
        tk.Label(content_frame, text="Add Grade", font=("Helvetica", 16), bg="lightblue").pack(pady=20)

        tk.Label(content_frame, text="Student Name:", bg="lightblue", anchor="w").pack(pady=5)
        student_name_entry = tk.Entry(content_frame, width=30)
        student_name_entry.pack(pady=5)

        tk.Label(content_frame, text="Subject:", bg="lightblue", anchor="w").pack(pady=5)
        subject_entry = tk.Entry(content_frame, width=30)
        subject_entry.pack(pady=5)

        tk.Label(content_frame, text="Grade (0-10):", bg="lightblue", anchor="w").pack(pady=5)
        grade_entry = tk.Entry(content_frame, width=30)
        grade_entry.pack(pady=5)

        def add_grade():
            student_name = student_name_entry.get()
            subject = subject_entry.get()
            try:
                grade = int(grade_entry.get())
                if not (0 <= grade <= 10):
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Grade must be an integer between 0 and 10.")
                return

            if student_name in students_data:
                if subject not in students_data[student_name]:
                    students_data[student_name][subject] = []
                students_data[student_name][subject].append(grade)
                messagebox.showinfo("Success", f"Added grade {grade} for {student_name} in {subject}.")
            else:
                messagebox.showerror("Error", "Student not found.")

        tk.Button(content_frame, text="Add", command=add_grade, bg="green", fg="white", width=15).pack(pady=10)

    def load_delete_grade():
        for widget in content_frame.winfo_children():
            widget.destroy()
        tk.Label(content_frame, text="Delete Grade", font=("Helvetica", 16), bg="lightblue").pack(pady=20)

        tk.Label(content_frame, text="Student Name:", bg="lightblue", anchor="w").pack(pady=5)
        student_name_entry = tk.Entry(content_frame, width=30)
        student_name_entry.pack(pady=5)

        tk.Label(content_frame, text="Subject:", bg="lightblue", anchor="w").pack(pady=5)
        subject_entry = tk.Entry(content_frame, width=30)
        subject_entry.pack(pady=5)

        tk.Label(content_frame, text="Grade (to delete):", bg="lightblue", anchor="w").pack(pady=5)
        grade_entry = tk.Entry(content_frame, width=30)
        grade_entry.pack(pady=5)

        def delete_grade():
            student_name = student_name_entry.get()
            subject = subject_entry.get()
            try:
                grade = int(grade_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Grade must be an integer.")
                return

            if student_name in students_data and subject in students_data[student_name]:
                if grade in students_data[student_name][subject]:
                    students_data[student_name][subject].remove(grade)
                    messagebox.showinfo("Success", f"Removed grade {grade} for {student_name} in {subject}.")
                else:
                    messagebox.showerror("Error", "Grade not found.")
            else:
                messagebox.showerror("Error", "Student or subject not found.")

        tk.Button(content_frame, text="Delete", command=delete_grade, bg="red", fg="white", width=15).pack(pady=10)

    menu_buttons = [
        ("Add Student", load_add_student),
        ("View Students", load_view_students),
        ("Delete Student", load_delete_student),
        ("Add Grade", load_add_grade),
        ("Delete Grade", load_delete_grade),
        ("Save Data", save_to_file),
        ("Exit", teacher_window.destroy),
    ]

    for text, command in menu_buttons:
        tk.Button(menu_frame, text=text, command=command, bg="white", fg="black", width=20, pady=5, relief="solid",
                  borderwidth=1).pack(pady=5)

    teacher_window.mainloop()

def login(root):
    def verify_credentials():
        username = username_entry.get()
        password = password_entry.get()

        print(f"Login attempt: {username}")  # Debug message

        if username in credentials and credentials[username] == password:
            print("Login successful.")  # Debug message
            if username == "admin":
                admin_dashboard(root)
            else:
                teacher_dashboard(root)
        else:
            print("Login failed.")  # Debug message
            messagebox.showerror("Login Failed", "Invalid username or password")

    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.geometry("300x200")
    login_window.configure(bg="lightblue")

    tk.Label(login_window, text="Login", font=("Helvetica", 16, "bold"), bg="lightblue").pack(pady=10)

    tk.Label(login_window, text="Username:", bg="lightblue").pack(anchor="w", padx=20)
    username_entry = tk.Entry(login_window)
    username_entry.pack(padx=20, pady=5)

    tk.Label(login_window, text="Password:", bg="lightblue").pack(anchor="w", padx=20)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(padx=20, pady=5)

    tk.Button(login_window, text="Login", command=verify_credentials, width=15).pack(pady=10)

def admin_dashboard(root):
    root.destroy()  # Close current window
    admin_window = tk.Tk()
    admin_window.title("Admin Dashboard")
    admin_window.geometry("800x600")
    tk.Label(admin_window, text="Admin Dashboard", font=("Helvetica", 18), bg="lightblue", pady=10).pack(fill=tk.X)

    def register_teacher():
        username = simpledialog.askstring("Register Teacher", "Enter new teacher username:")
        password = simpledialog.askstring("Register Teacher", "Enter password for the teacher:")
        if username and password:
            if username in credentials:
                messagebox.showerror("Error", "Teacher already exists.")
            else:
                credentials[username] = password
                save_credentials(credentials)
                messagebox.showinfo("Success", f"Teacher {username} registered successfully.")
        else:
            messagebox.showerror("Error", "Username and password cannot be empty.")

    def register_student():
        student_name = simpledialog.askstring("Register Student", "Enter student name:")
        if student_name:
            if student_name in students_data:
                messagebox.showerror("Error", "Student already exists.")
            else:
                students_data[student_name] = {}
                save_to_file()
                messagebox.showinfo("Success", f"Student {student_name} registered successfully.")
        else:
            messagebox.showerror("Error", "Student name cannot be empty.")

    tk.Button(admin_window, text="Register Teacher", command=register_teacher, bg="green", fg="white", width=20).pack(
        pady=10)
    tk.Button(admin_window, text="Register Student", command=register_student, bg="blue", fg="white", width=20).pack(
        pady=10)
    tk.Button(admin_window, text="Exit", command=admin_window.destroy, bg="red", fg="white", width=20).pack(pady=20)
    admin_window.mainloop()

def main_app():
    load_from_file()

    app = tk.Tk()
    app.title("Student Rating System")

    tk.Label(app, text="VIKO Student Rating Platform", font=("Helvetica", 18, "bold"), bg="lightblue",
             pady=10).pack(fill=tk.X)

    tk.Button(app, text="Login", command=lambda: login(app), width=25).pack(pady=10)
    tk.Button(app, text="Exit", command=app.destroy, width=25, bg="red", fg="white").pack(pady=10)

    app.mainloop()

if __name__ == "__main__":
    main_app()
