import json
from tkinter import Tk, Canvas, Text, Button, Toplevel, END, messagebox, Label, Entry
from portalocker import lock, unlock, LOCK_EX
import shared_state

# Load or initialize the About data
ABOUT_FILE = 'faqs.json'

try:
    with open(ABOUT_FILE, 'r') as file:
        abouts = json.load(file)
except FileNotFoundError:
    abouts = []

def save_about():
    with open(ABOUT_FILE, 'w') as file:
        lock(file, LOCK_EX)  # Acquire an exclusive lock
        json.dump(abouts, file)
        unlock(file)  # Release the lock

def go_to_window(windows):
    window.destroy()
    if windows == "login":
        import login
        login.create_login_window()

def center_window(curr_window, win_width, win_height):
    window_width, window_height = win_width, win_height
    screen_width = curr_window.winfo_screenwidth()
    screen_height = curr_window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    curr_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

def create_about_window():
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
        outline="")

    canvas.create_text(
        432.0,
        64.0,
        anchor="nw",
        text="About",
        fill="#000000",
        font=("Hanuman Regular", 40 * -1)
    )

    edit_about_button = Button(text="Edit About", font=("Hanuman Regular", 16), command=open_edit_about_window, bg="#F8D48E", relief="raised")

    loa = shared_state.current_user_loa
    loa = "admin"
    if loa == "admin":
        edit_about_button.place(x=415.0, y=727.0, height=50, width=125)

    back_button = Button(text="Back", font=("Hanuman Regular", 16), command=lambda: go_to_window("login"), bg="#FFFFFF", relief="raised")
    back_button.place(x=785.0, y=727.0, height=50, width=125)

    global about_entry
    about_entry = Text(
        window,
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    about_entry.place(
        x=102.0,
        y=180.0,
        width=768.0,
        height=511.0
    )

    display_about(about_entry)

    # Display the FAQs in the required format
    window.resizable(False, False)
    window.mainloop()

def display_about(about_entry):
    about_entry.delete(1.0, END)
    for i, faq in enumerate(abouts, 1):
        if 'Details' in faq:
            about_entry.insert(END, f"{i}.) {faq['Details']}\n", 'bold')
            about_entry.tag_configure('bold', font=('Hanuman Regular', 20))
        else:
            about_entry.insert(END, f"{i}.) <Missing Details>\n", 'bold')
            about_entry.tag_configure('bold', font=('Hanuman Regular', 20))
    about_entry.config(state='disabled')


def open_edit_about_window():
    edit_window = Toplevel(window)
    edit_window.geometry("400x300")
    edit_window.title("Edit About")

    center_window(edit_window, 400, 300)
    Label(edit_window, text='Edit About').pack(pady=10)
    edit_entry_1 = Text(
        edit_window,
        bd=0,
        bg="#FFFFFF",
        fg="#000000",
        highlightthickness=0
    )
    edit_entry_1.place(x=50, y=50, width=300, height=200)

    # Function to save changes and update entry_1 in main window
    def save_edited_about(edit_entry):
        about_entry.config(state='normal')
        selected_index = about_entry.index('1.0')
        for about in abouts:
            about['Details'] = edit_entry
            save_about()
            about_entry.destroy()
            edit_window.destroy()
            display_about(about_entry)
            return

    save_button = Button(edit_window, text="Save Changes", command=lambda: save_edited_about(edit_entry_1.get('1.0', END)))
    save_button.place(x=150, y=255, width=100, height=30)

if __name__ == "__main__":
    create_about_window()
