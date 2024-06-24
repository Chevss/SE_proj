# Libraries
import hashlib
import re
import secrets
import smtplib
import sqlite3
from datetime import datetime
from email.mime.text import MIMEText
from pathlib import Path
from tkinter import Button, Canvas, Entry, messagebox, OptionMenu, PhotoImage, Radiobutton, StringVar, Tk
from tkcalendar import DateEntry

import shared_state
from user_logs import log_actions

# Database connection
conn = sqlite3.connect('Trimark_construction_supply.db')
cursor = conn.cursor()

# Paths
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\Registration")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Using hash to protect the confidentiality of passwords.
def generate_salt():
    return secrets.token_hex(16)

def hash_password(password, salt):
    return hashlib.sha256((password + salt).encode()).hexdigest()

# Send email containing the generated username from registration inputs and random generated password.
def send_email(email, employee_id, username, password):
    try:
        msg = MIMEText(f"Your Employee ID is: {employee_id}\nYour username is: {username}\nYour temporary password is: {password}")
        msg['Subject'] = 'Registration Details'
        msg['From'] = 'trimarkcstest@outlook.com'
        msg['To'] = email

        with smtplib.SMTP('smtp-mail.outlook.com', 587) as server:
            server.starttls()
            server.login('trimarkcstest@outlook.com', '1ZipJM2DsVnRoBkmVVKRCm0e8c6NniwhjW1FEWEC8n5Y')
            server.sendmail('trimarkcstest@outlook.com', email, msg.as_string())
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

