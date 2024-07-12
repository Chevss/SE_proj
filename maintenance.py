from cryptography.fernet import Fernet
from pathlib import Path
from tkinter import BooleanVar, Button, Canvas, Checkbutton, Entry, filedialog, messagebox, Tk
import os
import shutil
import sqlite3
import time

# From user made modules
from client import send_query
from new_pass import is_valid_password
from registration import is_valid_contact_number, is_valid_email, is_valid_name
from salt_and_hash import generate_salt, hash_password
from server.server import DATABASE
from user_logs import log_actions
import shared_state

employee_id = None

'''
    Backup and Restore | Backup and Restore | Backup and Restore | Backup and Restore | Backup and Restore | Backup and Restore | Backup and Restore | Backup and Restore
'''

# Generate a key for encryption
def generate_key():
    return Fernet.generate_key()

# Load or generate a key
def load_key():
    key_file = "secret.key"
    if not os.path.exists(key_file):
        key = generate_key()
        with open(key_file, "wb") as key_file:
            key_file.write(key)
    else:
        with open(key_file, "rb") as key_file:
            key = key_file.read()
    return key

# Encrypt a file
def encrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, "rb") as file:
        file_data = file.read()
    encrypted_data = fernet.encrypt(file_data)
    encrypted_file_path = file_path + ".enc"
    with open(encrypted_file_path, "wb") as file:
        file.write(encrypted_data)
    return encrypted_file_path

# Decrypt a file
def decrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = fernet.decrypt(encrypted_data)
    decrypted_file_path = file_path.replace(".enc", "")
    with open(decrypted_file_path, "wb") as file:
        file.write(decrypted_data)
    return decrypted_file_path

# Backup the database
def backup_database(local=True):
    db_path = DATABASE
    key = load_key()
    timestamp = time.strftime("%Y%m%d%H%M%S")

    backup_dir = filedialog.askdirectory()
    if not backup_dir:
        return  # User cancelled the operation
    backup_file = os.path.join(backup_dir, f"backup_{timestamp}.db")

    shutil.copy2(db_path, backup_file)
    encrypted_file = encrypt_file(backup_file, key)
    os.remove(backup_file)  # Remove the unencrypted file

    messagebox.showinfo("Success", f"Backup created at {encrypted_file}")
    action = f"Made a backup of the database stored at: {backup_dir}"
    log_actions(shared_state.current_user, action)

# Restore the database
def restore_database(local=True):
    key = load_key()

    backup_file = filedialog.askopenfilename(filetypes=[("Encrypted Database", "*.db.enc")])
    if not backup_file:
        return  # User cancelled the operation

    decrypted_file = decrypt_file(backup_file, key)
    db_path = DATABASE
    shutil.copy2(decrypted_file, db_path)
    os.remove(decrypted_file)  # Remove the decrypted file after restoration

    messagebox.showinfo("Success", "Database restored successfully")
    action = f"Restored a backup of the database found at: {backup_file}" 
    log_actions(shared_state.current_user, action) # Won't show to the user_logs because when restoring the backup, it will be overwritten.


'''
    Update Account Details | Update Account Details | Update Account Details | Update Account Details | Update Account Details | Update Account Details | Update Account Details
'''

def update_first_name(employee_id, new_first_name):
    try:
        query = "UPDATE accounts SET First_Name = ? WHERE Employee_ID = ?"
        params = (new_first_name, employee_id)
        response = send_query(query, params)

        messagebox.showinfo("Success", "First Name updated successfully")
        action = "Updated first name to " + new_first_name + "."
        log_actions(shared_state.current_user, action)
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error updating First Name: {response}")

def update_last_name(employee_id, new_last_name):
    try:
        query = "UPDATE accounts SET Last_Name = ? WHERE Employee_ID = ?"
        params = (new_last_name, employee_id)
        response = send_query(query, params)
        
        messagebox.showinfo("Success", "Last Name updated successfully")
        action = "Updated last name to " + new_last_name + "."
        log_actions(shared_state.current_user, action)
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error updating Last Name: {response}")
    
