from pathlib import Path
from tkinter import BooleanVar, Button, Canvas, Checkbutton, Entry, messagebox, PhotoImage, Tk
from PIL import Image, ImageTk
from io import BytesIO
import base64
import sqlite3

# From user made modules
from client import send_query
from salt_and_hash import hash_password
from shared_state import abouts
from user_logs import log_actions
import shared_state

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\Login")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def get_stored_hashed_password(username):
    query = "SELECT salt, password FROM accounts WHERE username =? AND is_void = 0"
    result = send_query(query, (username,))
    if result:
        return result[0][0], result[0][1]
    else:
        return None, None

def go_to_window(windows):
    window.destroy()
    if windows == "forgot pass":
        log_actions(shared_state.current_user, action="Someone goes to 'forgot password?")
        import forgot_pass
        forgot_pass.create_forgot_pass_window()
    elif windows == "pos_main":
        import pos_admin
        pos_admin.create_pos_admin_window()
    elif windows == "about_login":
        import about_login
        about_login.create_about_window()

def load_image_from_about():
    if 'Logo' in abouts:
        try:
            logo_base64 = abouts['Logo']
            
            # Ensure the data is a valid string
            if isinstance(logo_base64, str):
                try:
                    logo_data = base64.b64decode(logo_base64)
                    logo_image = Image.open(BytesIO(logo_data))
                    resized_image = logo_image.resize((350, 150), Image.LANCZOS)
                    return ImageTk.PhotoImage(resized_image)
                except base64.binascii.Error as b64_error:
                    print(f"Base64 decoding error: {b64_error}")
                except Exception as img_error:
                    print(f"Error opening image: {img_error}")
            else:
                print("Error: Logo data is not a string")
        except Exception as e:
            print(f"Error loading logo from abouts: {e}")
    return None

def get_user_status(username):
    query = "SELECT is_void FROM accounts WHERE username =?"
    result = send_query(query, (username,))
    if result:
        if result[0][0] == 0:
            return "Active"
        elif result[0][0] == 1:
            return "Inactive"
    else:
        return None

def get_loa(username):
    query = "SELECT LOA FROM accounts WHERE username =?"
    result = send_query(query, (username,))
    if result:
        return result[0][0]
    else:
        return None

# Check credentials and initiate login process.
def check_credentials(username, password):
    user_status = get_user_status(username)
    print(username)
    print(password)
    print(user_entry)
    print(pass_entry)
    print(user_status)
    print("User Status: ", user_status) # DEBUG
    if user_status == "Inactive":
        messagebox.showerror("Error", "User is currently Inactive.\nContact your immediate Supervisor to Reactivate your account")
        log_actions(username, action=f"{username} tried to log in but their account is inactive")
        return
    
    salt, stored_hashed_password = get_stored_hashed_password(username)

    if salt and stored_hashed_password:
        hashed_password = hash_password(password, salt)
        if hashed_password == stored_hashed_password:
            loa = get_loa(username)
            print("LOA: ", loa) # DEBUG
            if loa is not None:
                if user_status == "Active":
                    messagebox.showinfo("Success", "Login successful!")
                    log_actions(username, action = "Logged In")
                    shared_state.current_user = username
                    shared_state.current_user_loa = loa
                    go_to_window("pos_main")
                else:
                    messagebox.showerror("Error", "Invalid user status.")
            else:
                messagebox.showerror("Error", "Unable to retrieve access level.")
        else:
            messagebox.showerror("Error", "Incorrect password.")
            log_actions(username, action=f"{username} tried to logged in but the entered password is incorrect")
            pass_entry.delete(0, 'end')
    else:
        messagebox.showerror("Error", "Username not found.")
        log_actions(username, action=f"{username} tried to logged in but this username is not registered")
        user_entry.delete(0, 'end')

def create_login_window():
    global window, user_entry, pass_entry
    window = Tk()
    window.title("Login")
    window.geometry("600x400")
    window.configure(bg="#FFE1C6")
    
    def exit():
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

    def handle_abouts_change():
        image_image_1 = load_image_from_about()
        if image_image_1:
            canvas.itemconfig(image_1, image=image_image_1)
            canvas.image = image_image_1

    shared_state.event_dispatcher.add_handler(handle_abouts_change)

    image_image_1 = load_image_from_about()

    if image_image_1:
        canvas = Canvas(window, bg="#FFE1C6", height=400, width=600, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)
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

    about = canvas.create_text(555.0, 385.0, anchor="nw", text="About", fill="black", font=("Hanuman Regular", 12 * -1))

    canvas.tag_bind(about, "<Button-1>", lambda event: go_to_window("about_login"))
    canvas.tag_bind(about, "<Enter>", lambda event: canvas.itemconfig(about, fill="red"))
    canvas.tag_bind(about, "<Leave>", lambda event: canvas.itemconfig(about, fill="black"))

    exit_ = Button(text="Exit",font=("Hanuman Regular", 14), command=exit, relief="raised", bg="white")
    exit_.place(x=349.0, y=325.0, width=133.0, height=37.0)

    login_ = Button(text="Login", font=("Hanuman Regular", 14), command=lambda: check_credentials(user_entry.get(), pass_entry.get()), bg="#FF7676", fg='white',relief="raised")
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
