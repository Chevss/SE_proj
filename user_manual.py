import tkinter as tk
from tkinter import ttk, Tk
from PIL import Image, ImageTk
import fitz  # PyMuPDF

def center_window(curr_window, win_width, win_height):
    window_width, window_height = win_width, win_height
    screen_width = curr_window.winfo_screenwidth()
    screen_height = curr_window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    curr_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

def go_to_window():
    window.destroy()
    import help_ad
    help_ad.create_help_window()

def show_pdf(tab, pdf_path):
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    img = ImageTk.PhotoImage(img)
    label = tk.Label(tab, image=img)
    label.image = img  # Keep a reference to prevent garbage collection
    label.pack()

def create_users_manual_window():
    global window
    window = Tk()
    window.geometry("972x835")
    window.title("Users Manual")
    window.configure(bg="#FFE1C6")

    center_window(window, 972, 835)

    # Create a custom style for the notebook tabs
    style = ttk.Style()
    style.configure('Custom.TNotebook.Tab', font=('Hanuman Regular', 12))

    notebook = ttk.Notebook(window, width=972, height=835, style='Custom.TNotebook')
    notebook.pack(padx=25, pady=25)

    # Create tabs with corresponding PDF files
    tabs = [
        ("Login", "path/to/login.pdf"),
        ("POS", "path/to/pos.pdf"),
        ("Account", "path/to/account.pdf"),
        ("Reports", "path/to/reports.pdf"),
        ("Barcodes", "path/to/barcodes.pdf"),
        ("Inventory", "path/to/inventory.pdf"),
        ("Backup", "path/to/backup.pdf"),
        ("Restore", "path/to/restore.pdf")
    ]

    for tab_name, pdf_path in tabs:
        tab = ttk.Frame(notebook)
        notebook.add(tab, text=tab_name)
        show_pdf(tab, pdf_path)

    back_button = tk.Button(window, text="Back", command=go_to_window, font=("Hanuman Regular", 12))
    back_button.place(x=900, y=15)

    # Start the main loop
    window.mainloop()

if __name__ == "__main__":
    create_users_manual_window()
