from pathlib import Path
from tkinter import Tk, ttk, Canvas, Entry, messagebox, Button, PhotoImage, Label, Toplevel, Scrollbar, Frame, RIGHT, Y, W, CENTER, NO
from tkcalendar import DateEntry
import sqlite3

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\Inventory")

conn = sqlite3.connect('Trimark_construction_supply.db')
cursor = conn.cursor()

sort_order_quantity = "asc"  # Track sort order for quantity column
sort_order_price = "asc"  # Track sort order for price column

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def fetch_inventory_data():
    cursor.execute("SELECT * FROM inventory")
    return cursor.fetchall()


def search_inventory(keyword):
    query = """
    SELECT Barcode, Product_Name, Product_Quantity, Product_Price, Product_Description, Is_Void 
    FROM inventory 
    WHERE Barcode LIKE ? 
    OR Product_Name LIKE ? 
    OR Product_Description LIKE ?
    """
    cursor.execute(query, (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
    return cursor.fetchall()


def search_barcode(barcode):
    cursor.execute("SELECT Product_Name, Product_Quantity, Product_Price FROM inventory WHERE Barcode = ?", (barcode,))
    result = cursor.fetchone()
    return result


def go_to_window(windows):
    window.destroy()
    if windows == "back":
        import pos_admin
        pos_admin.create_pos_admin_window()


def add_product_window():
    add_window = Toplevel(window)
    add_window.title("Add Product")

    add_window.geometry("600x500")
    add_window.configure(bg="#FFE1C6")

    # Calculate the position for the window to be centered
    window_width, window_height = 600, 500
    screen_width = add_window.winfo_screenwidth()
    screen_height = add_window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Set the window geometry and position
    add_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    canvas = Canvas(
        add_window,
        bg="#FFE1C6",
        height=500,
        width=600,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    # Add Product label centered
    add_label = Label(
        add_window,
        text="Add Product",
        bg="#FFE1C6",  # Match canvas background
        fg="#000000",  # Black text color
        font=("Hanuman Regular", 24)  # Larger font size
    )
    add_label.place(relx=0.5, rely=0.05, anchor="n")

    # Labels without gray background
    barcode_label = Label(add_window, text="Barcode:", bg="#FFE1C6", font=("Hanuman Regular", 16))
    barcode_label.place(x=50, y=80)

    product_name_label = Label(add_window, text="Product Name:", bg="#FFE1C6", font=("Hanuman Regular", 16))
    product_name_label.place(x=50, y=130)

    product_price_label = Label(add_window, text="Product Price:", bg="#FFE1C6", font=("Hanuman Regular", 16))
    product_price_label.place(x=50, y=180)

    product_details_label = Label(add_window, text="Product Details:", bg="#FFE1C6", font=("Hanuman Regular", 16))
    product_details_label.place(x=50, y=230)

    product_quantity_label = Label(add_window, text="Product Quantity:", bg="#FFE1C6", font=("Hanuman Regular", 16))
    product_quantity_label.place(x=50, y=280)

    # Entry widgets
    barcode_entry = Entry(add_window, font=("Hanuman Regular", 16))
    barcode_entry.place(x=220, y=80, width=300)

    product_name_entry = Entry(add_window, font=("Hanuman Regular", 16))
    product_name_entry.place(x=220, y=130, width=300)

    product_price_entry = Entry(add_window, font=("Hanuman Regular", 16))
    product_price_entry.place(x=220, y=180, width=300)

    product_details_entry = Entry(add_window, font=("Hanuman Regular", 16))
    product_details_entry.place(x=220, y=230, width=300)

    product_quantity_entry = Entry(add_window, font=("Hanuman Regular", 16))
    product_quantity_entry.place(x=220, y=280, width=300)

    def save_and_close():
        # Call save_product function
        save_product(
            barcode_entry.get(),
            product_name_entry.get(),
            float(product_price_entry.get()),
            product_details_entry.get(),
            int(product_quantity_entry.get())
        )
        messagebox.showinfo("Product Saved", "The product has been saved successfully!")
        add_window.destroy()  # Close the add window

    save_button = Button(add_window, text="Save", command=save_and_close, font=("Hanuman Regular", 16))
    save_button.place(x=250, y=330)

    canvas.create_rectangle(
        50.0,
        50.0,
        550.0,
        430.0,
        fill="#FFE1C6",
        outline=""
    )

    add_window.mainloop()


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


def fetch_inventory_sorted_by_quantity(order="asc"):
    cursor.execute(f"SELECT * FROM inventory ORDER BY Product_Quantity {order.upper()}")
    return cursor.fetchall()


def fetch_inventory_sorted_by_price(order="asc"):
    cursor.execute(f"SELECT * FROM inventory ORDER BY Product_Price {order.upper()}")
    return cursor.fetchall()


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
    back_button = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: go_to_window("back"),
        relief="flat"
    )
    back_button.place(
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

    def update_table():
        # Clear the current table
        my_tree.delete(*my_tree.get_children())

        # Fetch the latest inventory data
        data = fetch_inventory_data()

        # Insert the fetched data into the treeview
        for record in data:
            modified_row = list(record)
            modified_row[-1] = "Yes" if record[-1] == 1 else "No"
            my_tree.insert("", "end", values=modified_row)

    # Modify button_3 to use the update_table function
    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=update_table,  # Link to update_table function
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

    search_entry = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        font=("Hanuman Regular", 24 * -1)
    )
    search_entry.place(x=41.0, y=92.0, width=300, height=47)

    def on_search():
        keyword = search_entry.get()
        rows = search_inventory(keyword)
        # Clear the treeview
        my_tree.delete(*my_tree.get_children())
        # Insert the filtered rows
        for row in rows:
            modified_row = list(row)
            modified_row[-1] = "Yes" if row[-1] == 1 else "No"
            my_tree.insert("", "end", values=modified_row)

    search_button = Button(
        window,
        text="Search",
        command=on_search,
        font=("Hanuman Regular", 16),
        bg="#FFE1C6"
    )
    search_button.place(x=350, y=92, width=100, height=47)

    canvas.create_text(
        41.0,
        50.0,
        anchor="nw",
        text="Search Product",
        fill="#000000",
        font=("Hanuman Regular", 28 * -1)
    )

    

    def toggle_sort(column):
        global sort_order_quantity, sort_order_price
        if column == "quantity":
            sort_order_quantity = "desc" if sort_order_quantity == "asc" else "asc"
            populate_treeview_quantity()
        elif column == "price":
            sort_order_price = "desc" if sort_order_price == "asc" else "asc"
            populate_treeview_price()

    def populate_treeview_quantity():
        current_items = fetch_inventory_sorted_by_quantity(sort_order_quantity)
        update_treeview(current_items)

    def populate_treeview_price():
        current_items = fetch_inventory_sorted_by_price(sort_order_price)
        update_treeview(current_items)

    def update_treeview(items):
        my_tree.delete(*my_tree.get_children())
        for item in items:
            modified_row = list(item)
            modified_row[-1] = "Yes" if item[-1] == 1 else "No"
            my_tree.insert("", "end", values=modified_row)

    # Create a frame for the treeview and scrollbar
    tree_frame = Frame(window)
    tree_frame.place(x=41, y=176, width=1199, height=482)

    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, height=20)

    tree_scroll.config(command=my_tree.yview)

    my_tree['columns'] = (
        "Barcode", "Product Name", "Product Quantity", "Product Price", "Product Description", "Is Void"
    )

    # Format columns
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("Barcode", anchor=W, width=100)
    my_tree.column("Product Name", anchor=W, width=150)
    my_tree.column("Product Quantity", anchor=CENTER, width=120)
    my_tree.column("Product Price", anchor=CENTER, width=100)
    my_tree.column("Product Description", anchor=W, width=250)
    my_tree.column("Is Void", anchor=CENTER, width=100)

    # Create Headings
    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("Barcode", text="Barcode", anchor=W)
    my_tree.heading("Product Name", text="Product Name", anchor=W)
    my_tree.heading("Product Quantity", text="Product Quantity", anchor=CENTER)
    my_tree.heading("Product Price", text="Product Price", anchor=CENTER)
    my_tree.heading("Product Description", text="Product Description", anchor=W)
    my_tree.heading("Is Void", text="Is Void", anchor=CENTER)

    # Increase font size
    style = ttk.Style()
    style.configure("Treeview", font=("Arial", 14))  # Adjust font family and size here

    my_tree.pack(fill="both", expand=True)

    # Global variables for sort order
    sort_order_quantity = "asc"
    sort_order_price = "asc"

    # Function to toggle sort order
    def toggle_sort(column):
        global sort_order_quantity, sort_order_price
        if column == "quantity":
            sort_order_quantity = "desc" if sort_order_quantity == "asc" else "asc"
            populate_treeview_quantity()
        elif column == "price":
            sort_order_price = "desc" if sort_order_price == "asc" else "asc"
            populate_treeview_price()

    # Function to populate treeview with sorted quantity
    def populate_treeview_quantity():
        current_items = get_current_items()
        current_items.sort(key=lambda x: x[2], reverse=(sort_order_quantity == "desc"))
        update_treeview(current_items, sort_order_quantity)

    # Function to populate treeview with sorted price
    def populate_treeview_price():
        current_items = get_current_items()
        current_items.sort(key=lambda x: x[3], reverse=(sort_order_price == "desc"))
        update_treeview(current_items, sort_order_price)

    # Function to get current items from treeview
    def get_current_items():
        items = []
        for item in my_tree.get_children():
            items.append(my_tree.item(item)["values"])
        return items

    # Function to update treeview with given items
    def update_treeview(items, sort_button=None):
        my_tree.delete(*my_tree.get_children())
        for item in items:
            modified_row = list(item)
            modified_row[-1] = "Yes" if item[-1] == 1 else "No"
            my_tree.insert("", "end", values=modified_row)

    def populate_treeview():
        populate_treeview_quantity()  # Initially populate with quantity sorted data

    # Example of binding headings
    my_tree.heading("Product Quantity", text="Product Quantity", anchor=CENTER, command=lambda: toggle_sort("quantity"))
    my_tree.heading("Product Price", text="Product Price", anchor=CENTER, command=lambda: toggle_sort("price"))
    my_tree.heading("Is Void", text="Is Void", anchor=CENTER)  # Placeholder, no sorting for boolean

    # Initial population of treeview
    populate_treeview()

    window.resizable(False, False)
    window.mainloop()


if __name__ == "__main__":
    create_inventory_window()
