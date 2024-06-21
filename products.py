from pathlib import Path
from tkinter import Tk, ttk, Canvas, Entry, messagebox, Button, PhotoImage, Label, Toplevel, Scrollbar, Frame, RIGHT, Y, W, CENTER, NO, END
from tkcalendar import DateEntry
import sqlite3
from datetime import datetime
from user_logs import log_actions
from barcode import Code39
from barcode.writer import ImageWriter
from PIL import Image, ImageTk
import io
import random

OUTPUT_PATH = Path(__file__).parent
# ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\chevy_9ljzuod\Downloads\SE_proj-main (1)\SE_proj-main\assets\Inventory")
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\chevy_9ljzuod\Downloads\SE_proj-main\assets\Inventory")

conn = sqlite3.connect('Trimark_construction_supply.db')
cursor = conn.cursor()


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def fetch_inventory_data():
    cursor.execute("SELECT * FROM inventory")
    return cursor.fetchall()

def search_inventory(keyword):
    query = f"""
    SELECT Barcode, Product_Name, Product_Quantity, Product_Price, Product_Description, Date_Delivered, Is_Void 
    FROM inventory 
    WHERE Barcode LIKE ? 
    OR Product_Name LIKE ? 
    OR Product_Description LIKE ?
    """
    cursor.execute(query, (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
    return cursor.fetchall()

def search_barcode(barcode):
    cursor.execute("SELECT Product_Name, Product_Price, Product_Description, Product_Quantity FROM inventory WHERE Barcode = ?", (barcode,))
    result = cursor.fetchone()
    return result

def go_to_window(windows):
    window.destroy()
    if windows == "back":
        import inventory_admin
        inventory_admin.create_inventory_window()

def is_barcode_unique(barcode):
    # This is a placeholder function. Implement your own logic to check if barcode is unique.
    # For example, you might check against a database or a list of existing barcodes.
    return True

def register_product_window():
    register_product_window = Toplevel(window)
    register_product_window.title("Register Product")
    register_product_window.resizable(False, False)
    register_product_window.geometry("600x500")
    register_product_window.configure(bg="#FFE1C6")

    # Calculate the position for the window to be centered
    window_width, window_height = 600, 500
    screen_width = register_product_window.winfo_screenwidth()
    screen_height = register_product_window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Set the window geometry and position
    register_product_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    canvas = Canvas(
        register_product_window,
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
        register_product_window,
        text="Register Product",
        bg="#FFE1C6",  # Match canvas background
        fg="#000000",  # Black text color
        font=("Hanuman Regular", 24)  # Larger font size
    )
    add_label.place(relx=0.5, rely=0.05, anchor="n")

    # Labels without gray background
    barcode_label = Label(register_product_window, text="Barcode:", bg="#FFE1C6", font=("Hanuman Regular", 16))
    barcode_label.place(x=50, y=80)

    product_name_label = Label(register_product_window, text="Product Name:", bg="#FFE1C6", font=("Hanuman Regular", 16))
    product_name_label.place(x=50, y=170)

    product_price_label = Label(register_product_window, text="Product Price:", bg="#FFE1C6", font=("Hanuman Regular", 16))
    product_price_label.place(x=50, y=220)

    product_details_label = Label(register_product_window, text="Product Details:", bg="#FFE1C6", font=("Hanuman Regular", 16))
    product_details_label.place(x=50, y=270)

    # Entry widgets
    barcode_entry = Entry(register_product_window, font=("Hanuman Regular", 16))
    barcode_entry.place(x=220, y=80, width=300)

    product_name_entry = Entry(register_product_window, font=("Hanuman Regular", 16))
    product_name_entry.place(x=220, y=170, width=300)

    product_price_entry = Entry(register_product_window, font=("Hanuman Regular", 16))
    product_price_entry.place(x=220, y=220, width=300)

    product_details_entry = Entry(register_product_window, font=("Hanuman Regular", 16))
    product_details_entry.place(x=220, y=270, width=300)


    # Function to generate unique Code39 barcode
    def generate_unique_barcode():
        while True:
            barcode_value = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-. $/+%', k=10))
            if is_barcode_unique(barcode_value):
                barcode_entry.delete(0, END)
                barcode_entry.insert(0, barcode_value)
                
                # Generate barcode image
                barcode = Code39(barcode_value, writer=ImageWriter(), add_checksum=False)
                buffer = io.BytesIO()
                barcode.write(buffer)
                buffer.seek(0)
                
                break

    # Create Barcode button
    create_barcode_button = Button(register_product_window, text="Create Barcode", command=generate_unique_barcode, font=("Hanuman Regular", 12))
    create_barcode_button.place(x=315, y=118, width=120)

    def save_and_close():
        username = "temporary"
        action = "Added new product."

        current_date = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        # Call save_product function
        register_product(
            barcode_entry.get(),
            product_name_entry.get(),
            float(product_price_entry.get()),
            product_details_entry.get(),
            current_date
        )
        messagebox.showinfo("Product Saved", "The product has been saved successfully!")
        register_product_window.destroy()  # Close the add window

    save_button = Button(register_product_window, text="Save", command=save_and_close, font=("Hanuman Regular", 16))
    save_button.place(x=250, y=380)

    canvas.create_rectangle(
        50.0,
        50.0,
        550.0,
        430.0,
        fill="#FFE1C6",
        outline=""
    )

    register_product_window.mainloop()

def add_supply_window():
    add_supply_window = Toplevel(window)
    add_supply_window.resizable(False, False)
    add_supply_window.title("Add Supply")

    add_supply_window.geometry("600x450")
    add_supply_window.configure(bg="#FFE1C6")

    # Calculate the position for the window to be centered
    window_width, window_height = 600, 450
    screen_width = add_supply_window.winfo_screenwidth()
    screen_height = add_supply_window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Set the window geometry and position
    add_supply_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    canvas = Canvas(
        add_supply_window,
        bg="#FFE1C6",
        height=500,
        width=600,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    # Add Supply label centered
    add_label = Label(
        add_supply_window,
        text="Add Supply",
        bg="#FFE1C6",
        fg="#000000",
        font=("Hanuman Regular", 24)
    )
    add_label.place(relx=0.5, rely=0.05, anchor="n")

    barcode_label = Label(add_supply_window, text="Barcode:", bg="#FFE1C6", font=("Hanuman Regular", 16))
    barcode_label.place(x=50, y=80)

    barcode_entry = Entry(add_supply_window, font=("Hanuman Regular", 16))
    barcode_entry.place(x=220, y=80, width=240)

    def verify_barcode():
        barcode = barcode_entry.get().strip()
        result = search_barcode(barcode)

        if result:
            # Populate entry fields with existing product details
            product_name_entry.config(state='normal')
            product_name_entry.delete(0, 'end')
            product_name_entry.insert(0, result[0])
            product_name_entry.config(state='disabled')

            product_quantity_entry.config(state='normal')
            product_quantity_entry.delete(0, 'end')
            product_quantity_entry.insert(0, result[3])
            product_quantity_entry.config(state='normal')  # Make quantity editable

            date_entry.config(state='normal')
            date_entry.delete(0, 'end')
            date_entry.set_date(result[5])
        else:
            messagebox.showerror("Product Not Found", "No product found with the entered barcode.")

            # Reset the fields since barcode not found
            product_name_entry.delete(0, 'end')
            product_quantity_entry.delete(0, 'end')
            date_entry.set_date('')

        # Validate if barcode is unique for adding supply
        if not is_barcode_unique(barcode):
            messagebox.showerror("Duplicate Barcode", "Barcode already exists. Cannot add supply.")
            return

    verify_button = Button(add_supply_window, text="Verify", command=verify_barcode, font=("Hanuman Regular", 12))
    verify_button.place(x=465, y=78)

    product_name_label = Label(add_supply_window, text="Product Name:", bg="#FFE1C6", font=("Hanuman Regular", 16))
    product_name_label.place(x=50, y=130)

    product_name_entry = Entry(add_supply_window, font=("Hanuman Regular", 16))
    product_name_entry.place(x=220, y=130, width=300)
    product_name_entry.config(state='disabled')

    product_quantity_label = Label(add_supply_window, text="Add Quantity:", bg="#FFE1C6", font=("Hanuman Regular", 16))
    product_quantity_label.place(x=50, y=180)

    product_quantity_entry = Entry(add_supply_window, font=("Hanuman Regular", 16))
    product_quantity_entry.place(x=220, y=180, width=300)
    product_quantity_entry.config(state='disabled')

    date_label = Label(add_supply_window, text="Date Delivered:", bg="#FFE1C6", font=("Hanuman Regular", 16))
    date_label.place(x=50, y=230)

    date_entry = DateEntry(add_supply_window, date_pattern="mm-dd-yyyy", width=12, background='darkblue',
                           foreground='white', borderwidth=2, font=("Hanuman Regular", 16))
    date_entry.place(x=220, y=230)

    def save_supply():
        barcode = barcode_entry.get().strip()
        product_name = product_name_entry.get().strip()
        product_quantity_str = product_quantity_entry.get().strip()
        date_delivered = date_entry.get_date()

        
        # Validate and convert product quantity
        try:
            product_quantity = int(product_quantity_str)
        except ValueError:
            messagebox.showerror("Invalid Quantity", "Please enter a valid numeric value for product quantity.")
            return

        # Ensure barcode is not empty
        if not barcode:
            messagebox.showerror("Missing Barcode", "Please enter a barcode.")
            return

        # Ensure product name is not empty
        if not product_name:
            messagebox.showerror("Missing Product Name", "Please enter a product name.")
            return

        try:
            cursor.execute('''
                INSERT INTO inventory (Barcode, Product_Name, Product_Quantity, Date_Delivered)
                VALUES (?, ?, ?, ?)
            ''', (barcode, product_name, product_quantity, date_delivered))
            conn.commit()
            messagebox.showinfo("Supply Added", "Supply added successfully!")
            add_supply_window.destroy()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error adding supply: {e}")

    save_button = Button(add_supply_window, text="Save", command=save_supply, font=("Hanuman Regular", 16))
    save_button.place(x=250, y=330)

    canvas.create_rectangle(
        50.0,
        50.0,
        550.0,
        430.0,
        fill="#FFE1C6",
        outline=""
    )

    add_supply_window.mainloop()

def update_products_window():
    update_supply_window = Toplevel(window)
    update_supply_window.resizable(False, False)
    update_supply_window.title("Update Supply")

    update_supply_window.geometry("600x500")
    update_supply_window.configure(bg="#FFE1C6")

    # Calculate the position for the window to be centered
    window_width, window_height = 600, 500
    screen_width = update_supply_window.winfo_screenwidth()
    screen_height = update_supply_window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Set the window geometry and position
    update_supply_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    canvas = Canvas(
        update_supply_window,
        bg="#FFE1C6",
        height=500,
        width=600,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    # Add Supply label centered
    add_label = Label(
        update_supply_window,
        text="Update Supply",
        bg="#FFE1C6",
        fg="#000000",
        font=("Hanuman Regular", 24)
    )
    add_label.place(relx=0.5, rely=0.05, anchor="n")

    barcode_label = Label(update_supply_window, text="Barcode:", bg="#FFE1C6", font=("Hanuman Regular", 16))
    barcode_label.place(x=50, y=80)

    barcode_entry = Entry(update_supply_window, font=("Hanuman Regular", 16))
    barcode_entry.place(x=220, y=80, width=240)

    def verify_barcode():
        barcode = barcode_entry.get().strip()
        result = search_barcode(barcode)
        if result:
            # Populate entry fields with existing product details
            product_name_entry.delete(0, 'end')
            product_name_entry.insert(0, result[0])
            product_quantity_entry.delete(0, 'end')
            product_quantity_entry.insert(0, result[1])
            product_price_entry.delete(0, 'end')
            product_price_entry.insert(0, result[2])
            product_details_entry.delete(0, 'end')
            product_details_entry.insert(0, result[3])
            void_option.set(result[4])
            date_entry.set_date(result[5])
        else:
            messagebox.showerror("Product Not Found", "No product found with the entered barcode.")

    verify_button = Button(update_supply_window, text="Verify", command=verify_barcode, font=("Hanuman Regular", 12))
    verify_button.place(x=465, y=78)

    product_name_label = Label(update_supply_window, text="Product Name:", bg="#FFE1C6", font=("Hanuman Regular", 16))
    product_name_label.place(x=50, y=130)

    product_name_entry = Entry(update_supply_window, font=("Hanuman Regular", 16))
    product_name_entry.place(x=220, y=130, width=300)

    product_price_label = Label(update_supply_window, text="Product Price:", bg="#FFE1C6", font=("Hanuman Regular", 16))
    product_price_label.place(x=50, y=180)

    product_price_entry = Entry(update_supply_window, font=("Hanuman Regular", 16))
    product_price_entry.place(x=220, y=180, width=300)

    product_details_label = Label(update_supply_window, text="Product Details:", bg="#FFE1C6", font=("Hanuman Regular", 16))
    product_details_label.place(x=50, y=230)

    product_details_entry = Entry(update_supply_window, font=("Hanuman Regular", 16))
    product_details_entry.place(x=220, y=230, width=300)

    product_quantity_label = Label(update_supply_window, text="Product Quantity:", bg="#FFE1C6", font=("Hanuman Regular", 16))
    product_quantity_label.place(x=50, y=280)

    product_quantity_entry = Entry(update_supply_window, font=("Hanuman Regular", 16))
    product_quantity_entry.place(x=220, y=280, width=300)

    void_label = Label(update_supply_window, text="Is Void:", bg="#FFE1C6", font=("Hanuman Regular", 16))
    void_label.place(x=50, y=330)

    void_option = ttk.Combobox(update_supply_window, values=["No", "Yes"], font=("Hanuman Regular", 16), state="readonly")
    void_option.place(x=220, y=330, width=100)
    void_option.current(0)  # Default to "No"

    date_label = Label(update_supply_window, text="Date Delivered:", bg="#FFE1C6", font=("Hanuman Regular", 16))
    date_label.place(x=50, y=380)

    date_entry = DateEntry(update_supply_window, date_pattern="mm-dd-yyyy", width=12, background='darkblue',
                           foreground='white', borderwidth=2, font=("Hanuman Regular", 16))
    date_entry.place(x=220, y=380)

    def save_supply():
        barcode = barcode_entry.get().strip()
        product_name = product_name_entry.get().strip()
        product_price = float(product_price_entry.get())
        product_details = product_details_entry.get().strip()
        product_quantity = int(product_quantity_entry.get())
        is_void = 1 if void_option.get() == "Yes" else 0
        date_delivered = date_entry.get_date()

        try:
            cursor.execute('''
                INSERT INTO inventory (Barcode, Product_Name, Product_Quantity, Product_Price, Product_Description, Is_Void, Date_Delivered)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (barcode, product_name, product_quantity, product_price, product_details, is_void, date_delivered))
            conn.commit()
            messagebox.showinfo("Supply Added", "Supply added successfully!")
            update_supply_window.destroy()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error adding supply: {e}")

    save_button = Button(update_supply_window, text="Save", command=save_supply, font=("Hanuman Regular", 16))
    save_button.place(x=250, y=430)

    canvas.create_rectangle(
        50.0,
        50.0,
        550.0,
        430.0,
        fill="#FFE1C6",
        outline=""
    )

    update_supply_window.mainloop()

def register_product(barcode, product_name, product_price, product_details, date_registered):
    try:
        cursor.execute('''
            INSERT INTO inventory (Barcode, Product_Name, Product_Price, Product_Description, Date_Registered)
            VALUES (?, ?, ?, ?, ?)
        ''', (barcode, product_name, product_price, product_details, date_registered))
        conn.commit()
        print("Product added successfully!")
    except sqlite3.Error as e:
        print(f"Error inserting data into inventory table: {e}")

def get_LOA(username):
    # hashed_username = hash_username(username)

    cursor.execute("SELECT Loa FROM accounts WHERE username =?", (username,))
    row = cursor.fetchone()
    if row:
        return row[0]
    else:
        return None

def fetch_inventory_sorted_by_quantity(order="asc"):
    cursor.execute(f"SELECT * FROM inventory ORDER BY Product_Quantity {order.upper()}")
    return cursor.fetchall()

def fetch_inventory_sorted_by_price(order="asc"):
    cursor.execute(f"SELECT * FROM inventory ORDER BY Product_Price {order.upper()}")
    return cursor.fetchall()

def create_products_window():
    global window
    window = Tk()

    window.geometry("1280x800")
    window.configure(bg="#FFE1C6")

    window.title("Products")
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
    back_button = Button(
        window,
        text="Back",
        command=lambda: go_to_window("back"),
        font=("Hanuman Regular", 16),
        bg="#FFFFFF",
        relief="raised"
    )
    back_button.place(
        x=1071.0,
        y=696.0,
        width=169.0,
        height=64.0
    )


    register_product_button = Button(
        window,
        text="Register Product",
        command=lambda: register_product_window(),
        font=("Hanuman Regular", 16),
        bg="#83F881",
        relief="raised"
    )
    register_product_button.place(
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
            modified_row[-1] = "No" if record[-1] == 1 else "Yes"
            my_tree.insert("", "end", values=modified_row)

    update_product_button = Button(
        window,
        text="Update Products",
        command=lambda: update_products_window(),
        font=("Hanuman Regular", 16),
        bg="#81CDF8",
        relief="raised"
    )
    update_product_button.place(
        x=617.0,
        y=691.0,
        width=237.84408569335938,
        height=73.0
    )

    add_supply_button = Button(
        window,
        text="Add Supply",
        command=lambda: add_supply_window(),
        font=("Hanuman Regular", 16),
        bg="#81CDF8",
        relief="raised"
    )
    add_supply_button.place(
        x=329.0,
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

    # Create a frame for the treeview and scrollbar
    tree_frame = Frame(window)
    tree_frame.place(x=41, y=176, width=1199, height=482)

    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, height=20)

    tree_scroll.config(command=my_tree.yview)

    my_tree['columns'] = (
        "Barcode", "Product Name", "Product Quantity", "Product Price", "Product Description", "Date Registered",
        "Date Delivered", "Is Void"
    )

    # Format columns
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("Barcode", anchor=W, width=100)
    my_tree.column("Product Name", anchor=W, width=130)
    my_tree.column("Product Quantity", anchor=CENTER, width=120)
    my_tree.column("Product Price", anchor=CENTER, width=100)
    my_tree.column("Product Description", anchor=W, width=250)
    my_tree.column("Date Registered", anchor=CENTER, width=150)
    my_tree.column("Date Delivered", anchor=CENTER, width=150)
    my_tree.column("Is Void", anchor=CENTER, width=100)

    # Create Headings
    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("Barcode", text="Barcode", anchor=W)
    my_tree.heading("Product Name", text="Product Name", anchor=W)
    my_tree.heading("Product Quantity", text="Product Quantity", anchor=CENTER)
    my_tree.heading("Product Price", text="Product Price", anchor=CENTER)
    my_tree.heading("Product Description", text="Product Description", anchor=W)
    my_tree.heading("Date Registered", text="Date Registered", anchor=CENTER)
    my_tree.heading("Date Delivered", text="Date Delivered", anchor=CENTER)
    my_tree.heading("Is Void", text="Available", anchor=CENTER)

    # Increase font size
    style = ttk.Style()
    style.configure("Treeview", font=("Hanuman Regular", 11))  # Adjust font family and size here

    # Pack the treeview into the frame
    my_tree.pack(fill="both", expand=True)

    # Initially populate the treeview with data
    update_table()

    def fetch_inventory_sorted_by_quantity(order="asc"):
        cursor.execute(f"SELECT * FROM inventory ORDER BY Product_Quantity {order.upper()}")
        return cursor.fetchall()

    def fetch_inventory_sorted_by_price(order="asc"):
        cursor.execute(f"SELECT * FROM inventory ORDER BY Product_Price {order.upper()}")
        return cursor.fetchall()

    window.resizable(False, False)
    window.mainloop()


if __name__ == "__main__":
    create_products_window()
