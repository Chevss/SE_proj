from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox
import re
import hashlib
import secrets
import sqlite3

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:/Users/TIPQC/Desktop/SE_proj-main/assets/New_pass")


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
        conn = sqlite3.connect('accounts.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE accounts SET Password = ?, Salt = ? WHERE Email = ?', (hashed_password, salt, email))
        conn.commit()
        messagebox.showinfo("Success", "Password updated successfully.")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error updating password: {e}")
    finally:
        cursor.close()
        conn.close()


def create_new_pass_window(email):
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

    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        300.5,
        205.0,
        image=entry_image_1
    )
    confirm_pass_entry = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        font=("Hanuman Regular", 24 * -1),
        show="•"
    )
    confirm_pass_entry.place(
        x=119.0,
        y=186.0,
        width=363.0,
        height=36.0
    )

    entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        300.5,
        132.0,
        image=entry_image_2
    )
    new_pass_entry = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
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

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    back_button = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("back_button clicked"),
        relief="flat"
    )
    back_button.place(
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

    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    confirm_button = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=handle_confirm,
        relief="flat"
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

    window.resizable(False, False)
    window.mainloop()




if __name__ == "__main__":
    create_new_pass_window("user@example.com")
