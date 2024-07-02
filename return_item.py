import sqlite3
from pathlib import Path
from tkinter import BooleanVar, Button, Canvas, Checkbutton, Entry, filedialog, messagebox, Tk
from tkinter import ttk

def go_to_window(windows):
    window.destroy()
    if windows == "Back":
        import pos_admin
        pos_admin.create_pos_admin_window()

def create_return_item_window():
    global window, new_phone_entry
    window = Tk()
    window.title("Return Item")
    window.geometry("500x230")
    window.configure(bg="#FFE1C6")

    window_width, window_height = 500, 230
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    canvas = Canvas(window, bg="#DDD", height=400, width=600, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    canvas.create_rectangle(window_width, 0, 0, 55, fill="#000", outline="")
    canvas.create_text(180, 15, anchor="nw", text="Return Item", fill="#FFFFFF", font=("Hanuman Regular", 24 * -1))

    canvas.create_text(50, 70, anchor="nw", text="Purchase ID", fill="#000000", font=("Hanuman Regular", 16 * -1))
    # purchase_id_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=1, font=("Hanuman Regular", 24 * -1))
    # purchase_id_entry.place(x=50, y=95, width=200, height=32)

    
    purchase_id = get_purchase_id()
    combobox = ttk.Combobox(window, values=purchase_id)
    combobox.place(x=50, y=95, width=200, height=32)




    return_item_button = Button(window, text="Normal Item", font=("Hanuman Regular", 16), bg="green", fg='#FFF', command=None)
    return_item_button.place(x=300, y=95, width=150.0, height=32)

    broken_item_button = Button(window, text="Broken Item", font=("Hanuman Regular", 16), bg="green", fg='#FFF', command=None)
    broken_item_button.place(x=300, y=150, width=150.0, height=32)

    back_button = Button(window, text="Back", font=("Hanuman Regular", 16), bg="red", fg="#FFF", command=lambda:go_to_window("Back"))
    back_button.place(x=50, y=150, width=100.0, height=32)

    window.resizable(False, False)
    window.mainloop()

def get_purchase_id():
    conn = sqlite3.connect('Trimark_construction_supply.db')
    cursor = conn.cursor()

    cursor.execute("SELECT Purchase_ID FROM purchase_history")
    data = cursor.fetchall()

    conn.close()

    purchase_ids = [item[0] for item in data]
    return purchase_ids