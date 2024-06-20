from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox, Checkbutton, BooleanVar
import re
import hashlib
import secrets
import sqlite3

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\chevy_9ljzuod\Downloads\SE_proj-main\assets\New_pass")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def generate_salt():
    return secrets.token_hex(16)


def hash_password(password, salt):
    return hashlib.sha256((password + salt).encode()).hexdigest()


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


def update_password(email, new_password):
    salt = generate_salt()
    hashed_password = hash_password(new_password, salt)
    try:
        conn = sqlite3.connect('Trimark_construction_supply.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE accounts SET Password = ?, Salt = ? WHERE Email = ?', (hashed_password, salt, email))
        conn.commit()
        messagebox.showinfo("Success", "Password updated successfully.")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error updating password: {e}")
    finally:
        cursor.close()
        conn.close()

def go_to_window(windows):
        window.destroy()
        if windows == "Cancel":
            import login
            login.create_login_window()

def create_new_pass_window(email):
    global window
    window = Tk()
    window.title("New Password")
    window.geometry("600x400")
    window.configure(bg="#FFE1C6")

    window_width, window_height = 600, 400
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    canvas = Canvas(
        window,
        bg="#FFE1C6",
        height=400,
        width=600,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    confirm_pass_entry = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=1,
        font=("Hanuman Regular", 24 * -1),
        show="•"
    )
    confirm_pass_entry.place(
        x=119.0,
        y=186.0,
        width=363.0,
        height=36.0
    )

    new_pass_entry = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=1,
        font=("Hanuman Regular", 24 * -1),
        show="•"
    )
    new_pass_entry.place(
        x=119.0,
        y=113.0,
        width=363.0,
        height=36.0
    )

    canvas.create_text(
        119.0,
        89.0,
        anchor="nw",
        text="New Password",
        fill="#000000",
        font=("Hanuman Regular", 16 * -1)
    )

    canvas.create_text(
        119.0,
        162.0,
        anchor="nw",
        text="Confirm New Password",
        fill="#000000",
        font=("Hanuman Regular", 16 * -1)
    )
    

    cancel_button = Button(
        window,
        text="Cancel",
        font=("Hanuman Regular", 16),
        bg="#FFFFFF",
        command=lambda:go_to_window("Cancel")
    )
    cancel_button.place(
        x=415.0,
        y=336.0,
        width=133.0,
        height=37.0
    )
    

    def handle_confirm():
        new_password = new_pass_entry.get()
        confirm_password = confirm_pass_entry.get()

        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        valid_password, password_message = is_valid_password(new_password)
        if not valid_password:
            messagebox.showerror("Error", password_message)
            return

        update_password(email, new_password)
        window.destroy()
        import login
        login.create_login_window()

    confirm_button = Button(
        window,
        text="Confirm",
        font=("Hanuman Regular", 16),
        bg="#FC7373",
        fg='white',
        command=lambda:handle_confirm()
    )
    confirm_button.place(
        x=250.0,
        y=236.0,
        width=100.0,
        height=37.0
    )

    canvas.create_rectangle(
        179.0,
        20.0,
        420.0,
        76.0,
        fill="#FB7373",
        outline=""
    )

    canvas.create_text(
        220.0,
        35.0,
        anchor="nw",
        text="New Password",
        fill="#FFFFFF",
        font=("Hanuman Regular", 24 * -1)
    )
    
    show_password_var = BooleanVar()

    def toggle_password_visibility():
        if show_password_var.get():
            new_pass_entry.config(show="")
            confirm_pass_entry.config(show="")
        else:
            new_pass_entry.config(show="•")
            confirm_pass_entry.config(show="•")

    show_password_checkbox = Checkbutton(
        window,
        text="Show Password",
        variable=show_password_var,
        bg="#FFE1C6",
        font=("Hanuman Regular", 10),
        command=toggle_password_visibility
    )
    show_password_checkbox.place(x=360.0, y=158.0)

    window.resizable(False, False)
    window.mainloop()




if __name__ == "__main__":
    create_new_pass_window("user@example.com")
