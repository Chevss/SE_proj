from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\chevy_9ljzuod\Downloads\SE_proj-main\SE_proj-main\assets\New_pass")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
window = Tk()
def create_new_pass_window():
    window.title("New Password")
    window.geometry("600x400")
    window.configure(bg="#FFE1C6")

    window_width, window_height = 600, 400
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Set the window geometry and position
    window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    canvas = Canvas(
        window,
        bg="#FFE1C6",
        height=400,
        width=600,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        300.5,
        205.0,
        image=entry_image_1
    )
    confirm_pass_entry = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        font=("Hanuman Regular", 24 * -1),
        show="•"
    )
    confirm_pass_entry.place(
        x=119.0,
        y=186.0,
        width=363.0,
        height=36.0
    )

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        300.5,
        132.0,
        image=entry_image_2
    )
    new_pass_entry = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        font=("Hanuman Regular", 24 * -1),
        show="•"
    )
    new_pass_entry.place(
        x=119.0,
        y=113.0,
        width=363.0,
        height=36.0
    )

    canvas.create_text(
        119.0,
        89.0,
        anchor="nw",
        text="New Password",
        fill="#000000",
        font=("Hanuman Regular", 16 * -1)
    )

    canvas.create_text(
        119.0,
        162.0,
        anchor="nw",
        text="Confirm New Password",
        fill="#000000",
        font=("Hanuman Regular", 16 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    back_button = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("back_button clicked"),
        relief="flat"
    )
    back_button.place(
        x=415.0,
        y=336.0,
        width=133.0,
        height=37.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    confirm_button = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("confirm_button clicked"),
        relief="flat"
    )
    confirm_button.place(
        x=250.0,
        y=236.0,
        width=100.0,
        height=37.0
    )

    canvas.create_rectangle(
        179.0,
        20.0,
        420.0,
        76.0,
        fill="#FB7373",
        outline="")

    canvas.create_text(
        220.0,
        35.0,
        anchor="nw",
        text="New Password",
        fill="#FFFFFF",
        font=("Hanuman Regular", 24 * -1)
    )
    window.resizable(False, False)
    window.mainloop()

if __name__ == "__main__":
    create_new_pass_window()

