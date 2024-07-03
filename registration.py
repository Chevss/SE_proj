# Libraries
import re
import smtplib
import sqlite3
from datetime import datetime
from email.mime.text import MIMEText
from pathlib import Path
from tkinter import Button, Canvas, Scrollbar, Entry, messagebox, OptionMenu, PhotoImage, Radiobutton, StringVar, Tk
from tkcalendar import DateEntry
from tkinter.ttk import Treeview
import secrets
# From user made modules
import shared_state
from salt_and_hash import generate_salt, hash_password
from user_logs import log_actions

# Database connection
conn = sqlite3.connect('Trimark_construction_supply.db')
cursor = conn.cursor()

# Paths
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\Registration")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

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
def save_user(loa, first_name, last_name, mi, suffix, birthdate, contact_number, home_address, email, username, password, is_void):
    salt = generate_salt()
    hashed_password = hash_password(password, salt)
    date_registered = datetime.now()


    try:
        employee_id = generate_employee_id(loa)

        cursor.execute('''
        INSERT INTO accounts ( Employee_ID, LOA, First_Name, Last_Name, MI, Suffix, Birthdate, Contact_No, Address, Email, Username, Password, Salt, is_void, Date_Registered)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', ( employee_id, loa, first_name, last_name, mi, suffix, birthdate, contact_number, home_address, email, username, hashed_password, salt, is_void, date_registered))
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Failed to save user: {str(e)}")
        conn.rollback()

# def update_table():
#     try:
#         cursor.execute('SELECT * FROM accounts')
#         rows = cursor.fetchall()
#         print (rows)
        
#         # Clear existing items in the tree view
#         for item in tree.get_children():
#             print (item)
#             tree.delete(item)
        
#         # Insert updated data into the tree view
#         for row in rows:
#             tree.insert('', 'end', values=row)  # Modify according to your treeview structure
            
#         conn.commit()  # Commit any changes if necessary
#     except sqlite3.Error as e:
#         messagebox.showerror("Error", f"Failed to fetch data from database: {str(e)}")


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
def register_user(first_name, mi, last_name, suffix, birthdate, contact_number, home_address, email, loa, window):
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
    is_void = 0

    save_user(loa, first_name, last_name, mi, suffix, birthdate, contact_number, home_address, email, username, password, is_void)
    employee_id = generate_employee_id(loa)
    send_email(email, employee_id, username, password)

    log_actions(shared_state.current_user, action = f"Registered {first_name} {last_name} account with {loa} Level of Access.")

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
    log_actions(shared_state.current_user, action = "Go back to POS window")
    from pos_admin import create_pos_admin_window
    create_pos_admin_window()

def void_selected_account():
    selected_item = tree.focus()  # Get the currently selected item
    if selected_item:
        confirm_activate = messagebox.askyesno("Confirmation", "Are you sure you want to activate this account?")
        if confirm_activate:
            item = tree.item(selected_item)
            item_values = item['values']
            print(f"Current values before update: {item_values}")
            employee_id = item_values[1]

            try:
                # Update the database
                cursor.execute("UPDATE accounts SET is_void = 1 WHERE Employee_ID = ?", (employee_id,))
                conn.commit()  # Commit changes to the database
                print(f"Database updated successfully for Employee ID {employee_id}")

                # Update the treeview display
                new_status = "Inactive"
                tree.item(selected_item, values=(new_status,) + tuple(item_values[1:]))  # Update the status in the Treeview
                print(f"Current values after update: {tree.item(selected_item)['values']}")  # Print updated values

                messagebox.showinfo("Success", f"Account with Employee ID {employee_id} has been activated.")
                log_actions(shared_state.current_user, action=f"{shared_state.current_user} Activated user {employee_id}")

            except Exception as e:
                messagebox.showerror("Error", f"Error updating account: {str(e)}")
                print(f"Error updating account: {str(e)}")
        else:
            messagebox.showinfo("Canceled", "Operation canceled.")
    else:
        messagebox.showinfo("Error", "No item selected.")

def activate_selected_account():
    selected_item = tree.focus()  # Get the currently selected item
    if selected_item:
        confirm_activate = messagebox.askyesno("Confirmation", "Are you sure you want to activate this account?")
        if confirm_activate:
            item = tree.item(selected_item)
            item_values = item['values']
            print(f"Current values before update: {item_values}")
            employee_id = item_values[1]

            try:
                # Update the database
                cursor.execute("UPDATE accounts SET is_void = 0 WHERE Employee_ID = ?", (employee_id,))
                conn.commit()  # Commit changes to the database
                print(f"Database updated successfully for Employee ID {employee_id}")

                # Update the treeview display
                new_status = "Active"
                tree.item(selected_item, values=(new_status,) + tuple(item_values[1:]))  # Update the status in the Treeview
                print(f"Current values after update: {tree.item(selected_item)['values']}")  # Print updated values

                messagebox.showinfo("Success", f"Account with Employee ID {employee_id} has been activated.")
                log_actions(shared_state.current_user, action=f"{shared_state.current_user} Activated user {employee_id}")

            except Exception as e:
                messagebox.showerror("Error", f"Error updating account: {str(e)}")
                print(f"Error updating account: {str(e)}")
        else:
            messagebox.showinfo("Canceled", "Operation canceled.")
    else:
        messagebox.showinfo("Error", "No item selected.")


# Registration window
def create_registration_window():
    global window
    window = Tk()
    window.title("Registration")
    window.configure(bg="#FFE1C6")

    window_width, window_height = 1280, 690
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    canvas = Canvas(window, bg="#FFE1C6", height=690, width=1280, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)


    # Background creation

    # Labels
    canvas.create_text(860.0, 98.0, anchor="nw", text="First Name", fill="#000000", font=("Hanuman Regular", 16 * -1))
    canvas.create_text(1188.0, 98.0, anchor="nw", text="M.I.", fill="#000000", font=("Hanuman Regular", 16 * -1))
    canvas.create_text(860.0, 166.0, anchor="nw", text="Last Name", fill="#000000", font=("Hanuman Regular", 16 * -1))
    canvas.create_text(1180.0, 166.0, anchor="nw", text="Suffix", fill="#000000", font=("Hanuman Regular", 16 * -1))
    canvas.create_text(860.0, 232.0, anchor="nw", text="Birthdate", fill="#000000", font=("Hanuman Regular", 16 * -1))
    canvas.create_text(860.0, 292.0, anchor="nw", text="Contact Number", fill="#000000", font=("Hanuman Regular", 16 * -1))
    canvas.create_text(860.0, 358.0, anchor="nw", text="Home Address", fill="#000000", font=("Hanuman Regular", 16 * -1))
    canvas.create_text(860.0, 420.0, anchor="nw", text="Email Address", fill="#000000", font=("Hanuman Regular", 16 * -1))
    canvas.create_text(860.0, 497.0, anchor="nw", text="Level of Access", fill="#000000", font=("Hanuman Regular", 16 * -1))

    # First name
    first_name_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=1, font=("Hanuman Regular", 20 * -1))
    first_name_entry.place(x=860.0, y=125.0, width=307.0, height=36.0)

    def capitalize_mi(event):
        event.widget.after(0, lambda: update_entry(event.widget))

    def update_entry(widget):
        text = widget.get()
        widget.delete(0, 'end')
        widget.insert(0, text.upper())

    # Middle initial    
    mi_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=1, font=("Hanuman Regular", 20 * -1))
    mi_entry.place(x=1176.0, y=125.0, width=47.0, height=36.0)
    mi_entry.bind('<KeyRelease>', capitalize_mi)
    
    # Last name
    last_name_entry = Entry( bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=1, font=("Hanuman Regular", 20 * -1))
    last_name_entry.place(x=860.0, y=190.0, width=307.0, height=36.0)

    # Suffix
    suffix_entry = StringVar()
    suffix_options = ["", "Jr", "Sr", "I", "II", "III"]
    suffix_menu = OptionMenu(window, suffix_entry, *suffix_options)
    suffix_menu.config(bg="#FFE1C6", font=("Hanuman Regular", 14 * -1))
    suffix_menu.place(x=1176.0, y=190.0, width=47.0, height=36.0)

    # Birthdate  
    birthdate_entry = DateEntry(window, width=12, background='darkblue', foreground='white', borderwidth=1, font=("Hanuman Regular", 15))
    birthdate_entry.place(x=860, y=256)

    # Contact number    
    contact_no_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=1, font=("Hanuman Regular", 20 * -1))
    contact_no_entry.place(x=860.0, y=316.0, width=363.0, height=36.0)

    # Address
    address_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=1, font=("Hanuman Regular", 20 * -1))
    address_entry.place(x=860.0, y=382.0, width=363.0, height=36.0)

    # Email address
    email_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=1, font=("Hanuman Regular", 20 * -1))
    email_entry.place(x=860.0, y=444.0, width=363.0, height=36.0)
    
    # LOA
    loa_var = StringVar(value="employee")

    radio_admin = Radiobutton(window, text="Admin", variable=loa_var, value="admin", bg="#FFE1C6", font=("Hanuman Regular", 14 * -1))
    radio_admin.place(x=886.0, y=524.0)

    radio_employee = Radiobutton(window, text="Employee/Staff", variable=loa_var, value="employee", bg="#FFE1C6", font=("Hanuman Regular", 14 * -1))
    radio_employee.place(x=886.0, y=555.0)

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
            loa_var.get(),
            window
        )
        if success:
            print(f"User {email_entry.get()} registered successfully.")
            clear_entries()
            reload_window(window)
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
    register_button.place(x=860.0, y=609.0, width=133.0, height=37.0)

    # Back button
    back_button = Button( 
        window,
        text="Cancel",
        font=("Hanuman Regular", 16),
        bg="#FFFFFF",
        command=lambda:go_to_window(window)
    )
    
    back_button.place(x=1090.0, y=609.0, width=133.0, height=37.0)

    canvas.create_rectangle(903.0, 21.0, 1181.0, 85.0, fill="#FB7373", outline="")
    canvas.create_text(957.0, 33.0, anchor="nw", text="Registration", fill="#FFFFFF", font=("Hanuman Regular", 32 * -1))

    activate_button = Button( 
        window,
        text="Activate",
        font=("Hanuman Regular", 16),
        bg="#FFFFFF",
        command=activate_selected_account
    )

    activate_button.place(x=250.0, y=609.0, width=133.0, height=37.0)


    void_button = Button( 
        window,
        text="Void",
        font=("Hanuman Regular", 16),
        bg="#FFFFFF",
        command=void_selected_account
    )

    void_button.place(x=450.0, y=609.0, width=133.0, height=37.0)
    global tree
    # Create Treeview
    tree = Treeview(window, columns=("is_void", "Employee_ID", "LOA", "Name", "Birthdate", "Contact_No", "Address", "Email"),
                    show="headings", height=15)
    tree.heading("is_void", text="Status", anchor='center')
    tree.heading("Employee_ID", text="ID", anchor='center')
    tree.heading("LOA", text="LOA", anchor='center')
    tree.heading("Name", text="Name", anchor='center')
    tree.heading("Birthdate", text="Birthdate", anchor='center')
    tree.heading("Contact_No", text="Contact No", anchor='center')
    tree.heading("Address", text="Address", anchor='center')
    tree.heading("Email", text="Email", anchor='center')
    tree.column("is_void",  width=60, stretch=False, anchor='center')
    tree.column("Employee_ID",  width=55, stretch=False, anchor='center')
    tree.column("LOA",  width=50, stretch=False, anchor='center')
    tree.column("Name",  width=110, stretch=False, anchor='center')
    tree.column("Birthdate",  width=60, stretch=False, anchor='center')
    tree.column("Contact_No",  width=100, stretch=False, anchor='center')
    tree.column("Address",  width=200, stretch=False, anchor='center')
    tree.column("Email",  width=200, stretch=False, anchor='center')

    # Create vertical scrollbar
    vsb = Scrollbar(window, orient="vertical", command=tree.yview)
    vsb.place(x=780, y=21, height=525)
    tree.configure(yscrollcommand=vsb.set)
    # Create horizontal scrollbar
    hsb = Scrollbar(window, orient="horizontal", command=tree.xview)
    hsb.place(x=83, y=546, width=697)
    tree.configure(xscrollcommand=hsb.set)

    # Place Treeview
    tree.place(x=83, y=21, width=697, height=525)   

    # Fetch data from database and insert into Treeview
    cursor.execute("SELECT is_void, Employee_ID, LOA, First_Name, MI, Last_Name, Suffix, Birthdate, Contact_No, Address, Email FROM accounts")
    rows = cursor.fetchall()
    
    for row in rows:
        if row[0] == '0':
            is_void = "Active"
        elif row[0] == '1':
            is_void = "Inactive"
        employee_id = row[1]
        loa = row[2]
        first_name = row[3]
        mi = row[4] if row[4] else ""
        last_name = row[5]
        suffix = row[6] if row[6] else ""
        name = f"{first_name} {mi} {last_name} {suffix}".strip()
        birthdate = row[7]
        contact_no = row[8]
        address = row[9]
        email = row[10]
        tree.insert("", "end", values=(is_void, employee_id, loa, name, birthdate, contact_no, address, email))

      # Update the status in Treeview

    window.resizable(False, False)
    window.mainloop()

def reload_window(window):
    window.destroy()
    create_registration_window()

# Run main
# if __name__ == "__main__":
#     create_registration_window()
