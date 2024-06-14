# Standard Libraries and Tkinter GUI Toolkit Components
from email.mime.text import MIMEText
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, Radiobutton, StringVar, messagebox, OptionMenu
import hashlib, re, secrets, smtplib, sqlite3
from database import insert_account

# Database connection
conn = sqlite3.connect('accounts.db')
cursor = conn.cursor()

# Paths
OUTPUT_PATH = Path(__file__).parent
# ASSETS_PATH = OUTPUT_PATH / Path(r"C:/Users/katsu/Documents/GitHub/SE_proj/assets/Registration")
ASSETS_PATH = OUTPUT_PATH / Path(r"C:/Users/TIPQC/Desktop/SE_proj-main/assets/Registration")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Password and username utilities
def generate_salt():
    return secrets.token_hex(16)

def hash_password(password, salt):
    return hashlib.sha256((password + salt).encode()).hexdigest()

def hash_username(username):
    return hashlib.sha256(username.encode()).hexdigest()

def send_email(email, username, password):
    msg = MIMEText(f"Your username is: {username}\nYour temporary password is: {password}")
    msg['Subject'] = 'Registration Details'
    msg['From'] = 'trimarkcstest@outlook.com'
    msg['To'] = email

    with smtplib.SMTP('smtp-mail.outlook.com', 587) as server:
        server.starttls()
        server.login('trimarkcstest@outlook.com', '1ZipJM2DsVnRoBkmVVKRCm0e8c6NniwhjW1FEWEC8n5Y')
        server.sendmail('trimarkcstest@outlook.com', email, msg.as_string())

def generate_username(first_name, mi, last_name, suffix, loa):
    prefix = 'a' if loa == 'admin' else 'e'
    mi_part = mi if mi else ''
    suffix_part = suffix if suffix else ''
    return f"{prefix}{first_name[0].lower()}{mi_part.lower()}{last_name.lower()}{suffix_part.lower()}.tmcs"

def register_user(first_name, mi, last_name, suffix, contact_number, home_address, email, loa):
    if not first_name or not last_name or not contact_number or not home_address or not email:
        messagebox.showerror("Error", "All fields except Middle Initial and Suffix are required")
        return

    if not is_valid_name(first_name):
        messagebox.showerror("Error", "First name can only contain letters")
        return

    if not is_valid_name(last_name):
        messagebox.showerror("Error", "Last name can only contain letters")
        return

    if not is_valid_mi(mi):
        messagebox.showerror("Error", "Middle Initial can only contain up to 2 letters")
        return

    if not is_valid_contact_number(contact_number):
        messagebox.showerror("Error", "Contact number must be 11 digits long")
        return

    valid_email, email_message = is_valid_email(email)
    if not valid_email:
        messagebox.showerror("Error", email_message)
        return

    username = generate_username(first_name, mi, last_name, suffix, loa)

    cursor.execute("SELECT * FROM accounts WHERE Username = ?", (username,))
    if cursor.fetchone():
        messagebox.showerror("Error", "Username already exists")
        return

    cursor.execute("SELECT * FROM accounts WHERE Email = ?", (email,))
    if cursor.fetchone():
        messagebox.showerror("Error", "Email already exists")
        return

    password = secrets.token_urlsafe(10)  # Generate a random password

    salt = generate_salt()
    hashed_password = hash_password(password, salt)

    insert_account(loa, first_name, last_name, mi, suffix, contact_number, home_address, email, username, hashed_password, salt, 0)
    send_email(email, username, password)
    messagebox.showinfo("Success", "Registration successful. Your username and temporary password have been sent to your email.")


