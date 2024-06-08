from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage

OUTPUT_PATH = Path(__file__).parent
# ASSETS_PATH = OUTPUT_PATH / Path(r"C:/Users/TIPQC/Downloads/SE_proj-main/assets/Menu_admin")
ASSETS_PATH = OUTPUT_PATH / Path(r"C:/Users/katsu/Documents/GitHub/SE_proj/assets/Menu_admin")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def create_menu_ad_window():
    window = Tk()
    window.geometry("859x673")
    window.configure(bg = "#FFE1C6")
    window.title("Admin Menu")

    window_width, window_height = 859, 673
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Set the window geometry and position
    window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    canvas = Canvas(
        window,
        bg = "#FFE1C6",
        height = 673,
        width = 859,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: logout(window),
        relief="flat"
    )
    button_1.place(
        x=331.0,
        y=597.0,
        width=206.0,
        height=50.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_2 clicked"),
        relief="flat"
    )
    button_2.place(
        x=579.0,
        y=411.0,
        width=224.0,
        height=134.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_3 clicked"),
        relief="flat"
    )
    button_3.place(
        x=322.0,
        y=411.0,
        width=224.0,
        height=134.0
    )

    button_image_4 = PhotoImage(
        file=relative_to_assets("button_4.png"))
    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_4 clicked"),
        relief="flat"
    )
    button_4.place(
        x=65.0,
        y=411.0,
        width=224.0,
        height=134.0
    )

    button_image_5 = PhotoImage(
        file=relative_to_assets("button_5.png"))
    button_5 = Button(
        image=button_image_5,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_5 clicked"),
        relief="flat"
    )
    button_5.place(
        x=579.0,
        y=233.0,
        width=224.0,
        height=134.0
    )

    button_image_6 = PhotoImage(
        file=relative_to_assets("button_6.png"))
    button_6 = Button(
        image=button_image_6,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_6 clicked"),
        relief="flat"
    )
    button_6.place(
        x=322.0,
        y=233.0,
        width=224.0,
        height=134.0
    )

    button_image_7 = PhotoImage(
        file=relative_to_assets("button_7.png"))
    button_7 = Button(
        image=button_image_7,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: registration(window),
        relief="flat"
    )
    button_7.place(
        x=65.0,
        y=233.0,
        width=224.0,
        height=134.0
    )

    button_image_8 = PhotoImage(
        file=relative_to_assets("button_8.png"))
    button_8 = Button(
        image=button_image_8,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_8 clicked"),
        relief="flat"
    )
    button_8.place(
        x=579.0,
        y=55.0,
        width=224.0,
        height=134.0
    )

    button_image_9 = PhotoImage(
        file=relative_to_assets("button_9.png"))
    button_9 = Button(
        image=button_image_9,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_9 clicked"),
        relief="flat"
    )
    button_9.place(
        x=322.0,
        y=55.0,
        width=224.0,
        height=134.0
    )

    button_image_10 = PhotoImage(
        file=relative_to_assets("button_10.png"))
    button_10 = Button(
        image=button_image_10,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_10 clicked"),
        relief="flat"
    )
    button_10.place(
        x=65.0,
        y=55.0,
        width=224.0,
        height=134.0
    )

    window.resizable(False, False)
    window.mainloop()

def registration(window):
    window.destroy()
    from registration import create_registration_window
    create_registration_window()

def logout(window):
    window.destroy()
    from login import create_login_window
    create_login_window()

if __name__ == "__main__":
    create_menu_ad_window()
