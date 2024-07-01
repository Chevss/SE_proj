import json
import os
import tkinter as tk
from tkinter import Text, Button, DISABLED, messagebox
from portalocker import lock, unlock, LOCK_EX
import shared_state

# Load or initialize the User manual data
USER_MANUAL_FILE = 'user_manual.json'

def load_user_manual():
    try:
        with open(USER_MANUAL_FILE, 'r') as file:
            data = json.load(file)
            if isinstance(data, dict):
                return data
            return {}
    except FileNotFoundError:
        return {}

def save_manual(content):
    user_manual_data = {'manual_content': content}
    try:
        with open(USER_MANUAL_FILE, 'w') as file:
            lock(file, LOCK_EX)
            json.dump(user_manual_data, file)
            unlock(file)
        os.chmod(USER_MANUAL_FILE, 0o600)
        messagebox.showinfo("Saved", "Manual content saved successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save manual content: {str(e)}")
        # Log the exception for further debugging
        print(f"Error saving manual content: {str(e)}")

def open_edit_manual_window():
    edit_window = tk.Toplevel()
    edit_window.title("Edit Manual")
    edit_window.geometry("600x500")

    center_window(edit_window, 600,500)

    edit_text = Text(edit_window)
    edit_text.pack(expand=True, fill="both")

    # Load existing manual content into the Text widget for editing
    user_manual_data = load_user_manual()
    if user_manual_data and 'manual_content' in user_manual_data:
        edit_text.insert("1.0", user_manual_data['manual_content'])

    def save_and_close():
        content = edit_text.get("1.0", "end-1c")
        save_manual(content)
        edit_window.destroy()
        update_user_manual_entry(content)

    save_button = Button(edit_window, text="Save", command=save_and_close)
    save_button.pack()

    edit_window.mainloop()

def update_user_manual_entry(content=None):
    if content is None:
        user_manual_data = load_user_manual()
        if user_manual_data and 'manual_content' in user_manual_data:
            content = user_manual_data['manual_content']

    user_manual_entry.config(state="normal")  # Enable editing temporarily
    user_manual_entry.delete("1.0", "end")
    user_manual_entry.insert("1.0", content)
    user_manual_entry.config(state=DISABLED)  # Disable editing again

def center_window(win, width, height):
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        win.geometry(f'{width}x{height}+{x}+{y}')

def create_user_manual_window():
    window = tk.Tk()
    window.geometry("972x835")
    window.configure(bg="#FFE1C6")

    center_window(window, 972, 835)

    canvas = tk.Canvas(
        window,
        bg="#FFE1C6",
        height=835,
        width=972,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)
    canvas.create_rectangle(
        395.0,
        40.0,
        588.0,
        99.0,
        fill="#5CB0FF",
        outline=""
    )
    canvas.create_text(
        408.0,
        50.0,
        anchor="nw",
        text="User Manual",
        fill="#000000",
        font=("Hanuman Regular", 30 * -1)
    )

    loa = shared_state.current_user_loa
    loa = "admin"
    if loa == "admin":
        edit_user_manual_button = Button(
            window,
            text="Edit Manual",
            font=("Hanuman Regular", 16),
            command=open_edit_manual_window,
            bg="#F8D48E",
            relief="raised"
        )
        edit_user_manual_button.place(x=415.0, y=727.0, height=50, width=125)

    back_button = Button(
        window,
        text="Back",
        font=("Hanuman Regular", 16),
        command=lambda: go_to_window(window, "pos"),
        bg="#FFFFFF",
        relief="raised"
    )
    back_button.place(x=785.0, y=727.0, height=50, width=125)

    global user_manual_entry
    user_manual_entry = Text(
        window,
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        state=DISABLED  # Make the Text widget initially non-editable
    )
    user_manual_entry.place(
        x=102.0,
        y=125.0,
        width=768.0,
        height=566.0
    )

    # Load manual content into the Text widget
    update_user_manual_entry()

    window.resizable(False, False)
    window.mainloop()

def go_to_window(curr_window, window_type):
    curr_window.destroy()
    if window_type == "pos":
        import pos_admin
        pos_admin.create_pos_admin_window()

if __name__ == "__main__":
    create_user_manual_window()
