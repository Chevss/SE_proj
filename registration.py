from pathlib import Path
from tkinter import Tk, Canvas, Text, Button, PhotoImage

import secrets
import hashlib
import sqlite3

conn = sqlite3.connect('accounts.db')
cursor = conn.cursor()
window = Tk()

def generate_salt():
    salt = secrets.token_hex(16)
    return salt

def hash_password(password, salt):
    salted_password = password + salt
    return hashlib.sha256(salted_password.encode()).hexdigest()

def hash_username(username):
    return hashlib.sha256(username.encode()).hexdigest()

def save_password(username, password, loa, email):
    salt = generate_salt()
    hashed_password = hash_password(password, salt)
    hashed_username = hash_username(username)

    cursor.execute("INSERT INTO accounts (username, salt, hashed_password, Loa, email) VALUES (?,?,?,?,?)",
        (hashed_username, salt, hashed_password, loa, email))
    conn.commit()

def  create_registration_window():
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:/Users/TIPQC/Downloads/SE_proj-main/assets/Registration")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window.title("Registration")
    window.geometry("600x550")
    window.configure(bg = "#FFE1C6")

    canvas = Canvas(
        window,
        bg = "#FFE1C6",
        height = 550,
        width = 600,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        300.5,
        247.0,
        image=entry_image_1
    )
    entry_1 = Text(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entry_1.place(
        x=119.0,
        y=228.0,
        width=363.0,
        height=36.0
    )

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        300.5,
        182.0,
        image=entry_image_2
    )
    entry_2 = Text(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entry_2.place(
        x=119.0,
        y=163.0,
        width=363.0,
        height=36.0
    )

    canvas.create_text(
        119.0,
        139.0,
        anchor="nw",
        text="User",
        fill="#000000",
        font=("Hanuman Regular", 16 * -1)
    )

    canvas.create_text(
        119.0,
        204.0,
        anchor="nw",
        text="Password",
        fill="#000000",
        font=("Hanuman Regular", 16 * -1)
    )

    entry_image_3 = PhotoImage(
        file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(
        300.5,
        312.0,
        image=entry_image_3
    )
    entry_3 = Text(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entry_3.place(
        x=119.0,
        y=293.0,
        width=363.0,
        height=36.0
    )

    canvas.create_text(
        119.0,
        269.0,
        anchor="nw",
        text="Confirm Password",
        fill="#000000",
        font=("Hanuman Regular", 16 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_1 clicked"),
        relief="flat"
    )
    button_1.place(
        x=349.0,
        y=466.0,
        width=133.0,
        height=37.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_2 clicked"),
        relief="flat"
    )
    button_2.place(
        x=119.0,
        y=466.0,
        width=133.0,
        height=37.0
    )

    canvas.create_rectangle(
        161.0,
        44.0,
        439.0,
        108.0,
        fill="#FB7373",
        outline="")

    canvas.create_text(
        207.0,
        52.0,
        anchor="nw",
        text="Registration",
        fill="#FFFFFF",
        font=("Hanuman Regular", 32 * -1)
    )

    canvas.create_text(
        119.0,
        339.0,
        anchor="nw",
        text="Level of Access",
        fill="#000000",
        font=("Hanuman Regular", 16 * -1)
    )

    canvas.create_text(
        145.0,
        366.0,
        anchor="nw",
        text="Admin",
        fill="#000000",
        font=("Hanuman Regular", 15 * -1)
    )

    canvas.create_text(
        145.0,
        397.0,
        anchor="nw",
        text="Employee/Staff",
        fill="#000000",
        font=("Hanuman Regular", 15 * -1)
    )
    window.resizable(False, False)
    window.mainloop()

if __name__ == "__main__":
    create_registration_window()
