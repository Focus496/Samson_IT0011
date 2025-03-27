import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# Database setup
def init_db():
    conn = sqlite3.connect("password_manager.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            middle_name TEXT,
            last_name TEXT,
            birthday TEXT,
            gender TEXT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            site TEXT,
            username TEXT,
            password TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

# Sign-up function
def sign_up():
    def save_user():
        first = first_name.get()
        middle = middle_name.get()
        last = last_name.get()
        birthday = birth_date.get()
        gender = gender_var.get()
        username = user_name.get()
        password = pass_word.get()

        if not (first and last and birthday and username and password):
            messagebox.showerror("Error", "All fields except middle name must be filled")
            return

        try:
            conn = sqlite3.connect("password_manager.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (first_name, middle_name, last_name, birthday, gender, username, password) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (first, middle, last, birthday, gender, username, password))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Account created successfully!")
            signup_window.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")

    signup_window = tk.Toplevel(root)
    signup_window.title("Sign Up")
    signup_window.geometry("400x450")
    
    ttk.Label(signup_window, text="First Name:").pack(pady=2)
    first_name = ttk.Entry(signup_window)
    first_name.pack(pady=2)
    
    ttk.Label(signup_window, text="Middle Name:").pack(pady=2)
    middle_name = ttk.Entry(signup_window)
    middle_name.pack(pady=2)
    
    ttk.Label(signup_window, text="Last Name:").pack(pady=2)
    last_name = ttk.Entry(signup_window)
    last_name.pack(pady=2)
    
    ttk.Label(signup_window, text="Birthday (YYYY-MM-DD):").pack(pady=2)
    birth_date = ttk.Entry(signup_window)
    birth_date.pack(pady=2)
    
    ttk.Label(signup_window, text="Gender:").pack(pady=2)
    gender_var = tk.StringVar(value="Other")
    gender_menu = ttk.Combobox(signup_window, textvariable=gender_var, values=("Male", "Female", "Other"))
    gender_menu.pack(pady=2)
    
    ttk.Label(signup_window, text="Username:").pack(pady=2)
    user_name = ttk.Entry(signup_window)
    user_name.pack(pady=2)
    
    ttk.Label(signup_window, text="Password:").pack(pady=2)
    pass_word = ttk.Entry(signup_window, show="*")
    pass_word.pack(pady=2)
    
    ttk.Button(signup_window, text="Sign Up", command=save_user).pack(pady=10)

# Login function
def login():
    username = simpledialog.askstring("Login", "Enter Username:")
    password = simpledialog.askstring("Login", "Enter Password:", show="*")
    
    conn = sqlite3.connect("password_manager.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        messagebox.showinfo("Success", "Login successful!")
        open_main_menu(user[0])
    else:
        messagebox.showerror("Error", "Invalid credentials!")
# Adding a new password
def add_password(user_id):
    site = simpledialog.askstring("Add Password", "Enter Website:")
    username = simpledialog.askstring("Add Password", "Enter Username:")
    password = simpledialog.askstring("Add Password", "Enter Password:")
    if site and username and password:
        conn = sqlite3.connect("password_manager.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO passwords (user_id, site, username, password) VALUES (?, ?, ?, ?)",
                       (user_id, site, username, password))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Password saved!")
    else:
        messagebox.showerror("Error", "All fields are required!")

# Viewing all passwords
def view_passwords(user_id):
    conn = sqlite3.connect("password_manager.db")
    cursor = conn.cursor()
    cursor.execute("SELECT site, username, password FROM passwords WHERE user_id = ?", (user_id,))
    records = cursor.fetchall()
    conn.close()
    output = "\n".join([f"{r[0]} - {r[1]}: {r[2]}" for r in records]) or "No passwords found."
    messagebox.showinfo("Stored Passwords", output)

# Searching for a password
def search_password(user_id):
    site = simpledialog.askstring("Search Password", "Enter Website:")
    conn = sqlite3.connect("password_manager.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, password FROM passwords WHERE user_id = ? AND site = ?", (user_id, site))
    record = cursor.fetchone()
    conn.close()
    if record:
        messagebox.showinfo("Password Found", f"Username: {record[0]}\nPassword: {record[1]}")
    else:
        messagebox.showerror("Error", "No password found for this site.")

# Edit password
def edit_password(user_id):
    site = simpledialog.askstring("Edit Password", "Enter Website:")
    if not site:
        return
    
    conn = sqlite3.connect("password_manager.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, password FROM passwords WHERE user_id = ? AND site = ?", (user_id, site))
    record = cursor.fetchone()
    
    if not record:
        messagebox.showerror("Error", "No password found for this site.")
        conn.close()
        return
    
    new_password = simpledialog.askstring("Edit Password", "Enter New Password:", show="*")
    if not new_password:
        return
    
    cursor.execute("UPDATE passwords SET password = ? WHERE user_id = ? AND site = ?", (new_password, user_id, site))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Password updated successfully!")

# Delete password
def delete_password(user_id):
    site = simpledialog.askstring("Delete Password", "Enter Website:")
    if not site:
        return
    
    conn = sqlite3.connect("password_manager.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM passwords WHERE user_id = ? AND site = ?", (user_id, site))
    record = cursor.fetchone()
    
    if not record:
        messagebox.showerror("Error", "No password found for this site.")
        conn.close()
        return
    
    confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this password?")
    if confirm:
        cursor.execute("DELETE FROM passwords WHERE user_id = ? AND site = ?", (user_id, site))
        conn.commit()
        messagebox.showinfo("Success", "Password deleted successfully!")
    
    conn.close()

# Main menu
def open_main_menu(user_id):
    menu_window = tk.Toplevel(root)
    menu_window.title("Password Manager")
    menu_window.geometry("400x400")
    
    ttk.Label(menu_window, text="Password Manager", font=("Arial", 14, "bold")).pack(pady=10)
    ttk.Button(menu_window, text="Add Password", command=lambda: add_password(user_id)).pack(pady=5)
    ttk.Button(menu_window, text="View All Passwords", command=lambda: view_passwords(user_id)).pack(pady=5)
    ttk.Button(menu_window, text="Search Password", command=lambda: search_password(user_id)).pack(pady=5)
    ttk.Button(menu_window, text="Edit Password", command=lambda: edit_password(user_id)).pack(pady=5)
    ttk.Button(menu_window, text="Delete Password", command=lambda: delete_password(user_id)).pack(pady=5)
    ttk.Button(menu_window, text="Exit", command=menu_window.destroy).pack(pady=10)

# GUI setup
root = tk.Tk()
root.title("Password Manager")
root.geometry("400x300")

ttk.Label(root, text="Welcome to Password Manager", font=("Arial", 12, "bold")).pack(pady=10)
ttk.Button(root, text="Login", command=login).pack(pady=5)
ttk.Button(root, text="Sign Up", command=sign_up).pack(pady=5)
ttk.Button(root, text="Exit", command=root.quit).pack(pady=10)

init_db()
root.mainloop()