def create_registration_window():
    window = Tk()
    window.title("Registration")
    window.configure(bg="#FFE1C6")

    # Calculate the position for the window to be centered
    window_width, window_height = 600, 750
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Set the window geometry and position
    window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    canvas = Canvas(
        window,
        bg="#FFE1C6",
        height=750,
        width=600,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(272.5, 209.0, image=entry_image_1)
    last_name_entry = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        font=("Hanuman Regular", 20 * -1)
    )
    last_name_entry.place(x=119.0, y=190.0, width=307.0, height=36.0)

    entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(461.5, 144.0, image=entry_image_2)
    MI_entry = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        font=("Hanuman Regular", 20 * -1)
    )
    MI_entry.place(x=441.0, y=125.0, width=41.0, height=36.0)

    entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(272.5, 144.0, image=entry_image_3)
    first_name_entry = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        font=("Hanuman Regular", 20 * -1)
    )
    first_name_entry.place(x=119.0, y=125.0, width=307.0, height=36.0)

    canvas.create_text(
        119.0,
        98.0,
        anchor="nw",
        text="First Name",
        fill="#000000",
        font=("Hanuman Regular", 16 * -1)
    )

    canvas.create_text(
        447.0,
        98.0,
        anchor="nw",
        text="M.I.",
        fill="#000000",
        font=("Hanuman Regular", 16 * -1)
    )

    entry_image_4 = PhotoImage(file=relative_to_assets("entry_4.png"))
    entry_bg_4 = canvas.create_image(461.5, 209.0, image=entry_image_4)
    suffix_entry = StringVar()
    suffix_options = ["", "Jr", "Sr", "I", "II", "III"]
    suffix_menu = OptionMenu(window, suffix_entry, *suffix_options)
    suffix_menu.config(bg="#FFE1C6", font=("Hanuman Regular", 14 * -1))
    suffix_menu.place(x=441.0, y=190.0, width=41.0, height=36.0)

    canvas.create_text(
        439.0,
        166.0,
        anchor="nw",
        text="Suffix",
        fill="#000000",
        font=("Hanuman Regular", 16 * -1)
    )

    canvas.create_text(
        119.0,
        166.0,
        anchor="nw",
        text="Last Name",
        fill="#000000",
        font=("Hanuman Regular", 16 * -1)
    )

    entry_image_5 = PhotoImage(file=relative_to_assets("entry_5.png"))
    entry_bg_5 = canvas.create_image(300.5, 275.0, image=entry_image_5)
    contact_no_entry = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        font=("Hanuman Regular", 20 * -1)
    )
    contact_no_entry.place(x=119.0, y=256.0, width=363.0, height=36.0)

    canvas.create_text(
        119.0,
        232.0,
        anchor="nw",
        text="Contact Number",
        fill="#000000",
        font=("Hanuman Regular", 16 * -1)
    )

    entry_image_6 = PhotoImage(file=relative_to_assets("entry_6.png"))
    entry_bg_6 = canvas.create_image(300.5, 341.0, image=entry_image_6)
    address_entry = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        font=("Hanuman Regular", 20 * -1)
    )
    address_entry.place(x=119.0, y=322.0, width=363.0, height=36.0)

    canvas.create_text(
        119.0,
        298.0,
        anchor="nw",
        text="Home Address",
        fill="#000000",
        font=("Hanuman Regular", 16 * -1)
    )

    entry_image_7 = PhotoImage(file=relative_to_assets("entry_7.png"))
    entry_bg_7 = canvas.create_image(300.5, 403.0, image=entry_image_7)
    email_entry = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        font=("Hanuman Regular", 20 * -1)
    )
    email_entry.place(x=119.0, y=384.0, width=363.0, height=36.0)

    canvas.create_text(
        119.0,
        360.0,
        anchor="nw",
        text="Email Address",
        fill="#000000",
        font=("Hanuman Regular", 16 * -1)
    )

    canvas.create_text(119.0, 437.0, anchor="nw", text="Level of Access", fill="#000000", font=("Hanuman Regular", 16 * -1))

    loa_var = StringVar(value="employee")

    radio_admin = Radiobutton(
        window,
        text="Admin",
        variable=loa_var,
        value="admin",
        bg="#FFE1C6",
        font=("Hanuman Regular", 14 * -1)
    )
    radio_admin.place(x=145.0, y=464.0)

    radio_employee = Radiobutton(
        window,
        text="Employee/Staff",
        variable=loa_var,
        value="employee",
        bg="#FFE1C6",
        font=("Hanuman Regular", 14 * -1)
    )
    radio_employee.place(x=145.0, y=495.0)

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    back_button = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: back_to_menu_ad(window),
        relief="flat"
    )
    back_button.place(x=349.0, y=559.0, width=133.0, height=37.0)

    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    register_button = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: register_user(
            first_name_entry.get(), 
            MI_entry.get(), 
            last_name_entry.get(), 
            suffix_entry.get(), 
            contact_no_entry.get(), 
            address_entry.get(), 
            email_entry.get(), 
            loa_var.get()
        ),
        relief="flat"
    )
    register_button.place(x=119.0, y=559.0, width=133.0, height=37.0)

    canvas.create_rectangle(162.0, 21.0, 440.0, 85.0, fill="#FB7373", outline="")
    canvas.create_text(209.0, 29.0, anchor="nw", text="Registration", fill="#FFFFFF", font=("Hanuman Regular", 32 * -1))

    window.resizable(False, False)
    window.mainloop()

def back_to_menu_ad(window):
    window.destroy()
    from pos_admin import create_menu_ad_window
    create_menu_ad_window()

def is_valid_name(name):
    return bool(re.match(r'^[a-zA-Z]+$', name))

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

if __name__ == "__main__":
    create_registration_window()
