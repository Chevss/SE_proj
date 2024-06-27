import os
import shutil
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
