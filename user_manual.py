import tkinter as tk
from tkinter import ttk, Tk, Canvas, Scrollbar
from PIL import Image, ImageTk
import fitz  # PyMuPDF

class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        canvas = Canvas(self)
        scrollbar = Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

def center_window(curr_window, win_width, win_height):
    window_width, window_height = win_width, win_height
    screen_width = curr_window.winfo_screenwidth()
    screen_height = curr_window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    curr_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

def go_to_window():
    window.destroy()
    import pos_admin
    pos_admin.create_pos_admin_window()

def show_pdf(tab, pdf_path):
    doc = fitz.open(pdf_path)
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img = ImageTk.PhotoImage(img)
        label = tk.Label(tab.scrollable_frame, image=img)
        label.image = img  # Keep a reference to prevent garbage collection
        label.pack()

def create_users_manual_window():
    global window
    window = Tk()
    window.geometry("680x835")
    window.title("Users Manual")
    window.configure(bg="#FFE1C6")

    center_window(window, 680, 835)

    # Create a custom style for the notebook tabs
    style = ttk.Style()
    style.configure('Custom.TNotebook.Tab', font=('Hanuman Regular', 12))

    notebook = ttk.Notebook(window, width=972, height=835, style='Custom.TNotebook')
    notebook.pack(padx=25, pady=25)

    # Create tabs with corresponding PDF files
    tabs = [
        ("Login", "assets\Manual\Login_Manual.pdf"),
        ("POS", "assets\Manual\POS_Manual _not finished_.pdf"),
        ("Account", "assets\Manual\BackupRestore.pdf"),
        ("Reports", "assets\Manual\Reports.pdf"),
        ("Barcodes", "assets\Manual\Barcode.pdf"),
        ("Inventory", "assets\Manual\Inventory.pdf"),
        ("Backup & Restore", "assets\Manual\BackupRestore.pdf"),
    ]

    for tab_name, pdf_path in tabs:
        tab = ScrollableFrame(notebook)
        notebook.add(tab, text=tab_name)
        show_pdf(tab, pdf_path)

    back_button = tk.Button(window, text="Back", command=go_to_window, font=("Hanuman Regular", 12))
    back_button.place(x=600, y=15)

    # Start the main loop
    window.mainloop()

# if __name__ == "__main__":
#     create_users_manual_window()
