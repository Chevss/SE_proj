

from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets/About")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def go_to_window(window):
    if window == "back":
        import maintenance
        maintenance.

def create_about_window():
    global window
    window = Tk()

    window.geometry("972x835")
    window.configure(bg = "#FFE1C6")


    canvas = Canvas(
        window,
        bg = "#FFE1C6",
        height = 835,
        width = 972,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
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

    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_1 clicked"),
        relief="flat"
    )
    button_1.place(
        x=386.0,
        y=734.0,
        width=201.0,
        height=83.0
    )

    back_button = Button(text="Back", font=("Hanuman Regular", 20), command=lambda: go_to_window("inventory"), bg="#81CDF8", relief="ridge")
    back_button.place(x=699.0, y=734.0,

    entry_1 = Text(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entry_1.place(
        x=102.0,
        y=180.0,
        width=768.0,
        height=511.0
    )
    window.resizable(False, False)
    window.mainloop()

if __name__ == "__main__":
    create_about_window()