def update_password(employee_id, new_password, salt):
    try:
        query = "UPDATE accounts SET Password = ?, Salt = ? WHERE Employee_ID = ?"
        params = (new_password, salt, employee_id)
        response = send_query(query, params)

        messagebox.showinfo("Success", "Password updated successfully")
        action = "Changed password."
        log_actions(shared_state.current_user, action)
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error updating Password: {e}")

def update_email(employee_id, new_email):
    try:
        query = "UPDATE accounts SET Email = ? WHERE Employee_ID = ?"
        params = (new_email, employee_id)
        response = send_query(query, params)

        messagebox.showinfo("Success", "Email updated successfully")
        action = "Updated email to " + new_email + "."
        log_actions(shared_state.current_user, action)
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error updating Email: {response}")

def update_phone_number(employee_id, new_phone_number):
    try:
        query = "UPDATE accounts SET Contact_No = ? WHERE Employee_ID = ?"
        params = (new_phone_number, employee_id)
        response = send_query(query, params)

        messagebox.showinfo("Success", "Phone Number updated successfully")
        action = "Updated phone number to " + new_phone_number + "."
        log_actions(shared_state.current_user, action)
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error updating Phone Number: {response}")

def perform_action(command_name):
    from pos_admin import window
    if shared_state.current_user:
        username = shared_state.current_user  # Assuming current_user stores the username
        employee_id = get_employee_id(username) # Fetch the Employee_ID using the username

        if command_name == "first_name":
            window.destroy()
            create_change_first_name_window()

        elif command_name == "last_name":
            window.destroy()
            create_change_last_name_window()
            
        elif command_name == "password":
            window.destroy()
            create_change_password_window()

        elif command_name == "email":
            window.destroy()
            create_change_email_window()

        elif command_name == "phone_number":
            window.destroy()
            create_change_phone_window()

# Handling changes
def get_employee_id(username):
    global employee_id

    try:
        query = "SELECT Employee_ID FROM accounts WHERE Username = ?"
        params = (username,)
        response = send_query(query, params)

        if response:
            employee_id = response[0][0]  # Assign fetched Employee_ID to global variable
            return employee_id
        else:
            return None

    except sqlite3.Error as e:
        print(f"Error fetching employee ID: {e}")
        return None

def handle_first_name_update():
    new_first_name = new_first_name_entry.get()
    if new_first_name:
        if is_valid_name(new_first_name):
            update_first_name(employee_id, new_first_name)
            go_to_window("Back")
        else:
            messagebox.showerror("Error", "Invalid first name format")
    else:
        messagebox.showerror("Error", "Please enter a new first name")

def handle_last_name_update():
    new_last_name = new_last_name_entry.get()
    if new_last_name:
        if is_valid_name(new_last_name):
            update_last_name(employee_id, new_last_name)
            go_to_window("Back")
        else:
            messagebox.showerror("Error", "Invalid last name format")
    else:
        messagebox.showerror("Error", "Please enter a new last name")

def handle_password_update():
    global employee_id
    new_password = new_pass_entry.get()
    confirm_password = confirm_pass_entry.get()

    if new_password and confirm_password:
        if new_password == confirm_password:
            valid, message = is_valid_password(new_password)
            if valid:
                salt = generate_salt()
                hashed_password = hash_password(new_password, salt)
                update_password(employee_id, hashed_password, salt)
                go_to_window("Back")
            else:
                messagebox.showerror("Error", message)
        else:
            messagebox.showerror("Error", "Passwords do not match")
    else:
        messagebox.showerror("Error", "Please enter both passwords")

def check_email_uniqueness(email, current_email=None):
    try:
        query = "SELECT Email FROM accounts"
        params = ()
        response = send_query(query, params)

        existing_emails = [row[0] for row in response]
        
        if email in existing_emails and email != current_email:
            return False, "Email already in use"
        return True, ""

    except sqlite3.Error as e:
        print(f"Error checking email uniqueness: {e}")
        return False, "Error checking email uniqueness"

def handle_email_update(username):
    new_email = new_email_entry.get()
    if new_email:
        valid, message = is_valid_email(new_email)
        if valid:
            unique, unique_message = check_email_uniqueness(new_email, current_email=username)
            if unique:
                employee_id = get_employee_id(username)  # Fetch employee ID
                update_email(employee_id, new_email)
                messagebox.showinfo("Success", "Email updated successfully")
                action = "Updated email to " + new_email + "."
                log_actions(shared_state.current_user, action)
                go_to_window("Back")  # Assuming this function exists to close the window or navigate away
            else:
                messagebox.showerror("Error", unique_message)
        else:
            messagebox.showerror("Error", message)
    else:
        messagebox.showerror("Error", "Please enter a new email")

