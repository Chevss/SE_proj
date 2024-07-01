import tkinter as tk
from tkinter import ttk, messagebox, Tk, Canvas

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

    # Create tabs (dummy content for demonstration)
    tabs = [
        ("Login", "Login Content"),
        ("POS", "POS Content"),
        ("Account", "Account Content"),
        ("Reports", "Reports Content"),
        ("Barcodes", "Barcodes Content"),
        ("Inventory", "Inventory Content"),
        ("Backup", "Backup Content"),
        ("Restore", "Restore Content")
    ]

    for tab_name, tab_content in tabs:
        tab = ttk.Frame(notebook)
        notebook.add(tab, text=tab_name)
        tk.Label(tab, text=tab_content, font=("Hanuman Regular", 12)).pack()

    back_button = tk.Button(window, text="Back", command=go_to_window, font=("Hanuman Regular", 12))
    back_button.place(x=900, y=15)

    # Start the main loop
    window.mainloop()

if __name__ == "__main__":
    create_users_manual_window()
