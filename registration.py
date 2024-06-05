
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Program Files\Pos_System\assets\Registration")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("600x550")
window.configure(bg = "#FFE1C6")


canvas = Canvas(
    window,
    bg = "#FFE1C6",
    height = 550,
    width = 600,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    300.5,
    247.0,
    image=entry_image_1
)
entry_1 = Text(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=119.0,
    y=228.0,
    width=363.0,
    height=36.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    300.5,
    182.0,
    image=entry_image_2
)
entry_2 = Text(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=119.0,
    y=163.0,
    width=363.0,
    height=36.0
)

canvas.create_text(
    119.0,
    139.0,
    anchor="nw",
    text="User",
    fill="#000000",
    font=("Hanuman Regular", 16 * -1)
)

canvas.create_text(
    119.0,
    204.0,
    anchor="nw",
    text="Password",
    fill="#000000",
    font=("Hanuman Regular", 16 * -1)
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    300.5,
    312.0,
    image=entry_image_3
)
entry_3 = Text(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_3.place(
    x=119.0,
    y=293.0,
    width=363.0,
    height=36.0
)

canvas.create_text(
    119.0,
    269.0,
    anchor="nw",
    text="Confirm Password",
    fill="#000000",
    font=("Hanuman Regular", 16 * -1)
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
    x=349.0,
    y=466.0,
    width=133.0,
    height=37.0
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
    x=119.0,
    y=466.0,
    width=133.0,
    height=37.0
)

canvas.create_rectangle(
    161.0,
    44.0,
    439.0,
    108.0,
    fill="#FB7373",
    outline="")

canvas.create_text(
    207.0,
    52.0,
    anchor="nw",
    text="Registration",
    fill="#FFFFFF",
    font=("Hanuman Regular", 32 * -1)
)

canvas.create_text(
    119.0,
    339.0,
    anchor="nw",
    text="Level of Access",
    fill="#000000",
    font=("Hanuman Regular", 16 * -1)
)

canvas.create_text(
    145.0,
    366.0,
    anchor="nw",
    text="Admin",
    fill="#000000",
    font=("Hanuman Regular", 15 * -1)
)

canvas.create_text(
    145.0,
    397.0,
    anchor="nw",
    text="Employee/Staff",
    fill="#000000",
    font=("Hanuman Regular", 15 * -1)
)
window.resizable(False, False)
window.mainloop()