def handle_phone_update():
    new_phone_number = new_phone_entry.get()
    if new_phone_number:
        if is_valid_contact_number(new_phone_number):
            update_phone_number(employee_id, new_phone_number)
            go_to_window("Back")
        else:
            messagebox.showerror("Error", "Invalid phone number format")
    else:
        messagebox.showerror("Error", "Please enter a new phone number")

# Windows
def go_to_window(windows):
    window.destroy()
    if windows == "Back":
        import pos_admin
        pos_admin.create_pos_admin_window()

def create_change_first_name_window():
    global window, new_first_name_entry
    window = Tk()
    window.title("Update Account Details: First Name")
    window.geometry("500x230")
    window.configure(bg="#FFE1C6")

    window_width, window_height = 500, 230
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    canvas = Canvas(window, bg="#DDD", height=400, width=600, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    canvas.create_rectangle(window_width, 0, 0, 55, fill="#000", outline="")
    canvas.create_text(140, 15, anchor="nw", text="Change First Name", fill="#FFFFFF", font=("Hanuman Regular", 24 * -1))

    canvas.create_text(50, 70, anchor="nw", text="New First Name", fill="#000000", font=("Hanuman Regular", 16 * -1))
    new_first_name_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=1, font=("Hanuman Regular", 24 * -1))
    new_first_name_entry.place(x=50, y=95, width=400, height=32)

    confirm_button = Button(window, text="Confirm", font=("Hanuman Regular", 16), bg="green", fg='#FFF', command=handle_first_name_update)
    confirm_button.place(x=50, y=150, width=100.0, height=32)

    cancel_button = Button(window, text="Cancel", font=("Hanuman Regular", 16), bg="red", fg="#FFF", command=lambda:go_to_window("Back"))
    cancel_button.place(x=350, y=150, width=100.0, height=32)

    window.resizable(False, False)
    window.mainloop()

def create_change_last_name_window():
    global window, new_last_name_entry
    window = Tk()
    window.title("Update Account Details: Last Name")
    window.geometry("500x230")
    window.configure(bg="#FFE1C6")

    window_width, window_height = 500, 230
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    canvas = Canvas(window, bg="#DDD", height=400, width=600, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    canvas.create_rectangle(window_width, 0, 0, 55, fill="#000", outline="")
    canvas.create_text(145, 15, anchor="nw", text="Change Last Name", fill="#FFFFFF", font=("Hanuman Regular", 24 * -1))

    canvas.create_text(50, 70, anchor="nw", text="New Last Name", fill="#000000", font=("Hanuman Regular", 16 * -1))
    new_last_name_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=1, font=("Hanuman Regular", 24 * -1))
    new_last_name_entry.place(x=50, y=95, width=400, height=32)

    confirm_button = Button(window, text="Confirm", font=("Hanuman Regular", 16), bg="green", fg='#FFF', command=handle_last_name_update)
    confirm_button.place(x=50, y=150, width=100.0, height=32)

    cancel_button = Button(window, text="Cancel", font=("Hanuman Regular", 16), bg="red", fg="#FFF", command=lambda:go_to_window("Back"))
    cancel_button.place(x=350, y=150, width=100.0, height=32)

    window.resizable(False, False)
    window.mainloop()

