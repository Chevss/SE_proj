# Libraries
import hashlib
# import os
import re
import secrets
import smtplib
import sqlite3
from datetime import datetime
from email.mime.text import MIMEText
from pathlib import Path
from tkinter import Button, Canvas, Entry, messagebox, OptionMenu, PhotoImage, Radiobutton, StringVar, Tk
from database import create_database
from user_logs import log_actions


create_database()

# Database connection
conn = sqlite3.connect('Trimark_construction_supply.db')
cursor = conn.cursor()

# Paths
OUTPUT_PATH = Path(__file__).parent
# ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\katsu\Documents\GitHUb\SE_proj\assets\Registration")
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\TIPQC\Desktop\se\assets\Registration")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Using hash to protect the confidentiality of passwords.
def generate_salt():
    return secrets.token_hex(16)


def hash_password(password, salt):
    return hashlib.sha256((password + salt).encode()).hexdigest()

# Send email containing the generated username from registration inputs and random generated password.
def send_email(email, username, password):
    msg = MIMEText(f"Your username is: {username}\nYour temporary password is: {password}")
    msg['Subject'] = 'Registration Details'
    msg['From'] = 'trimarkcstest@outlook.com'
    msg['To'] = email

    with smtplib.SMTP('smtp-mail.outlook.com', 587) as server:
        server.starttls()
        server.login('trimarkcstest@outlook.com', '1ZipJM2DsVnRoBkmVVKRCm0e8c6NniwhjW1FEWEC8n5Y')
        server.sendmail('trimarkcstest@outlook.com', email, msg.as_string())

