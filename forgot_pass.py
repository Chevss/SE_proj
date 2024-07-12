from pathlib import Path
from tkinter import Button, Canvas, Entry, messagebox, Tk
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import smtplib
import sqlite3
import string

# From user made modules
from client import send_query
from user_logs import log_actions
import new_pass
import shared_state

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\Forgot_pass")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def generate_verification_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def send_verification_email(to_email, code):
    from_email = 'trimarkcstest@outlook.com'
    from_password = '1ZipJM2DsVnRoBkmVVKRCm0e8c6NniwhjW1FEWEC8n5Y'

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = 'Your Verification Code'

    body = f"Your verification code is: {code}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def create_forgot_pass_window():
    global window
    window = Tk()
    window.title("Forgot Password")
    window.geometry("600x400")
    window.configure(bg="#FFE1C6")

    window_width, window_height = 600, 400
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    canvas = Canvas(window, bg="#FFE1C6", height=400, width=600, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    verification_code_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=1, font=("Hanuman Regular", 24 * -1))
    verification_code_entry.place(x=119.0, y=237.0, width=363.0, height=36.0)

    email_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=1, font=("Hanuman Regular", 24 * -1))
    email_entry.place(x=119.0, y=113.0, width=363.0, height=36.0)

    canvas.create_text(119.0, 89.0, anchor="nw", text="E-Mail", fill="#000000", font=("Hanuman Regular", 16 * -1))
    canvas.create_text(119.0, 213.0, anchor="nw", text="Verification Code", fill="#000000", font=("Hanuman Regular", 16 * -1))
    
    def go_to_window(windows):
        window.destroy()
        if windows == "Cancel":
            import login
            login.create_login_window()

    cancel_button = Button(window, text="Cancel", font=("Hanuman Regular", 16), command=lambda: go_to_window("Cancel"), bg="white")
    cancel_button.place(x=415.0, y=336.0, width=133.0, height=37.0)

    # Get username of the input email address, because no user is not logged in (current_user = None)
    def get_username_by_email(email):
        query = "SELECT Username FROM accounts WHERE Email = ?"
        params = (email,)
        response = send_query(query, params)
        
        if response and len(response) > 0:
            # Assuming response is a list of tuples, extract the username
            username = response[0][0]
            log_actions(email, action=f"{email} sends a verification code")
            return username
        else:
            return None
        
    # Generate and send the verification code
    def handle_send_code():
        email = email_entry.get()
        global verification_code
        verification_code = generate_verification_code()
        shared_state.current_user = get_username_by_email(email)

        if shared_state.current_user:
            if send_verification_email(email, verification_code):
                messagebox.showinfo("Success", "Verification code sent to your email.")
                action = "Forgot password and requested a code for password change."
                log_actions(shared_state.current_user, action)
            else:
                messagebox.showerror("Error", "Failed to send verification code.")
        else:
            messagebox.showerror("Error", "No account found with that email address.")

    send_code_button = Button(window, text="Send Code", font=("Hanuman Regular", 16), bg="#FC7373", fg='white', command=handle_send_code)
    send_code_button.place(x=233.0, y=163.0, width=133.0, height=37.0)

    # Verify the entered code
    def handle_verify_code():
        entered_code = verification_code_entry.get()
        entered_email = email_entry.get()  # Retrieve email before destroying window
        if entered_code == verification_code:
            messagebox.showinfo("Success", "Verification successful!")
            action = "Code verified."
            log_actions(shared_state.current_user, action)
            window.destroy()  # Destroy window before calling new_pass.create_new_pass_window

            # Call create_new_pass_window from new_pass.py with email argument
            new_pass.create_new_pass_window(entered_email)
        else:
            messagebox.showerror("Error", "Invalid verification code.")

    verify_button = Button(window, text="Verify", font=("Hanuman Regular", 16), bg="#FC7373", fg='white', command=handle_verify_code)
    verify_button.place(x=250.0, y=287.0, width=100.0, height=37.0)

    canvas.create_rectangle(179.0, 20.0, 420.0, 76.0, fill="#FB7373", outline="")
    canvas.create_text(210.0, 32.0, anchor="nw", text="Forgot Password", fill="#FFFFFF", font=("Hanuman Regular", 24 * -1))
    
    window.resizable(False, False)
    window.mainloop()

if __name__ == "__main__":
    create_forgot_pass_window()
