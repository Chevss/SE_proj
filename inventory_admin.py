from pathlib import Path
from tkinter import Tk, ttk, Canvas, Entry, Text, Button, PhotoImage, Label, Toplevel, Scrollbar, Frame
import sqlite3

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Lorenzo Trinidad\Downloads\SE_proj-main\assets\Inventory")

conn = sqlite3.connect('Trimark_construction_supply.db')
cursor = conn.cursor()


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def fetch_inventory_data():
    cursor.execute("SELECT * FROM inventory")
    return cursor.fetchall()

def search_barcode(barcode):
    cursor.execute("SELECT Product_Name, Product_Quantity, Product_Price FROM inventory WHERE Barcode = ?", (barcode,))
    result = cursor.fetchone()

    conn.close()
    return result

def add_product_window():
    add_window = Toplevel(window)
    add_window.title("Add Product")

    add_window.geometry("600x400")
    add_window.configure(bg="#FFE1C6")

    # Calculate the position for the window to be centered
    window_width, window_height = 600, 400
    screen_width = add_window.winfo_screenwidth()
    screen_height = add_window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Set the window geometry and position
    add_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    canvas = Canvas(
        add_window,
        bg="#FFE1C6",
        height=400,
        width=600,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    barcode_label = Label(add_window, text="Barcode:")
    barcode_label.place(x=50, y=50)
    barcode_entry = Entry(add_window)
    barcode_entry.place(x=150, y=50)

    product_name_label = Label(add_window, text="Product Name:")
    product_name_label.place(x=50, y=100)
    product_name_entry = Entry(add_window)
    product_name_entry.place(x=150, y=100)

    product_price_label = Label(add_window, text="Product Price:")
    product_price_label.place(x=50, y=150)
    product_price_entry = Entry(add_window)
    product_price_entry.place(x=150, y=150)

    product_details_label = Label(add_window, text="Product Details:")
    product_details_label.place(x=50, y=200)
    product_details_entry = Entry(add_window)
    product_details_entry.place(x=150, y=200)

    product_quantity_label = Label(add_window, text="Product Quantity:")
    product_quantity_label.place(x=50, y=250)
    product_quantity_entry = Entry(add_window)
    product_quantity_entry.place(x=150, y=250)

    save_button = Button(add_window, text="Save", command=lambda: save_product(
        barcode_entry.get(),
        product_name_entry.get(),
        float(product_price_entry.get()),
        product_details_entry.get(),
        int(product_quantity_entry.get())
    ))
    save_button.place(x=250, y=300)

    canvas.create_rectangle(
        50.0,
        20.0,
        550.0,
        350.0,
        fill="#FFFFFF",
        outline=""
    )

    canvas.create_text(
        50.0,
        20.0,
        anchor="nw",
        text="Add Product",
        fill="#000000",
        font=("Hanuman Regular", 24 * -1)
    )

    add_window.mainloop()

def get_LOA(username):
    # hashed_username = hash_username(username)

    cursor.execute("SELECT Loa FROM accounts WHERE username =?", (username,))
    row = cursor.fetchone()
    if row:
        return row[0]
    else:
        return None

def save_product(barcode, product_name, product_price, product_details, product_quantity):
    try:
        cursor.execute('''
            INSERT INTO inventory (Barcode, Product_Name, Product_Quantity, Product_Price, Product_Description, Is_Void)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (barcode, product_name, product_quantity, product_price, product_details, 0))
        conn.commit()
        print("Product added successfully!")
    except sqlite3.Error as e:
        print(f"Error inserting data into inventory table: {e}")

def go_to_window(windows):
    window.destroy()
    if windows == "back":
        import pos_admin
        pos_admin.create_pos_admin_window()

def create_inventory_window():
    global window
    window = Tk()

    window.geometry("1280x800")
    window.configure(bg="#FFE1C6")
    
    window.title("Inventory")
    window.configure(bg="#FFE1C6")

    # Calculate the position for the window to be centered
    window_width, window_height = 1280, 800
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Set the window geometry and position
    window.geometry(f'{window_width}x{window_height}+{x}+{y}')

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
        command=lambda:go_to_window("back"),
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
    add_product_button = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: add_product_window(),
        relief="flat"
    )
    add_product_button.place(
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
    search_entry = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        font=("Hanuman Regular", 24 * -1)
    )
    search_entry.place(
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
    
    # Create a frame for the treeview and scrollbar
    frame = Frame(window)
    frame.place(x=41, y=176, width=1199, height=482)
    
    # Adjust the treeview style
    style = ttk.Style()
    style.configure("Treeview", font=("Hanuman Regular", 16), rowheight=30)
    style.configure("Treeview.Heading", font=("Hanuman Regular", 18, "bold"))

    # Create the treeview
    tree = ttk.Treeview(frame, columns=("Barcode", "Product_Name", "Product_Quantity", "Product_Price", "Product_Description", "Is_Void"), show="headings")
    tree.heading("Barcode", text="Barcode")
    tree.heading("Product_Name", text="Product Name")
    tree.heading("Product_Quantity", text="Quantity")
    tree.heading("Product_Price", text="Price")
    tree.heading("Product_Description", text="Description")
    tree.heading("Is_Void", text="Is Void")

    # Set column alignment
    tree.column("Barcode", anchor="center")
    tree.column("Product_Name", anchor="center")
    tree.column("Product_Quantity", anchor="center")
    tree.column("Product_Price", anchor="center")
    tree.column("Product_Description", anchor="center")
    tree.column("Is_Void", anchor="center")

    # Create a scrollbar
    scrollbar = Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    tree.pack(side="left", fill="both", expand=True)

    # Fetch data and insert into treeview
    cursor.execute("SELECT Barcode, Product_Name, Product_Quantity, Product_Price, Product_Description, Is_Void FROM inventory")
    rows = cursor.fetchall()
    for row in rows:
        # Replace Is_Void values
        modified_row = list(row)
        modified_row[-1] = "Yes" if row[-1] == 1 else "No"
        tree.insert("", "end", values=modified_row)
        
    window.resizable(False, False)
    window.mainloop()

if __name__ == "__main__":
    create_inventory_window()
