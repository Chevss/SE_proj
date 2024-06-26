
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets/Manual")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


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
    320.0,
    40.0,
    652.0,
    139.0,
    fill="#5CB0FF",
    outline="")

canvas.create_text(
    362.0,
    60.0,
    anchor="nw",
    text="User Manual",
    fill="#000000",
    font=("Hanuman Regular", 40 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=385.0,
    y=734.0,
    width=201.0,
    height=83.0
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    486.0,
    436.5,
    image=entry_image_1
)
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