# Store the registered employee or admin to the database.
def save_user(loa, first_name, last_name, mi, suffix, contact_number, home_address, email, username, password):
    salt = generate_salt()
    hashed_password = hash_password(password, salt)
    date_registered = datetime.now()

    try:
        cursor.execute('''
        INSERT INTO accounts (LOA, First_Name, Last_Name, MI, Suffix, Contact_No, Address, Email, Username, Password, Salt, Date_Registered)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (loa, first_name, last_name, mi, suffix, contact_number, home_address, email, username, hashed_password, salt, date_registered))
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Failed to save user: {str(e)}")
        conn.rollback()

# Generate username like how TIP does but not exactly.
def generate_username(first_name, mi, last_name, suffix, loa):
    prefix = 'a' if loa == 'admin' else 'e'
    first_name_initials = ''.join([name[0].lower() for name in first_name.split()])
    mi_part = mi.lower() if mi else ''
    suffix_part = suffix.lower() if suffix else ''
    return f"{prefix}{first_name_initials}{mi_part}{last_name.lower()}{suffix_part}.tmcs"

# Register user
def register_user(first_name, mi, last_name, suffix, contact_number, home_address, email, loa):
    if not first_name or not last_name or not contact_number or not home_address or not email:
        messagebox.showerror("Error", "All fields except Middle Initial and Suffix are required")
        return False

    if not is_valid_name(first_name):
        messagebox.showerror("Error", "First name can only contain letters")
        return False

    if not is_valid_name(last_name):
        messagebox.showerror("Error", "Last name can only contain letters")
        return False

    if not is_valid_mi(mi):
        messagebox.showerror("Error", "Middle Initial can only contain up to 2 letters")
        return False

    if not is_valid_contact_number(contact_number):
        messagebox.showerror("Error", "Contact number must be 11 digits long and contain only numbers")
        return False

    valid_email, email_message = is_valid_email(email)
    if not valid_email:
        messagebox.showerror("Error", email_message)
        return False

    username = generate_username(first_name, mi, last_name, suffix, loa)

    cursor.execute("SELECT * FROM accounts WHERE Username = ?", (username,))
    if cursor.fetchone():
        messagebox.showerror("Error", "Username already exists")
        return False

    cursor.execute("SELECT * FROM accounts WHERE Email = ?", (email,))
    if cursor.fetchone():
        messagebox.showerror("Error", "Email already exists")
        return False

    password = secrets.token_urlsafe(10)

    save_user(loa, first_name, last_name, mi, suffix, contact_number, home_address, email, username, password)
    send_email(email, username, password)

    log_actions(username, action = "Registered a user.")

    messagebox.showinfo("Success", "Registration successful. Your username and temporary password have been sent to your email.")
    return True

# Functions to check if the inputs are valid.
def is_valid_name(name):
    return bool(re.match(r'^[a-zA-Z ]+$', name))

def is_valid_mi(mi):
    return len(mi) <= 2 and bool(re.match(r'^[a-zA-Z]*$', mi))

def is_valid_contact_number(contact_number):
    return bool(re.match(r'^\d{11}$', contact_number))

def is_valid_email(email):
    if len(email) > 320:
        return False, "Email must not exceed 320 characters"
    email_regex = r'^[a-zA-Z0-9._%+-]{1,64}@[a-zA-Z0-9.-]{1,255}\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        return False, "Invalid email format"
    return True, ""

# Registration window
def create_registration_window():
    window = Tk()
    window.title("Registration")
    window.configure(bg="#FFE1C6")

    window_width, window_height = 600, 750
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    canvas = Canvas(window, bg="#FFE1C6", height=750, width=600, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    # Image loading
    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
    entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
    entry_image_4 = PhotoImage(file=relative_to_assets("entry_4.png"))
    entry_image_5 = PhotoImage(file=relative_to_assets("entry_5.png"))
    entry_image_6 = PhotoImage(file=relative_to_assets("entry_6.png"))
    entry_image_7 = PhotoImage(file=relative_to_assets("entry_7.png"))
    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png")) # back btn
    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png")) # register btn

    # Background creation
    entry_bg_1 = canvas.create_image(272.5, 144.0, image=entry_image_1) # fn
    entry_bg_2 = canvas.create_image(461.5, 144.0, image=entry_image_2) # mi
    entry_bg_3 = canvas.create_image(272.5, 209.0, image=entry_image_3) # ln
    entry_bg_4 = canvas.create_image(461.5, 209.0, image=entry_image_4) # suffix
    entry_bg_5 = canvas.create_image(300.5, 275.0, image=entry_image_5) # contact
    entry_bg_6 = canvas.create_image(300.5, 341.0, image=entry_image_6) # address
    entry_bg_7 = canvas.create_image(300.5, 403.0, image=entry_image_7) # email

    # Labels
    canvas.create_text(119.0, 98.0, anchor="nw", text="First Name", fill="#000000", font=("Hanuman Regular", 16 * -1))
    canvas.create_text(447.0, 98.0, anchor="nw", text="M.I.", fill="#000000", font=("Hanuman Regular", 16 * -1))
    canvas.create_text(119.0, 166.0, anchor="nw", text="Last Name", fill="#000000", font=("Hanuman Regular", 16 * -1))
    canvas.create_text(439.0, 166.0, anchor="nw", text="Suffix", fill="#000000", font=("Hanuman Regular", 16 * -1))
    canvas.create_text(119.0, 232.0, anchor="nw", text="Contact Number", fill="#000000", font=("Hanuman Regular", 16 * -1))
    canvas.create_text(119.0, 298.0, anchor="nw", text="Home Address", fill="#000000", font=("Hanuman Regular", 16 * -1))
    canvas.create_text(119.0, 360.0, anchor="nw", text="Email Address", fill="#000000", font=("Hanuman Regular", 16 * -1))
    canvas.create_text(119.0, 437.0, anchor="nw", text="Level of Access", fill="#000000", font=("Hanuman Regular", 16 * -1))

    # First name
    first_name_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Hanuman Regular", 20 * -1))
    first_name_entry.place(x=119.0, y=125.0, width=307.0, height=36.0)
    
    # Middle initial    
    mi_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Hanuman Regular", 20 * -1))
    mi_entry.place(x=441.0, y=125.0, width=41.0, height=36.0)
    
    # Last name
    last_name_entry = Entry( bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Hanuman Regular", 20 * -1))
    last_name_entry.place(x=119.0, y=190.0, width=307.0, height=36.0)

    # Suffix
    suffix_entry = StringVar()
    suffix_options = ["", "Jr", "Sr", "I", "II", "III"]
    suffix_menu = OptionMenu(window, suffix_entry, *suffix_options)
    suffix_menu.config(bg="#FFE1C6", font=("Hanuman Regular", 14 * -1))
    suffix_menu.place(x=441.0, y=190.0, width=41.0, height=36.0)

    # Contact number    
    contact_no_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Hanuman Regular", 20 * -1))
    contact_no_entry.place(x=119.0, y=256.0, width=363.0, height=36.0)

    # Address
    address_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Hanuman Regular", 20 * -1))
    address_entry.place(x=119.0, y=322.0, width=363.0, height=36.0)

    # Email address
    email_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Hanuman Regular", 20 * -1))
    email_entry.place(x=119.0, y=384.0, width=363.0, height=36.0)
    
    # LOA
    loa_var = StringVar(value="employee")

    radio_admin = Radiobutton(window, text="Admin", variable=loa_var, value="admin", bg="#FFE1C6", font=("Hanuman Regular", 14 * -1))
    radio_admin.place(x=145.0, y=464.0)

    radio_employee = Radiobutton(window, text="Employee/Staff", variable=loa_var, value="employee", bg="#FFE1C6", font=("Hanuman Regular", 14 * -1))
    radio_employee.place(x=145.0, y=495.0)

    def clear_entries():
        first_name_entry.delete(0, 'end')
        mi_entry.delete(0, 'end')
        last_name_entry.delete(0, 'end')
        contact_no_entry.delete(0, 'end')
        address_entry.delete(0, 'end')
        email_entry.delete(0, 'end')
        loa_var.set('employee')

    def attempt_registration():
        success = register_user(
            first_name_entry.get(), 
            mi_entry.get(), 
            last_name_entry.get(), 
            suffix_entry.get(), 
            contact_no_entry.get(), 
            address_entry.get(), 
            email_entry.get(), 
            loa_var.get()
        )
        if success:
            clear_entries()

    # Register button
    register_button = Button(image=button_image_2, borderwidth=0, highlightthickness=0, command=lambda: attempt_registration(), relief="flat")
    register_button.place(x=119.0, y=559.0, width=133.0, height=37.0)

    # Back button
    back_button = Button(image=button_image_1, borderwidth=0, highlightthickness=0, command=lambda: back_to_pos_ad(window), relief="flat")
    back_button.place(x=349.0, y=559.0, width=133.0, height=37.0)

    canvas.create_rectangle(162.0, 21.0, 440.0, 85.0, fill="#FB7373", outline="")
    canvas.create_text(209.0, 29.0, anchor="nw", text="Registration", fill="#FFFFFF", font=("Hanuman Regular", 32 * -1))

    window.resizable(False, False)
    window.mainloop()


def back_to_pos_ad(window):
    window.destroy()
    from pos_admin import create_pos_admin_window
    create_pos_admin_window()

# Run main
if __name__ == "__main__":
    create_registration_window()
