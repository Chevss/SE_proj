import hashlib
import sqlite3
from pathlib import Path
from tkinter import BooleanVar, Button, Canvas, Checkbutton, Entry, messagebox, PhotoImage, Tk
from PIL import Image, ImageTk
import shared_state
from user_logs import log_actions

# Global variables
conn = sqlite3.connect('Trimark_construction_supply.db')
cursor = conn.cursor()

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\Login")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def hash_password(password, salt):
    salted_password = password + salt
    return hashlib.sha256(salted_password.encode()).hexdigest()

def get_stored_hashed_password(username):
    cursor.execute("SELECT salt, password FROM accounts WHERE username =? AND is_void = 0", (username,))
    row = cursor.fetchone()
    if row:
        return row[0], row[1]
    else:
        return None, None
    
def get_loa(username):
    cursor.execute("SELECT Loa FROM accounts WHERE username =? AND is_void = 0", (username,))
    row = cursor.fetchone()
    if row:
        return row[0]
    else:
        return None

def go_to_window(windows):
    window.destroy()
    if windows == "forgot pass":
        log_actions(shared_state.current_user, action="Someone goes to 'forgot password?")
        import forgot_pass
        forgot_pass.create_forgot_pass_window()
    elif windows == "pos_main":
        import pos_admin
        pos_admin.create_pos_admin_window()

def get_user_status(username):
    cursor.execute("SELECT is_void FROM accounts WHERE username =?", (username,))
    row = cursor.fetchone()
    if row:
        if row[0] == 0:
            return "Active"
        return row[0]
    else:
        return None

# Check credentials and initiate login process.
def check_credentials(username, password, user_entry, pass_entry, window):
    global current_user

    if not username or not password:
        messagebox.showerror("Error", "Please enter your username and password.")
        return
    
    salt, stored_hashed_password = get_stored_hashed_password(username)
    
    if salt and stored_hashed_password:
        hashed_password = hash_password(password, salt)
        if hashed_password == stored_hashed_password:
            loa = get_loa(username)
            if loa is not None:
                user_status = get_user_status(username)  # Assuming you have a function to get user status
                if user_status is not None:
                    if user_status == 0:  # User is available
                        messagebox.showinfo("Success", "Login successful!")
                        log_actions(username, action = "Logged In")
                        shared_state.current_user = username
                        shared_state.current_user_loa = loa  # Store the LOA
                        go_to_window("pos_main")
                        window.destroy()
                    elif user_status == 1:  # User is unavailable
                        messagebox.showerror("Error", "User is currently Inactive.\nContact your immediate Supervisor to Reactivate your account")
                        log_actions(username, action=f"{username} tried to logged in but his account is inactive")
                    else:
                        messagebox.showerror("Error", "Invalid user status.")
                else:
                    messagebox.showerror("Error", "Unable to retrieve user status.")
            else:
                messagebox.showerror("Error", "Unable to retrieve access level.")
        else:
            messagebox.showerror("Error", "Incorrect password.")
            log_actions(username, action=f"{username} tried to logged in but the entered password is incorrect")
            pass_entry.delete(0, 'end')
    else:
        messagebox.showerror("Error", "Username not found.")
        log_actions(username, action="{username} tried to logged in but this username is not registered")
        user_entry.delete(0, 'end')

def create_login_window():
    global window
    window = Tk()
    window.title("Login")
    window.geometry("600x400")
    window.configure(bg="#FFE1C6")
    
    def exit():
        conn.close()
        window.destroy()

    window_width, window_height = 600, 400
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Set the window geometry and position
    window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    canvas = Canvas(window, bg="#FFE1C6", height=400, width=600, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    original_image = Image.open(relative_to_assets("Tri-mark Logo.png"))
    resized_image = original_image.resize((350, 150))

    # Convert the resized image to a PhotoImage object
    image_image_1 = ImageTk.PhotoImage(resized_image)

    # Create the image on the canvas
    image_1 = canvas.create_image(300.0, 84.0, image=image_image_1)

    user_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Hanuman Regular", 24 * -1))
    user_entry.place(x=119.0, y=195.0, width=363.0, height=36.0) 

    pass_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Hanuman Regular", 24 * -1), show="•")
    pass_entry.place(x=119.0, y=258.0, width=363.0, height=36.0)

    canvas.create_text(119.0, 170.0, anchor="nw", text="Username", fill="#000000", font=("Hanuman Regular", 16 * -1))
    canvas.create_text(119.0, 236.0, anchor="nw", text="Password", fill="#000000", font=("Hanuman Regular", 16 * -1))

    forgot_pass = canvas.create_text(380.0, 305.0, anchor="nw", text="Forgot Password?", fill="blue", font=("Hanuman Regular", 12 * -1))

    canvas.tag_bind(forgot_pass, "<Button-1>", lambda event: go_to_window("forgot pass"))
    canvas.tag_bind(forgot_pass, "<Enter>", lambda event: canvas.itemconfig(forgot_pass, fill="green"))
    canvas.tag_bind(forgot_pass, "<Leave>", lambda event: canvas.itemconfig(forgot_pass, fill="blue"))

    exit_image = PhotoImage(file=relative_to_assets("button_1.png"))
    exit_ = Button(image=exit_image, borderwidth=0, highlightthickness=0, command=exit, relief="flat")
    exit_.place(x=349.0, y=325.0, width=133.0, height=37.0)

    login_image = PhotoImage(file=relative_to_assets("button_2.png"))
    login_ = Button(image=login_image, borderwidth=0, highlightthickness=0, command=lambda: check_credentials(user_entry.get(), pass_entry.get(), user_entry, pass_entry, window), relief="flat")
    login_.place(x=119.0, y=325.0, width=133.0, height=37.0)

    show_password_var = BooleanVar()

    def toggle_password_visibility():
        if show_password_var.get():
            pass_entry.config(show="")
        else:
            pass_entry.config(show="•")

    show_password_checkbox = Checkbutton(window, text="Show Password", variable=show_password_var, bg="#FFE1C6", font=("Hanuman Regular", 10), command=toggle_password_visibility)
    show_password_checkbox.place(x=119.0, y=299)
    
    window.resizable(False, False)
    window.mainloop()

if __name__ == "__main__":
    create_login_window()
