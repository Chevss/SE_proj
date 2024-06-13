from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Program Files\Pos_System\build\assets\Inventory")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def create_inventory_window():
    window = Tk()

    window.geometry("1280x800")
    window.configure(bg="#FFE1C6")

    canvas = Canvas(
        window,
        bg="#FFE1C6",
        height=800,
        width=1280,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
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
        x=1071.0,
        y=696.0,
        width=169.0,
        height=64.0
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
        x=41.0,
        y=691.0,
        width=237.84408569335938,
        height=73.0
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
        x=329.0,
        y=691.0,
        width=237.84408569335938,
        height=73.0
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
        x=617.0,
        y=691.0,
        width=237.84408569335938,
        height=73.0
    )

    canvas.create_rectangle(
        41.0,
        176.0,
        1240.0,
        658.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_text(
        41.0,
        20.0,
        anchor="nw",
        text="Admin",
        fill="#000000",
        font=("Hanuman Regular", 20 * -1)
    )

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        317.0,
        122.0,
        image=entry_image_1
    )
    entry_1 = Text(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entry_1.place(
        x=41.0,
        y=92.0,
        width=552.0,
        height=58.0
    )

    canvas.create_text(
        41.0,
        50.0,
        anchor="nw",
        text="Search Product",
        fill="#000000",
        font=("Hanuman Regular", 28 * -1)
    )
    window.resizable(False, False)
    window.mainloop()

if __name__ == "__main__":
    create_inventory_window()