def create_change_password_window():
    global window, new_pass_entry, confirm_pass_entry
    window = Tk()
    window.title("Update Account Details: Password")
    window.geometry("500x300")
    window.configure(bg="#FFE1C6")

    window_width, window_height = 500, 300
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    def toggle_password_visibility():
        if show_password_var.get():
            new_pass_entry.config(show="")
            confirm_pass_entry.config(show="")
        else:
            new_pass_entry.config(show="•")
            confirm_pass_entry.config(show="•")

    canvas = Canvas(window, bg="#DDD", height=400, width=600, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    canvas.create_rectangle(window_width, 0, 0, 55, fill="#000", outline="")
    canvas.create_text(150, 15, anchor="nw", text="Change Password", fill="#FFFFFF", font=("Hanuman Regular", 24 * -1))

    canvas.create_text(50, 70, anchor="nw", text="New Password", fill="#000000", font=("Hanuman Regular", 16 * -1))
    new_pass_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=1, font=("Hanuman Regular", 24 * -1), show="•")
    new_pass_entry.place(x=50, y=95, width=400, height=32)

    canvas.create_text(50, 140, anchor="nw", text="Repeat Password", fill="#000000", font=("Hanuman Regular", 16 * -1))
    confirm_pass_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=1, font=("Hanuman Regular", 24 * -1), show="•")
    confirm_pass_entry.place(x=50, y=165, width=400, height=32)

    confirm_button = Button(window, text="Confirm", font=("Hanuman Regular", 16), bg="green", fg='#FFF', command=lambda:handle_password_update())
    confirm_button.place(x=50, y=220, width=100.0, height=32)

    cancel_button = Button(window, text="Cancel", font=("Hanuman Regular", 16), bg="red", fg="#FFF", command=lambda:go_to_window("Back"))
    cancel_button.place(x=350, y=220, width=100.0, height=32)
    
    show_password_var = BooleanVar()
    show_password_checkbox = Checkbutton(window, text="Show Password", variable=show_password_var, bg="#DDD", font=("Hanuman Regular", 10),
        command=toggle_password_visibility
    )
    show_password_checkbox.place(x=330, y=135)

    window.resizable(False, False)
    window.mainloop()

def create_change_email_window():
    global window, new_email_entry
    window = Tk()
    window.title("Update Account Details: Email")
    window.geometry("500x230")
    window.configure(bg="#FFE1C6")

    window_width, window_height = 500, 230
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    canvas = Canvas(window, bg="#DDD", height=400, width=600, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    canvas.create_rectangle(window_width, 0, 0, 55, fill="#000", outline="")
    canvas.create_text(165, 15, anchor="nw", text="Change Email", fill="#FFFFFF", font=("Hanuman Regular", 24 * -1))

    canvas.create_text(50, 70, anchor="nw", text="New Email", fill="#000000", font=("Hanuman Regular", 16 * -1))
    new_email_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=1, font=("Hanuman Regular", 24 * -1))
    new_email_entry.place(x=50, y=95, width=400, height=32)

    confirm_button = Button(window, text="Confirm", font=("Hanuman Regular", 16), bg="green", fg='#FFF', command=lambda:handle_email_update(shared_state.current_user))
    confirm_button.place(x=50, y=150, width=100.0, height=32)

    cancel_button = Button(window, text="Cancel", font=("Hanuman Regular", 16), bg="red", fg="#FFF", command=lambda:go_to_window("Back"))
    cancel_button.place(x=350, y=150, width=100.0, height=32)

    window.resizable(False, False)
    window.mainloop()

def create_change_phone_window():
    global window, new_phone_entry
    window = Tk()
    window.title("Update Account Details: Phone Number")
    window.geometry("500x230")
    window.configure(bg="#FFE1C6")

    window_width, window_height = 500, 230
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    canvas = Canvas(window, bg="#DDD", height=400, width=600, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    canvas.create_rectangle(window_width, 0, 0, 55, fill="#000", outline="")
    canvas.create_text(120, 15, anchor="nw", text="Change Phone Number", fill="#FFFFFF", font=("Hanuman Regular", 24 * -1))

    canvas.create_text(50, 70, anchor="nw", text="New Phone Number", fill="#000000", font=("Hanuman Regular", 16 * -1))
    new_phone_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=1, font=("Hanuman Regular", 24 * -1))
    new_phone_entry.place(x=50, y=95, width=400, height=32)

    confirm_button = Button(window, text="Confirm", font=("Hanuman Regular", 16), bg="green", fg='#FFF', command=handle_phone_update)
    confirm_button.place(x=50, y=150, width=100.0, height=32)

    cancel_button = Button(window, text="Cancel", font=("Hanuman Regular", 16), bg="red", fg="#FFF", command=lambda:go_to_window("Back"))
    cancel_button.place(x=350, y=150, width=100.0, height=32)

    window.resizable(False, False)
    window.mainloop()
