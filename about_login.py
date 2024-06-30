import json
import os
import base64
from tkinter import Tk, Canvas, Text, Button, Toplevel, END, Label, filedialog, Scrollbar
from PIL import Image, ImageTk
from io import BytesIO
from portalocker import lock, unlock, LOCK_EX
import shared_state

# Load or initialize the About data
ABOUT_FILE = 'abouts.json'

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
abouts = load_about()

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
        y=325.0,
        width=768.0,
        height=366.0
    )

    # vsb = Scrollbar(window, orient="vertical", command=about_entry.yview)
    # vsb.place(x=870, y=325, height=366)

    # about_entry.configure(yscrollcommand=vsb.set)

    display_about(about_entry)

    window.resizable(False, False)
    window.mainloop()

def display_about(about_entry):
    about_entry.delete(1.0, END)
    if 'Details' in shared_state.abouts:
        about_entry.insert(END, f"{shared_state.abouts['Details']}\n", 'bold')
        about_entry.tag_configure('bold', font=('Hanuman Regular', 20))
    else:
        about_entry.insert(END, f"<Missing Details>\n", 'bold')
        about_entry.tag_configure('bold', font=('Hanuman Regular', 20))
    if 'Logo' in shared_state.abouts:
        try:
            logo_data = base64.b64decode(shared_state.abouts['Logo'])
            logo_image = Image.open(BytesIO(logo_data))
            logo_image = logo_image.resize((350, 150), Image.LANCZOS)  # Resize the image
            logo_photo = ImageTk.PhotoImage(logo_image)
            logo_label = Label(window, image=logo_photo)
            logo_label.image = logo_photo
            logo_label.place(x=305, y=150)
        except Exception as e:
            print(f"Error displaying logo: {e}")
    about_entry.config(state='disabled')

def open_edit_about_window():
    edit_window = Toplevel(window)
    edit_window.geometry("400x400")
    edit_window.title("Edit About")

    center_window(edit_window, 400, 400)
    Label(edit_window, text='Edit About').pack(pady=10)

    logo_path_label = Label(edit_window, text='No file chosen')
    logo_path_label.pack(pady=5)

    def upload_logo():
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            logo_path_label.config(text=file_path)
            try:
                with open(file_path, 'rb') as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                    shared_state.abouts['Logo'] = encoded_string
                    shared_state.save_about()  # Save changes and trigger event
            except Exception as e:
                print(f"Error encoding logo: {e}")

    upload_logo_button = Button(edit_window, text="Upload Logo", command=upload_logo)
    upload_logo_button.pack(pady=5)

    edit_entry = Text(
        edit_window,
        bd=0,
        bg="#FFFFFF",
        fg="#000000",
        highlightthickness=0
    )
    edit_entry.place(x=50, y=120, width=300, height=200)
    if 'Details' in abouts:
        edit_entry.insert(1.0, abouts['Details'])

    def save_edited_about():
        abouts['Details'] = edit_entry.get('1.0', END).strip()
        save_about()
        display_about(about_entry)
        edit_window.destroy()

    save_button = Button(edit_window, text="Save Changes", command=save_edited_about)
    save_button.place(x=150, y=350, width=100, height=30)

if __name__ == "__main__":
    create_about_window()