# Store the registered employee or admin to the database.
def save_user(loa, first_name, last_name, mi, suffix, birthdate, contact_number, home_address, email, username, password):
    salt = generate_salt()
    hashed_password = hash_password(password, salt)
    date_registered = datetime.now()

    try:
        employee_id = generate_employee_id(loa)

        cursor.execute('''
        INSERT INTO accounts (Employee_ID, LOA, First_Name, Last_Name, MI, Suffix, Birthdate, Contact_No, Address, Email, Username, Password, Salt, Date_Registered)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (employee_id, loa, first_name, last_name, mi, suffix, birthdate, contact_number, home_address, email, username, hashed_password, salt, date_registered))
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Failed to save user: {str(e)}")
        conn.rollback()

# Generate employee ID like how TIP does but with modification.
def generate_employee_id(loa):
    # Get the current year
    current_year = datetime.now().year
    # Get the initial character based on level of access
    initial_char = 'A' if loa == 'admin' else 'E'
    
    try:
        # Fetch the last used counter for this year and level of access
        cursor.execute("SELECT MAX(Employee_ID) FROM accounts WHERE Employee_ID LIKE ?", (f"{current_year}{initial_char}%",))
        last_used_id = cursor.fetchone()[0]
        
        if last_used_id:
            # Extract the counter part and increment
            counter = int(last_used_id[-2:]) + 1
        else:
            # If no previous IDs exist for this year and level of access, start with 01
            counter = 1
        
        # Format the employee ID
        employee_id = f"{current_year}{initial_char}{counter:02}"
        
        return employee_id
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate Employee ID: {str(e)}")
        conn.rollback()

# Generate username like how TIP does but not exactly.
def generate_username(first_name, mi, last_name, suffix, loa):
    # Determine the prefix based on the level of access
    prefix = 'a' if loa == 'admin' else 'e'
    # Get the initials from the first name (concatenating the first letter of each word)
    first_name_initials = ''.join([name[0].lower() for name in first_name.split()])
    # Get the middle initial, if provided
    mi_part = mi.lower() if mi else ''
    # Get the suffix, if provided
    suffix_part = suffix.lower() if suffix else ''
    # Generate the username
    return f"{prefix}{first_name_initials}{mi_part}{last_name.lower()}{suffix_part}_tmcs"

# Register user
def register_user(first_name, mi, last_name, suffix, birthdate, contact_number, home_address, email, loa):
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

    save_user(loa, first_name, last_name, mi, suffix, birthdate, contact_number, home_address, email, username, password)
    employee_id = generate_employee_id(loa)
    send_email(email, employee_id, username, password)

    log_actions(shared_state.current_user, action = "Registered a user.")

    messagebox.showinfo("Success", "Registration successful. Your username, temporary password, and Employee ID have been sent to your email.")
    return True

# Functions to check if the inputs are valid.
def is_valid_name(name):
    return bool(re.match(r'^[a-zA-Z]+( [a-zA-Z]+)*$', name))

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

def go_to_window(windows):
        window.destroy()
        from pos_admin import create_pos_admin_window
        create_pos_admin_window()

# Registration window
def create_registration_window():
    global window
    window = Tk()
    window.title("Registration")
    window.configure(bg="#FFE1C6")

    window_width, window_height = 600, 730
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    canvas = Canvas(window, bg="#FFE1C6", height=730, width=600, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)


    # Background creation

    # Labels
    canvas.create_text(119.0, 98.0, anchor="nw", text="First Name", fill="#000000", font=("Hanuman Regular", 16 * -1))
    canvas.create_text(447.0, 98.0, anchor="nw", text="M.I.", fill="#000000", font=("Hanuman Regular", 16 * -1))
    canvas.create_text(119.0, 166.0, anchor="nw", text="Last Name", fill="#000000", font=("Hanuman Regular", 16 * -1))
    canvas.create_text(439.0, 166.0, anchor="nw", text="Suffix", fill="#000000", font=("Hanuman Regular", 16 * -1))
    canvas.create_text(119.0, 232.0, anchor="nw", text="Birthdate", fill="#000000", font=("Hanuman Regular", 16 * -1))
    canvas.create_text(119.0, 292.0, anchor="nw", text="Contact Number", fill="#000000", font=("Hanuman Regular", 16 * -1))
    canvas.create_text(119.0, 358.0, anchor="nw", text="Home Address", fill="#000000", font=("Hanuman Regular", 16 * -1))
    canvas.create_text(119.0, 420.0, anchor="nw", text="Email Address", fill="#000000", font=("Hanuman Regular", 16 * -1))
    canvas.create_text(119.0, 497.0, anchor="nw", text="Level of Access", fill="#000000", font=("Hanuman Regular", 16 * -1))

    # First name
    first_name_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=1, font=("Hanuman Regular", 20 * -1))
    first_name_entry.place(x=119.0, y=125.0, width=307.0, height=36.0)

    def capitalize_mi(event):
        event.widget.after(0, lambda: update_entry(event.widget))

    def update_entry(widget):
        text = widget.get()
        widget.delete(0, 'end')
        widget.insert(0, text.upper())

    # Middle initial    
    mi_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=1, font=("Hanuman Regular", 20 * -1))
    mi_entry.place(x=435.0, y=125.0, width=47.0, height=36.0)
    mi_entry.bind('<KeyRelease>', capitalize_mi)
    
    # Last name
    last_name_entry = Entry( bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=1, font=("Hanuman Regular", 20 * -1))
    last_name_entry.place(x=119.0, y=190.0, width=307.0, height=36.0)

    # Suffix
    suffix_entry = StringVar()
    suffix_options = ["", "Jr", "Sr", "I", "II", "III"]
    suffix_menu = OptionMenu(window, suffix_entry, *suffix_options)
    suffix_menu.config(bg="#FFE1C6", font=("Hanuman Regular", 14 * -1))
    suffix_menu.place(x=435.0, y=190.0, width=47.0, height=36.0)

    # Birthdate  
    birthdate_entry = DateEntry(window, width=12, background='darkblue', foreground='white', borderwidth=1, font=("Hanuman Regular", 15))
    birthdate_entry.place(x=119, y=256)

    # Contact number    
    contact_no_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=1, font=("Hanuman Regular", 20 * -1))
    contact_no_entry.place(x=119.0, y=316.0, width=363.0, height=36.0)

    # Address
    address_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=1, font=("Hanuman Regular", 20 * -1))
    address_entry.place(x=119.0, y=382.0, width=363.0, height=36.0)

    # Email address
    email_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=1, font=("Hanuman Regular", 20 * -1))
    email_entry.place(x=119.0, y=444.0, width=363.0, height=36.0)
    
    # LOA
    loa_var = StringVar(value="employee")

    radio_admin = Radiobutton(window, text="Admin", variable=loa_var, value="admin", bg="#FFE1C6", font=("Hanuman Regular", 14 * -1))
    radio_admin.place(x=145.0, y=524.0)

    radio_employee = Radiobutton(window, text="Employee/Staff", variable=loa_var, value="employee", bg="#FFE1C6", font=("Hanuman Regular", 14 * -1))
    radio_employee.place(x=145.0, y=555.0)

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
            birthdate_entry.get(),
            contact_no_entry.get(), 
            address_entry.get(), 
            email_entry.get(), 
            loa_var.get()
        )
        if success:
            print(f"User {email_entry.get()} registered successfully.")
            clear_entries()
        else:
            print("Registration failed.")

    # Register button
    register_button = Button( 
        window,
        text="Register",
        font=("Hanuman Regular", 16),
        bg="#FC7373",
        fg="#FFFFFF",
        command=lambda: attempt_registration() 
    )
    register_button.place(x=119.0, y=609.0, width=133.0, height=37.0)

    # Back button
    back_button = Button( 
        window,
        text="Cancel",
        font=("Hanuman Regular", 16),
        bg="#FFFFFF",
        command=lambda:go_to_window(window)
    )
    
    back_button.place(x=349.0, y=609.0, width=133.0, height=37.0)

    canvas.create_rectangle(162.0, 21.0, 440.0, 85.0, fill="#FB7373", outline="")
    canvas.create_text(209.0, 29.0, anchor="nw", text="Registration", fill="#FFFFFF", font=("Hanuman Regular", 32 * -1))

    window.resizable(False, False)
    window.mainloop()

# Run main
if __name__ == "__main__":
    create_registration_window()
