import os
import shutil
import sqlite3
import time
import tkinter as tk
from cryptography.fernet import Fernet
from pathlib import Path
from tkinter import filedialog, messagebox

# From user made modules
import shared_state
from user_logs import log_actions

OUTPUT_PATH = Path(__file__).parent
DATABASE_PATH = OUTPUT_PATH / Path(r"Trimark_construction_supply.db")

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
    db_path = DATABASE_PATH
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
    db_path = DATABASE_PATH
    shutil.copy2(decrypted_file, db_path)
    os.remove(decrypted_file)  # Remove the decrypted file after restoration

    messagebox.showinfo("Success", "Database restored successfully")
    action = f"Restored a backup of the database found at: {backup_file}" 
    log_actions(shared_state.current_user, action) # Won't show to the user_logs because when restoring the backup, it will be overwritten.


'''
    Update Account Details | Update Account Details | Update Account Details | Update Account Details | Update Account Details | Update Account Details | Update Account Details
'''

def update_first_name(employee_id, new_first_name):
    conn = sqlite3.connect('Trimark_construction_supply.db')
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE accounts SET First_Name = ? WHERE Employee_ID = ?", (new_first_name, employee_id))
        conn.commit()
        messagebox.showinfo("Success", "First Name updated successfully")
        action = "Updated first name to " + new_first_name + "."
        log_actions(shared_state.current_user, action)
    except sqlite3.Error as e:
        conn.rollback()
        messagebox.showerror("Error", f"Error updating First Name: {e}")
    finally:
        conn.close()

def update_last_name(employee_id, new_last_name):
    conn = sqlite3.connect('Trimark_construction_supply.db')
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE accounts SET Last_Name = ? WHERE Employee_ID = ?", (new_last_name, employee_id))
        conn.commit()
        messagebox.showinfo("Success", "Last Name updated successfully")
        action = "Updated last name to " + new_last_name + "."
        log_actions(shared_state.current_user, action)
    except sqlite3.Error as e:
        conn.rollback()
        messagebox.showerror("Error", f"Error updating Last Name: {e}")
    finally:
        conn.close()

def update_password(employee_id, new_password, salt):
    conn = sqlite3.connect('Trimark_construction_supply.db')
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE accounts SET Password = ?, Salt = ? WHERE Employee_ID = ?", (new_password, salt, employee_id))
        conn.commit()
        messagebox.showinfo("Success", "Password updated successfully")
        action = "Changed password."
        log_actions(shared_state.current_user, action)
    except sqlite3.Error as e:
        conn.rollback()
        messagebox.showerror("Error", f"Error updating Password: {e}")
    finally:
        conn.close()

def update_email(employee_id, new_email):
    conn = sqlite3.connect('Trimark_construction_supply.db')
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE accounts SET Email = ? WHERE Employee_ID = ?", (new_email, employee_id))
        conn.commit()
        messagebox.showinfo("Success", "Email updated successfully")
        action = "Updated email to " + new_email + "."
        log_actions(shared_state.current_user, action)
    except sqlite3.Error as e:
        conn.rollback()
        messagebox.showerror("Error", f"Error updating Email: {e}")
    finally:
        conn.close()

def update_phone_number(employee_id, new_phone_number):
    conn = sqlite3.connect('Trimark_construction_supply.db')
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE accounts SET Contact_No = ? WHERE Employee_ID = ?", (new_phone_number, employee_id))
        conn.commit()
        messagebox.showinfo("Success", "Phone Number updated successfully")
        action = "Updated phone number to " + new_phone_number + "."
        log_actions(shared_state.current_user, action)
    except sqlite3.Error as e:
        conn.rollback()
        messagebox.showerror("Error", f"Error updating Phone Number: {e}")
    finally:
        conn.close()
