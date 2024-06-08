from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, Radiobutton, StringVar, messagebox, Checkbutton, BooleanVar
import secrets
import hashlib
import sqlite3
import re

conn = sqlite3.connect('accounts.db')
cursor = conn.cursor()

OUTPUT_PATH = Path(__file__).parent
# ASSETS_PATH = OUTPUT_PATH / Path(r"C:/Users/TIPQC/Downloads/SE_proj-main/assets/Registration")
ASSETS_PATH = OUTPUT_PATH / Path(r"C:/Users/katsu/Documents/GitHub/SE_proj/assets/Registration")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def generate_salt():
    return secrets.token_hex(16)

def hash_password(password, salt):
    return hashlib.sha256((password + salt).encode()).hexdigest()

def hash_username(username):
    return hashlib.sha256(username.encode()).hexdigest()

def save_password(username, password, loa, email):
    salt = generate_salt()
    hashed_password = hash_password(password, salt)
    hashed_username = hash_username(username)

    cursor.execute("INSERT INTO accounts (username, salt, hashed_password, Loa, email) VALUES (?,?,?,?,?)",
                   (hashed_username, salt, hashed_password, loa, email))
    conn.commit()

def is_valid_username(username):
    if not 6 <= len(username) <= 20:
        return False, "Username must be between 6 and 20 characters"
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        return False, "Username can only contain letters, numbers, dashes, and underscores"
    return True, ""

def is_valid_email(email):
    if len(email) > 320:
        return False, "Email must not exceed 320 characters"
    email_regex = r'^[a-zA-Z0-9._%+-]{1,64}@[a-zA-Z0-9.-]{1,255}\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        return False, "Invalid email format"
    return True, ""

def is_valid_password(password):
    if len(password) < 10:
        return False, "Password must be at least 10 characters long"

    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one numeric character"
    if not re.search(r'[~`!@#$%^&*()\-_=+{}\[\]\\|;:"<>,./?]', password):
        return False, "Password must contain at least one special character"

    return True, ""

def register_user(username, password, confirm_password, loa, email):
    valid_username, username_message = is_valid_username(username)
    if not username or not password or not email:
        messagebox.showerror("Error", "All fields are required")
        return

    if not valid_username:
        messagebox.showerror("Error", username_message)
        return

    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match")
        return

    valid_email, email_message = is_valid_email(email)
    if not valid_email:
        messagebox.showerror("Error", email_message)
        return

    valid_password, password_message = is_valid_password(password)
    if not valid_password:
        messagebox.showerror("Error", password_message)
        return

    hashed_username = hash_username(username)
    cursor.execute("SELECT * FROM accounts WHERE username = ?", (hashed_username,))
    if cursor.fetchone():
        messagebox.showerror("Error", "Username already exists")
        return

    cursor.execute("SELECT * FROM accounts WHERE email = ?", (email,))
    if cursor.fetchone():
        messagebox.showerror("Error", "Email already exists")
        return

    save_password(username, password, loa, email)
    messagebox.showinfo("Success", "Registration successful")

def create_registration_window():
    window = Tk()
    window.title("Registration")
    window.geometry("600x550")
    window.configure(bg="#FFE1C6")

    window_width, window_height = 600, 650
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    canvas = Canvas(
        window,
        bg="#FFE1C6",
        height=550,
        width=600,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    user_entry_image = PhotoImage(file=relative_to_assets("entry_2.png"))
    user_entry_bg = canvas.create_image(300.5, 182.0, image=user_entry_image)
    user_entry = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        font=("Hanuman Regular", 24 * -1)
    )
    user_entry.place(x=119.0, y=163.0, width=363.0, height=36.0)

    canvas.create_text(119.0, 139.0, anchor="nw", text="Username", fill="#000000", font=("Hanuman Regular", 16 * -1))

    email_entry_image = PhotoImage(file=relative_to_assets("entry_4.png"))
    email_entry_bg = canvas.create_image(300.5, 247.0, image=email_entry_image)
    email_entry = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        font=("Hanuman Regular", 24 * -1)
    )
    email_entry.place(x=119.0, y=228.0, width=363.0, height=36.0)

    canvas.create_text(119.0, 204.0, anchor="nw", text="Email", fill="#000000", font=("Hanuman Regular", 16 * -1))

    pass_entry_image = PhotoImage(file=relative_to_assets("entry_1.png"))
    pass_entry_bg = canvas.create_image(300.5, 312.0, image=pass_entry_image)
    pass_entry = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        font=("Hanuman Regular", 24 * -1),
        show="*"
    )
    pass_entry.place(x=119.0, y=293.0, width=363.0, height=36.0)

    canvas.create_text(119.0, 269.0, anchor="nw", text="Password", fill="#000000", font=("Hanuman Regular", 16 * -1))

    confirm_pass_entry_image = PhotoImage(file=relative_to_assets("entry_3.png"))
    confirm_pass_entry_bg = canvas.create_image(300.5, 377.0, image=confirm_pass_entry_image)
    confirm_pass_entry = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        font=("Hanuman Regular", 24 * -1),
        show="*"
    )
    confirm_pass_entry.place(x=119.0, y=358.0, width=363.0, height=36.0)

    canvas.create_text(119.0, 334.0, anchor="nw", text="Confirm Password", fill="#000000", font=("Hanuman Regular", 16 * -1))

    show_password_var = BooleanVar()

    def toggle_password_visibility():
        if show_password_var.get():
            pass_entry.config(show="")
            confirm_pass_entry.config(show="")
        else:
            pass_entry.config(show="*")
            confirm_pass_entry.config(show="*")

    show_password_checkbox = Checkbutton(
        window,
        text="Show Password",
        variable=show_password_var,
        bg="#FFE1C6",
        font=("Hanuman Regular", 10),
        command=toggle_password_visibility
    )
    show_password_checkbox.place(x=359.0, y=398.0)

    canvas.create_text(119.0, 423.0, anchor="nw", text="Level of Access", fill="#000000", font=("Hanuman Regular", 16 * -1))

    loa_var = StringVar(value="employee")

    radio_admin = Radiobutton(
        window,
        text="Admin",
        variable=loa_var,
        value="admin",
        bg="#FFE1C6",
        font=("Hanuman Regular", 14 * -1)
    )
    radio_admin.place(x=119.0, y=443.0)

    radio_employee = Radiobutton(
        window,
        text="Employee/Staff",
        variable=loa_var,
        value="employee",
        bg="#FFE1C6",
        font=("Hanuman Regular", 14 * -1)
    )
    radio_employee.place(x=119.0, y=463.0)

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: back_to_menu_ad(window),
        relief="flat"
    )
    button_1.place(x=349.0, y=520.0, width=133.0, height=37.0)

    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: register_user(user_entry.get(), pass_entry.get(), confirm_pass_entry.get(), loa_var.get(), email_entry.get()),
        relief="flat"
    )
    button_2.place(x=119.0, y=520.0, width=133.0, height=37.0)

    canvas.create_rectangle(161.0, 44.0, 439.0, 108.0, fill="#FB7373", outline="")
    canvas.create_text(207.0, 52.0, anchor="nw", text="Registration", fill="#FFFFFF", font=("Hanuman Regular", 32 * -1))

    window.resizable(False, False)
    window.mainloop()

def back_to_menu_ad(window):
    window.destroy()
    from menu_ad import create_menu_ad_window
    create_menu_ad_window()

if __name__ == "__main__":
    create_registration_window()

