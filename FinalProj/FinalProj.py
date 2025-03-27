import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog

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

    tk.Label(signup_window, text="First Name:").grid(row=0, column=0)
    first_name = tk.Entry(signup_window)
    first_name.grid(row=0, column=1)
    
    tk.Label(signup_window, text="Middle Name:").grid(row=1, column=0)
    middle_name = tk.Entry(signup_window)
    middle_name.grid(row=1, column=1)
    
    tk.Label(signup_window, text="Last Name:").grid(row=2, column=0)
    last_name = tk.Entry(signup_window)
    last_name.grid(row=2, column=1)
    
    tk.Label(signup_window, text="Birthday (YYYY-MM-DD):").grid(row=3, column=0)
    birth_date = tk.Entry(signup_window)
    birth_date.grid(row=3, column=1)
    
    tk.Label(signup_window, text="Gender:").grid(row=4, column=0)
    gender_var = tk.StringVar(value="Other")
    tk.OptionMenu(signup_window, gender_var, "Male", "Female", "Other").grid(row=4, column=1)
    
    tk.Label(signup_window, text="Username:").grid(row=5, column=0)
    user_name = tk.Entry(signup_window)
    user_name.grid(row=5, column=1)
    
    tk.Label(signup_window, text="Password:").grid(row=6, column=0)
    pass_word = tk.Entry(signup_window, show="*")
    pass_word.grid(row=6, column=1)
    
    tk.Button(signup_window, text="Sign Up", command=save_user).grid(row=7, columnspan=2)

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

# Main menu
def open_main_menu(user_id):
    menu_window = tk.Toplevel(root)
    menu_window.title("Password Manager")
    
    tk.Button(menu_window, text="Add Password", command=lambda: add_password(user_id)).pack()
    tk.Button(menu_window, text="View All Passwords", command=lambda: view_passwords(user_id)).pack()
    tk.Button(menu_window, text="Search Password", command=lambda: search_password(user_id)).pack()
    tk.Button(menu_window, text="Edit Password", command=lambda: edit_password(user_id)).pack()
    tk.Button(menu_window, text="Delete Password", command=lambda: delete_password(user_id)).pack()
    tk.Button(menu_window, text="Exit", command=menu_window.destroy).pack()

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

# GUI setup
root = tk.Tk()
root.title("Password Manager")

tk.Button(root, text="Login", command=login).pack()
tk.Button(root, text="Sign Up", command=sign_up).pack()
tk.Button(root, text="Exit", command=root.quit).pack()

init_db()
root.mainloop()
