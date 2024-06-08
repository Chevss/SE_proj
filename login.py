from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox
from pathlib import Path
import secrets
import hashlib
import sqlite3

conn = sqlite3.connect('accounts.db')
cursor = conn.cursor()

def hash_password(password, salt):
    salted_password = password + salt
    return hashlib.sha256(salted_password.encode()).hexdigest()

def hash_username(username):
    return hashlib.sha256(username.encode()).hexdigest()

def check_loa(get_loa):
    if get_loa == "admin":
        import menu_ad
        menu_ad.create_menu_ad_window()
    else:
        import menu_em
        menu_em.create_menu_em_window()

def get_LOA(username):
    hashed_username = hash_username(username)

    cursor.execute("SELECT Loa FROM accounts WHERE username =?", (hashed_username,))
    row = cursor.fetchone()
    if row:
        return row[0]
    else:
        return None

def get_stored_hashed_password(username):
    hashed_username = hash_username(username)
    cursor.execute("SELECT salt, hashed_password FROM accounts WHERE username =?", (hashed_username,))
    row = cursor.fetchone()
    if row:
        return row[0], row[1]
    else:
        return None, None

def check_credentials(username, password, user_entry, pass_entry, window):
    salt, stored_hashed_password = get_stored_hashed_password(username)
    if salt and stored_hashed_password:
        hashed_password = hash_password(password, salt)
        if hashed_password == stored_hashed_password:
            messagebox.showinfo("Success", "Login successful!")
            window.destroy()
            return check_loa(get_LOA(username))
        else:
            messagebox.showerror("Error", "Incorrect password.")
            user_entry.delete(0, 'end')
            pass_entry.delete(0, 'end')
    else:
        messagebox.showerror("Error", "Username not found.")
        user_entry.delete(0, 'end')
        pass_entry.delete(0, 'end')

def create_login_window():
    conn = sqlite3.connect('accounts.db')
    cursor = conn.cursor()
    
    window = Tk()
    
    OUTPUT_PATH = Path(__file__).parent
    # ASSETS_PATH = OUTPUT_PATH / Path(r"C:/Users/TIPQC/Downloads/SE_proj-main/assets/Login")
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:/Users/katsu/Documents/GitHub/SE_proj/assets/Login")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    def on_text_click(event):
        canvas.itemconfig(forgot_pass, fill="red")

    def on_text_hover(event):
        canvas.itemconfig(forgot_pass, fill="green")

    def on_text_leave(event):
        canvas.itemconfig(forgot_pass, fill="blue")

    def exit():
        conn.close()
        window.destroy()

    window.title("Login")
    window.geometry("600x400")
    window.configure(bg="#FFE1C6")

    window_width, window_height = 600, 400
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Set the window geometry and position
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
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        300.0,
        84.0,
        image=image_image_1
    )

    pass_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    pass_bg_1 = canvas.create_image(
        300.5,
        284.0,
        image=pass_image_1
    )
    pass_entry = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        font=("Hanuman Regular", 24 * -1),
        show="*"
    )
    pass_entry.place(
        x=119.0,
        y=265.0,
        width=363.0,
        height=36.0,
    )

    user_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    user_bg_2 = canvas.create_image(
        300.5,
        219.0,
        image=user_image_2
    )
    user_entry = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        font=("Hanuman Regular", 24 * -1)
    )
    user_entry.place(
        x=119.0,
        y=200.0,
        width=363.0,
        height=36.0
    )

    canvas.create_text(
        119.0,
        176.0,
        anchor="nw",
        text="Username",
        fill="#000000",
        font=("Hanuman Regular", 16 * -1)
    )

    canvas.create_text(
        119.0,
        241.0,
        anchor="nw",
        text="Password",
        fill="#000000",
        font=("Hanuman Regular", 16 * -1)
    )

    forgot_pass = canvas.create_text(
        380.0,
        305.0,
        anchor="nw",
        text="Forgot Password?",
        fill="blue",
        font=("Hanuman Regular", 12 * -1)
    )
    canvas.tag_bind(forgot_pass, "<Button-1>", on_text_click)
    canvas.tag_bind(forgot_pass, "<Enter>", on_text_hover)
    canvas.tag_bind(forgot_pass, "<Leave>", on_text_leave)

    exit_image = PhotoImage(
        file=relative_to_assets("button_1.png"))
    exit_ = Button(
        image=exit_image,
        borderwidth=0,
        highlightthickness=0,
        command=exit,
        relief="flat"
    )
    exit_.place(
        x=349.0,
        y=325.0,
        width=133.0,
        height=37.0
    )

    login_image = PhotoImage(
        file=relative_to_assets("button_2.png"))
    login_ = Button(
        image=login_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: check_credentials(user_entry.get(), pass_entry.get(), user_entry, pass_entry, window),
        relief="flat"
    )
    login_.place(
        x=119.0,
        y=325.0,
        width=133.0,
        height=37.0
    )
    
    window.resizable(False, False)
    window.mainloop()

if __name__ == "__main__":
    create_login_window()
