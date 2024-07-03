import tkinter as tk
from pathlib import Path
from tkinter import Button, Canvas, PhotoImage

# From user made modules
from maintenance import backup_database, restore_database

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets/Maintenance")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def go_to_window(window_type):
    window.destroy()
    if window_type == "pos_admin":
        import pos_admin
        pos_admin.create_pos_admin_window()

def create_backup_restore_window():
    global window
    window = tk.Tk()
    window.geometry("640x400")
    window.configure(bg="#FFE1C6")
    window.title("Backup/Restore")

    window_width, window_height = 640, 160
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    # Create a canvas to place widgets on
    global canvas
    canvas = Canvas(window, bg="#FFE1C6", height=800, width=1280, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    # Backup
    backup_img = PhotoImage(file=relative_to_assets("backup.png"))
    backup_btn = Button(image=backup_img, borderwidth=2, highlightthickness=0,  command=lambda: backup_database(), relief="flat")
    backup_btn.place(x=30.0, y=20.0)

    # Restore
    restore_img = PhotoImage(file=relative_to_assets("restore.png"))
    restore_btn = Button(image=restore_img, borderwidth=2, highlightthickness=0, command=lambda: restore_database(), relief="flat")
    restore_btn.place(x=230.0, y=20.0)

    # Back
    back_img = PhotoImage(file=relative_to_assets("back.png"))
    back_btn = Button(image=back_img, borderwidth=2, highlightthickness=0, command=lambda: go_to_window("pos_admin"), relief="flat")
    back_btn.place(x=430.0, y=20.0)

    window.resizable(False, False)
    window.mainloop()

# if __name__ == "__main__":
#     create_backup_restore_window()