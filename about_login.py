import json
import os
import tkinter as tk
from tkinter import Tk, Canvas, Text, Button, Toplevel, END, Label, filedialog, PhotoImage
from PIL import Image, ImageTk
from portalocker import lock, unlock, LOCK_EX
from pathlib import Path
import base64
from io import BytesIO
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

def update_about_entry():
    display_about(about_entry)

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
    window = tk.Tk()
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
    about_entry = tk.Text(
        window,
        bd=0,
        bg="#FFE1C6",  # Match background color
        fg="#000716",
        highlightthickness=0,
        wrap='word'  # Prevent cutting words
    )
    about_entry.place(
        x=102.0,
        y=325.0,
        width=768.0,
        height=366.0
    )

    update_about_entry()  # Initial update of about_entry

    window.resizable(False, False)
    window.mainloop()


def resize_image(image_path, width, height):
    # Load the image using Pillow
    original_image = Image.open(image_path)
    
    # Resize the image using BILINEAR filter
    resized_image = original_image.resize((width, height), Image.BILINEAR)
    
    # Convert the Pillow image to PhotoImage
    return ImageTk.PhotoImage(resized_image)

def display_about(about_entry):
    about_entry.config(state='normal')
    about_entry.delete(1.0, END)
    if 'Details' in shared_state.abouts:
        about_text = shared_state.abouts['Details']
    else:
        about_text = "<Missing Details>"

    about_entry.insert(END, about_text + '\n\n')

    # Calculate number of lines and length of each line
    num_lines = len(about_text.split('\n'))
    max_line_length = max(len(line) for line in about_text.split('\n'))

    # Calculate x and y offsets to center text
    text_width = max_line_length * 10  # Approximate width of characters
    text_height = num_lines * 25  # Approximate height of characters
    x_offset = (768 - text_width) / 2  # 768 is the width of about_entry
    y_offset = (366 - text_height) / 2  # 366 is the height of about_entry

    # Tag and configure to center text
    about_entry.tag_configure('center', justify='center')
    about_entry.tag_add('center', '1.0', 'end')
    about_entry.tag_configure('big', font=('Hanuman Regular', 20))
    about_entry.tag_add('big', '1.0', 'end')

    about_entry.insert(tk.END, "Developers:\n")
    # Developer 1
    global dev1_image
    dev1_image_path = "assets/About/gaiti1x1.jpg"
    dev1_image = resize_image(dev1_image_path, 150, 150)  # Adjust width and height as needed
    about_entry.image_create(tk.END, image=dev1_image)
    about_entry.insert(tk.END, "\n")
    about_entry.insert(tk.END, "Gaiti, Chevy Joel B.\n")
    about_entry.insert(tk.END, "qcjbgaiti@tip.edu.ph\n")
    about_entry.insert(tk.END, "Bachelor of Science in Computer Science\n")

    # Developer 2
    global dev2_image
    dev2_image_path = "assets/About/r8qbozta.png"
    dev2_image = resize_image(dev2_image_path, 150, 150)  # Adjust width and height as needed
    about_entry.image_create(tk.END, image=dev2_image)
    about_entry.insert(tk.END, "\n")
    about_entry.insert(tk.END, "Tan, Thady Morven T.\n")
    about_entry.insert(tk.END, "qtmttan@tip.edu.ph\n")
    about_entry.insert(tk.END, "Bachelor of Science in Computer Science\n")

    # Developer 3
    global dev3_image
    dev3_image_path = "assets/Login/image_1.png"
    dev3_image = resize_image(dev3_image_path, 150, 150)  # Adjust width and height as needed
    about_entry.image_create(tk.END, image=dev3_image)
    about_entry.insert(tk.END, "\n")
    about_entry.insert(tk.END, "Gaiti, Chevy Joel B.\n")
    about_entry.insert(tk.END, "qcjbgaiti@tip.edu.ph\n")
    about_entry.insert(tk.END, "Bachelor of Science in Computer Science\n")


    if 'Logo' in shared_state.abouts:
        try:
            logo_base64 = shared_state.abouts['Logo']
            decoded_data = base64.b64decode(logo_base64)
            logo_image = Image.open(BytesIO(decoded_data))
            logo_image = logo_image.resize((350, 150), Image.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo_image)

            # Create a Label to display the logo image
            logo_label = Label(window, image=logo_photo)
            logo_label.image = logo_photo  # Keep a reference to prevent garbage collection
            logo_label.place(x=305, y=150)  # Adjust the coordinates as needed
            
        except Exception as e:
            print(f"Error displaying logo: {e}")

    about_entry.config(state='disabled')

def load_image(image_path):
    try:
        image = Image.open(image_path)
        image = image.resize((100, 100), Image.LANCZOS)  # Resize image as needed
        return ImageTk.PhotoImage(image)
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

# if __name__ == "__main__":
#     create_about_window()
