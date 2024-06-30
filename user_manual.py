import json
import os
from tkinter import Tk, Canvas, Text, Button, Scrollbar, END, filedialog
from PIL import Image, ImageTk
from portalocker import lock, unlock, LOCK_EX
import shared_state
from functools import partial

# Load or initialize the About data
ABOUT_FILE = 'user_manual.json'

def load_about():
    try:
        with open(ABOUT_FILE, 'r') as file:
            data = json.load(file)
            if isinstance(data, dict):
                return data
            return {}
    except FileNotFoundError:
        return {}

def save_about():
    with open(ABOUT_FILE, 'w') as file:
        lock(file, LOCK_EX)
        json.dump(shared_state.abouts, file)
        unlock(file)
    os.chmod(ABOUT_FILE, 0o600)

shared_state.abouts = load_about()

def center_window(curr_window, win_width, win_height):
    window_width, window_height = win_width, win_height
    screen_width = curr_window.winfo_screenwidth()
    screen_height = curr_window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    curr_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

def create_user_manual_window():
    global window
    window = Tk()
    window.geometry("972x835")
    window.configure(bg="#FFE1C6")

    center_window(window, 972, 835)

    canvas = Canvas(
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
        365.0,
        40.0,
        608.0,
        139.0,
        fill="#5CB0FF",
        outline=""
    )
    canvas.create_text(
        432.0,
        64.0,
        anchor="nw",
        text="About",
        fill="#000000",
        font=("Hanuman Regular", 40 * -1)
    )

    loa = shared_state.current_user_loa
    if loa == "admin":
        edit_user_manual_button = Button(
            text="Edit About",
            font=("Hanuman Regular", 16),
            command=open_edit_about_window,
            bg="#F8D48E",
            relief="raised"
        )
        edit_user_manual_button.place(x=415.0, y=727.0, height=50, width=125)

    back_button = Button(
        text="Back",
        font=("Hanuman Regular", 16),
        command=lambda: go_to_window("pos"),
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
        highlightthickness=0
    )
    user_manual_entry.place(
        x=102.0,
        y=325.0,
        width=768.0,
        height=366.0
    )

    # Add scrollbars to the Text widget
    vsb = Scrollbar(window, orient="vertical", command=user_manual_entry.yview)
    vsb.place(x=870, y=325, height=366)
    user_manual_entry.config(yscrollcommand=vsb.set)

    display_about(user_manual_entry)

    window.resizable(False, False)
    window.mainloop()

def go_to_window(windows):
    window.destroy()
    if windows == "pos":
        import pos_admin
        pos_admin.create_pos_admin_window()

def open_edit_about_window():
    edit_window = Toplevel(window)
    edit_window.geometry("600x400")
    edit_window.title("Edit About")

    center_window(edit_window, 600, 400)

    Label(edit_window, text="Edit About Information", font=("Hanuman Regular", 20)).pack(pady=20)

    # Entry widget for editing
    edit_entry = Text(edit_window, wrap='word', height=15, width=60)
    edit_entry.pack(pady=10)

    # Populate with existing about content
    current_about = shared_state.abouts.get('about_text', '')
    edit_entry.insert(END, current_about)

    # Save button
    save_button = Button(edit_window, text="Save", font=("Hanuman Regular", 16),
                         command=lambda: save_edited_about(edit_entry.get("1.0", "end-1c"), edit_window))
    save_button.pack(pady=20)

def save_edited_about(new_about, edit_window):
    shared_state.abouts['about_text'] = new_about
    save_about()
    edit_window.destroy()
    display_about(user_manual_entry)

def display_about(text_widget):
    about_text = shared_state.abouts.get('about_text', '')
    text_widget.delete(1.0, END)
    text_widget.insert(END, about_text)

if __name__ == "__main__":
    create_user_manual_window()
