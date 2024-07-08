from barcode import Code39
from barcode.writer import ImageWriter
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import  ttk, Canvas, Entry, messagebox, Button, Label, Toplevel, Scrollbar, IntVar,  END, BooleanVar, Radiobutton, Checkbutton
from tkcalendar import DateEntry
import io
import random
import sqlite3

# From user made modules
import shared_state
from user_logs import log_actions

show_individual = False

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\Inventory")

username = shared_state.current_user

try:
    conn = sqlite3.connect('Trimark_construction_supply.db')
    cursor = conn.cursor()
except sqlite3.Error as e:
    messagebox.showerror("Database Connection Error", f"Error connecting to database: {e}")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Global variable to keep track of sorting order
SORT_ORDER = {}

def fetch_inventory_data(show_individual=False):
    try:
        if show_individual:
            cursor.execute("""
            SELECT i.Barcode, p.Name, p.Price, i.Quantity, p.Details, p.Status, i.DateDelivered, i.Supplier 
            FROM inventory i
            JOIN product p ON i.Barcode = p.Barcode
            """)
        else:
            cursor.execute("""
            SELECT p.Barcode, p.Name, p.Price, SUM(i.Quantity) AS TotalQuantity, p.Details, p.Status, MIN(i.DateDelivered) AS OldestDateDelivered, i.Supplier 
            FROM inventory i
            JOIN product p ON i.Barcode = p.Barcode
            GROUP BY p.Barcode
            """)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error fetching data: {e}")
        return []

def get_inventory_data():
    try:
        cursor.execute("""
        SELECT i.Barcode, p.Name, p.Price, i.Quantity, p.Details, p.Status, i.DateDelivered, i.Supplier 
        FROM inventory i
        JOIN product p ON i.Barcode = p.Barcode
        """)
        rows = cursor.fetchall()
        print(f"Fetched {len(rows)} rows from inventory data.")  # Debug statement
        return rows
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error fetching inventory data: {e}")
        return []

def search_inventory_linear(keyword, individual=False):
    inventory_data = get_inventory_data()
    print (inventory_data)
    if not inventory_data:
        return []

    keyword = keyword.lower()  # Convert keyword to lowercase for case-insensitive search

    results = []
    for item in inventory_data:
        if (keyword in str(item[0]).lower() or  # Check Barcode
            keyword in item[1].lower()):        # Check Name
            
            results.append(item)

    if individual:
        return results[0] if results else None  # Return the first item or None if no results
    else:
        return results

def go_to_window(windows):
    window.destroy()
    if windows == "back":
        import pos_admin
        pos_admin.create_pos_admin_window()

def is_barcode_unique(barcode):
    try:
        cursor.execute("SELECT Barcode FROM product WHERE Barcode = ?", (barcode,))
        return cursor.fetchone() is None
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error checking barcode uniqueness: {e}")
        return False

def register_product(barcode, product_name, product_price, product_details, critical_lvl):
    try:
        # cursor.execute('''
        #     ALTER TABLE product ADD Critical_lvl INTEGER
        # ''')

        cursor.execute('''
            INSERT INTO product (Barcode, Name, Price, Details, Critical_lvl)
            VALUES (?, ?, ?, ?, ?)
        ''', (barcode, product_name, product_price, product_details, critical_lvl))
        conn.commit()
        
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error inserting data into product table: {e}")

def register_product_window():
    register_product_window = Toplevel(window)
    register_product_window.title("Register Product")
    register_product_window.resizable(False, False)
    register_product_window.geometry("600x500")
    register_product_window.configure(bg="#FFE1C6")

    window_width, window_height = 600, 500
    screen_width = register_product_window.winfo_screenwidth()
    screen_height = register_product_window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    register_product_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    canvas = Canvas(register_product_window, bg="#FFE1C6", height=500, width=600, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    add_label = Label(register_product_window, text="Register Product", bg="#FFE1C6", fg="#000000", font=("Hanuman Regular", 24))
    add_label.place(relx=0.5, rely=0.05, anchor="n")

    barcode_label = Label(register_product_window, text="Barcode:", bg="#FFE1C6", font=("Hanuman Regular", 16))
    barcode_label.place(x=50, y=80)

    product_name_label = Label(register_product_window, text="Product Name:", bg="#FFE1C6", font=("Hanuman Regular", 16))
    product_name_label.place(x=50, y=170)

    product_price_label = Label(register_product_window, text="Product Price:", bg="#FFE1C6", font=("Hanuman Regular", 16))
    product_price_label.place(x=50, y=220)

    product_details_label = Label(register_product_window, text="Product Details:", bg="#FFE1C6", font=("Hanuman Regular", 16))
    product_details_label.place(x=50, y=270)
    
    critical_lvl_label = Label(register_product_window, text="Critical Level:", bg="#FFE1C6", font=("Hanuman Regular", 16))
    critical_lvl_label.place(x=50, y=320)

    barcode_entry = Entry(register_product_window, font=("Hanuman Regular", 16))
    barcode_entry.place(x=220, y=80, width=300)

    product_name_entry = Entry(register_product_window, font=("Hanuman Regular", 16))
    product_name_entry.place(x=220, y=170, width=300)

    product_price_entry = Entry(register_product_window, font=("Hanuman Regular", 16))
    product_price_entry.place(x=220, y=220, width=300)

    product_details_entry = Entry(register_product_window, font=("Hanuman Regular", 16))
    product_details_entry.place(x=220, y=270, width=300)
    
    critical_lvl_entry = Entry(register_product_window, font=("Hanuman Regular", 16))
    critical_lvl_entry.place(x=220, y=320, width=300)

    def generate_unique_barcode():
        while True:
            barcode_value = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=10))
            if is_barcode_unique(barcode_value):
                barcode_entry.delete(0, END)
                barcode_entry.insert(0, barcode_value)
                barcode = Code39(barcode_value, add_checksum=False)
                buffer = io.BytesIO()
                barcode.write(buffer)
                buffer.seek(0)
                break

    create_barcode_button = Button(register_product_window, text="Create Barcode", command=generate_unique_barcode, font=("Hanuman Regular", 12))
    create_barcode_button.place(x=315, y=118, width=120)

    def save_and_close():
        # Retrieve values from entry fields
        barcode = barcode_entry.get()
        product_name = product_name_entry.get()
        product_price_str = product_price_entry.get()
        product_details = product_details_entry.get()
        critical_lvl = critical_lvl_entry.get()

        # Check if any entry field is empty
        if not barcode or not product_name or not product_price_str:
            messagebox.showerror("Incomplete Information", "Please fill in Barcode, Product name, and Product price.")
            return

        # Convert product price to float (assuming it's a valid number)
        try:
            product_price = float(product_price_str)
        except ValueError:
            messagebox.showerror("Invalid Price", "Please enter a valid product price.")
            return

        # Register the product and show success message
        register_product(barcode, product_name, product_price, product_details, critical_lvl)
        messagebox.showinfo("Product Saved", "The product has been saved successfully!")
        
        # Log action
        action = "Registered a product: " + product_name + ", " + product_details + ", (PHP " + str(product_price_str) + ")"
        log_actions(username, action)

        # Update table and close the window
        update_table(show_individual=False)
        register_product_window.destroy()

    save_button = Button(register_product_window, text="Save", command=save_and_close, font=("Hanuman Regular", 16))
    save_button.place(x=250, y=420)

    canvas.create_rectangle(50.0, 50.0, 550.0, 430.0, fill="#FFE1C6", outline="")

    register_product_window.mainloop()

def add_supply_window():
    add_supply_window = Toplevel()
    add_supply_window.resizable(False, False)
    add_supply_window.title("Add Supply")
    add_supply_window.geometry("600x450")
    add_supply_window.configure(bg="#FFE1C6")

    window_width, window_height = 600, 450
    screen_width = add_supply_window.winfo_screenwidth()
    screen_height = add_supply_window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    add_supply_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    canvas = Canvas(add_supply_window, bg="#FFE1C6", height=500, width=600, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    add_label = Label(add_supply_window, text="Add Supply", bg="#FFE1C6", fg="#000000", font=("Hanuman Regular", 24))
    add_label.place(relx=0.5, rely=0.05, anchor="n")

    barcode_label = Label(add_supply_window, text="Barcode:", bg="#FFE1C6", font=("Hanuman Regular", 16))
    barcode_label.place(x=50, y=80)

    barcode_entry = Entry(add_supply_window, font=("Hanuman Regular", 16))
    barcode_entry.place(x=220, y=80, width=240)

    product_name_label = Label(add_supply_window, text="Product Name:", bg="#FFE1C6", font=("Hanuman Regular", 16))
    product_name_entry = Entry(add_supply_window, font=("Hanuman Regular", 16))

    product_quantity_label = Label(add_supply_window, text="Add Quantity:", bg="#FFE1C6", font=("Hanuman Regular", 16))
    product_quantity_entry = Entry(add_supply_window, font=("Hanuman Regular", 16))

    date_label = Label(add_supply_window, text="Date Delivered:", bg="#FFE1C6", font=("Hanuman Regular", 16))
    date_entry = DateEntry(add_supply_window, date_pattern="mm-dd-yyyy", width=12, background='darkblue', foreground='white', borderwidth=2, font=("Hanuman Regular", 16), state='disabled')

    supplier_label = Label(add_supply_window, text="Supplier:", bg="#FFE1C6", font=("Hanuman Regular", 16))
    supplier_entry = Entry(add_supply_window, font=("Hanuman Regular", 16))
    supplier_entry.config(state='disabled')

    def verify_barcode():
        barcode = barcode_entry.get().strip()
        print(f"Verifying barcode: {barcode}")  # Check if the function is called
        
        if not barcode:
            messagebox.showerror("Error", "Please enter a barcode.")
            return
        
        try:
            cursor.execute("SELECT Name FROM product WHERE Barcode = ?", (barcode,))
            product = cursor.fetchone()
            print(product)
            
            if not product:
                messagebox.showerror("Error", "No product with this barcode exists.")
                return
            
            # Enable and populate product_name_entry
            product_name_label.place(x=50, y=130)
            product_name_entry.place(x=220, y=130, width=300)
            product_name_entry.delete(0, END)
            product_name_entry.insert(0, product[0])
            product_name_entry.config(state='disabled')

            product_quantity_label.place(x=50, y=180)
            product_quantity_entry.place(x=220, y=180, width=300)
            product_quantity_entry.config(state='normal')

            date_label.place(x=50, y=230)
            date_entry.place(x=220, y=230)

            supplier_label.place(x=50, y=280)
            supplier_entry.place(x=220, y=280, width=300)
            supplier_entry.config(state='normal')

            # Enable other entry fields
            product_quantity_entry.config(state='normal')
            date_entry.config(state='normal')
            supplier_entry.config(state='normal')

            save_button = Button(add_supply_window, text="Save", command=save_supply, font=("Hanuman Regular", 16))
            save_button.place(x=250, y=330)
            
            
        
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error verifying barcode: {e}")

    verify_button = Button(add_supply_window, text="Verify", command=verify_barcode, font=("Hanuman Regular", 12))
    verify_button.place(x=470, y=78)

    def save_supply():
        barcode = barcode_entry.get().strip()
        product_name = product_name_entry.get().strip()
        product_quantity_str = product_quantity_entry.get().strip()
        date_delivered = date_entry.get_date()
        supplier = supplier_entry.get().strip()

        # Validate inputs
        if not barcode or not product_name or not product_quantity_str or not supplier:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        try:
            product_quantity = int(product_quantity_str)
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity. Please enter a valid number.")
            return

        try:
            cursor.execute("SELECT Barcode FROM product WHERE Barcode = ?", (barcode,))
            product = cursor.fetchone()

            if not product:
                messagebox.showerror("Error", "No product with this barcode exists.")
                return

            # Insert supply into inventory table
            cursor.execute('''
                INSERT INTO inventory (Barcode, Quantity, DateDelivered, Supplier)
                VALUES (?, ?, ?, ?)
            ''', (barcode, product_quantity, date_delivered, supplier))
            conn.commit()

            messagebox.showinfo("Supply Added", "Supply added successfully!")

            # Log action
            action = f"Added {product_quantity} to the product {barcode} from {supplier}."
            log_actions(username, action)
            update_table(show_individual=False)
            add_supply_window.destroy()

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error verifying barcode: {e}")

    canvas.create_rectangle(50.0, 50.0, 550.0, 430.0, fill="#FFE1C6", outline="")

    add_supply_window.mainloop()

def update_products_window():
    update_supply_window = Toplevel(window)
    update_supply_window.resizable(False, False)
    update_supply_window.title("Update Supply")
    update_supply_window.geometry("600x500")
    update_supply_window.configure(bg="#FFE1C6")

    window_width, window_height = 600, 500
    screen_width = update_supply_window.winfo_screenwidth()
    screen_height = update_supply_window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    update_supply_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    canvas = Canvas(update_supply_window, bg="#FFE1C6", height=500, width=600, bd=0, highlightthickness=0)
    
    add_label = Label(update_supply_window, text="Update Product", bg="#FFE1C6", fg="#000000", font=("Hanuman Regular", 24))
    add_label.place(relx=0.5, rely=0.05, anchor="n")

    barcode_label = Label(update_supply_window, text="Barcode:", bg="#FFE1C6", font=("Hanuman Regular", 16))
    barcode_label.place(x=50, y=80)

    barcode_entry = Entry(update_supply_window, font=("Hanuman Regular", 16))
    barcode_entry.place(x=220, y=80, width=240)

    product_name_label = Label(update_supply_window, text="Product Name:", bg="#FFE1C6", font=("Hanuman Regular", 16))
    product_name_entry = Entry(update_supply_window, font=("Hanuman Regular", 16))
    product_name_entry.config(state='disabled')

    product_price_label = Label(update_supply_window, text="Product Price:", bg="#FFE1C6", font=("Hanuman Regular", 16))
    product_price_entry = Entry(update_supply_window, font=("Hanuman Regular", 16))

    product_details_label = Label(update_supply_window, text="Product Details:", bg="#FFE1C6", font=("Hanuman Regular", 16))
    product_details_entry = Entry(update_supply_window, font=("Hanuman Regular", 16))
    
    critical_lvl_label = Label(update_supply_window, text="Critical Level:", bg="#FFE1C6", font=("Hanuman Regular", 16))
    critical_lvl_entry = Entry(update_supply_window, font=("Hanuman Regular", 16))
    
    product_status_label = Label(update_supply_window, text="Status:", bg="#FFE1C6", font=("Hanuman Regular", 16))
    product_status_var = BooleanVar()
    product_status_checkbox = Checkbutton(update_supply_window, text="Available", variable=product_status_var, bg="#FFE1C6", font=("Hanuman Regular", 16))

    def fetch_product_details():
        barcode = barcode_entry.get().strip()
        if not barcode:
            messagebox.showerror("Error", "Please enter a barcode.")
            return
        
        try:
            cursor.execute("SELECT * FROM product WHERE Barcode = ?", (barcode,))
            product = cursor.fetchone()
            print(product)
            if not product:
                messagebox.showerror("Error", "Product not found.")
                return

            # Display product details
            product_name_label.place(x=50, y=130)
            product_name_entry.place(x=220, y=130, width=300)
            product_name_entry.config(state='normal')
            product_name_entry.delete(0, END)
            product_name_entry.insert(0, product[1])

            product_price_label.place(x=50, y=180)
            product_price_entry.place(x=220, y=180, width=300)
            product_price_entry.config(state='normal')
            product_price_entry.delete(0, END)
            product_price_entry.insert(0, product[2])

            product_details_label.place(x=50, y=230)
            product_details_entry.place(x=220, y=230, width=300)
            product_details_entry.config(state='normal')
            product_details_entry.delete(0, END)
            product_details_entry.insert(0, product[3])

            product_status_label.place(x=50, y=330)
            product_status_checkbox.place(x=220, y=330)
            product_status_var.set(product[5] == 'Available')
            product_status_checkbox.config(state='normal')

            critical_lvl_label.place(x=50, y=280)
            critical_lvl_entry.place(x=220, y=280)
            critical_lvl_entry.delete(0, END)
            critical_lvl_entry.insert(0, product[4])

            save_button = Button(update_supply_window, text="Save", command=save_supply, font=("Hanuman Regular", 16))
            save_button.place(x=250, y=430)

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching product details: {e}")

    verify_button = Button(update_supply_window, text="Verify", command=fetch_product_details, font=("Hanuman Regular", 12))
    verify_button.place(x=470, y=77)

    def save_supply():
        barcode = barcode_entry.get().strip()
        product_name = product_name_entry.get().strip()
        product_price = float(product_price_entry.get().strip())
        product_details = product_details_entry.get().strip()
        critical_lvl = critical_lvl_entry.get().strip()
        product_status = 'Available' if product_status_var.get() else 'Unavailable'

        try:
            cursor.execute('''
                UPDATE product
                SET Name = ?, Price = ?, Details = ?, Status = ?, Critical_lvl = ?
                WHERE Barcode = ?
            ''', (product_name, product_price, product_details, product_status, critical_lvl, barcode))
            conn.commit()

            messagebox.showinfo("Supply Updated", "Supply updated successfully!")

            # Log action
            action = "Updated " + barcode + " to " + product_name + ", " + product_details + ". (PHP " + str(product_price) + ") Now " + product_status + "."
            log_actions(username, action)
            
            update_supply_window.destroy()
            update_table(show_individual=False)

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error updating supply: {e}")
    
    canvas.create_rectangle(50.0, 50.0, 550.0, 430.0, fill="#FFE1C6", outline="")

    update_supply_window.mainloop()

def update_table(show_individual=False):
    global barcode_updt
    try:
        # Fetch inventory data
        data = fetch_inventory_data(show_individual)

        # Clear existing rows in Treeview
        for row in my_tree.get_children():
            my_tree.delete(row)

        # Configure the tag for red font color
        my_tree.tag_configure('low_quantity', foreground='red')

        # Insert fetched data into Treeview with correct order
        for item in data:
            barcode_updt = item[0]
            name = item[1]
            price = float(item[2]) if item[2] is not None else 0.00  # Ensure price is a float
            quantity = item[3] if item[3] is not None else 0  # Handle None by setting to 0
            details = item[4]
            status = item[5]
            date_delivered = datetime.strptime(item[6], '%Y-%m-%d').date() if item[6] else None
            supplier = item[7]

            # Fetch critical level from the database
            cursor.execute("SELECT Critical_lvl FROM product WHERE Barcode = ?", (barcode_updt,))
            result = cursor.fetchone()
            critical_level = int(result[0]) if result and result[0] is not None else 0

            # Format the price to two decimal points
            formatted_price = f"{price:.2f}"

            # Determine the tag based on quantity
            tags = ('low_quantity',) if quantity <= critical_level else ()

            # Insert the item into the Treeview with the appropriate tag
            my_tree.insert('', 'end', values=(barcode_updt, name, formatted_price, quantity, details, status, date_delivered, supplier), tags=tags)

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error fetching data: {e}")
    except ValueError as ve:
        messagebox.showerror("Value Error", f"Invalid value encountered: {ve}")

def sort_treeview(tree, col, descending):
    data = [(float(tree.set(child, col)), child) for child in tree.get_children('')]
    
    data.sort(reverse=descending)
    
    for index, (val, child) in enumerate(data):
        tree.move(child, '', index)
    
    tree.heading(col, command=lambda: sort_treeview(tree, col, not descending))

def on_header_click(event):
    # Identify which column header was clicked
    region = my_tree.identify_region(event.x, event.y)
    if region == 'heading':
        column = my_tree.identify_column(event.x)
        print(column)
        column_name = my_tree.heading(column, 'text')
        print(column_name)

        # Determine current sort order or initialize if not set
        descending = SORT_ORDER.get(column_name, False)

        # Sort the Treeview
        sort_treeview(column_name, column, descending)

        # Toggle sort order for next click
        SORT_ORDER[column_name] = not descending
    
def combine_similar_barcodes():
    # Fetch all inventory data
    data = fetch_inventory_data()
    
    # Dictionary to store aggregated data
    combined_data = {}
    
    # Aggregate data based on barcode
    for item in data:
        barcode = item[0]
        quantity = item[3]
        date_delivered = item[6]
        supplier = item[7]
        
        if barcode in combined_data:
            # Update quantity if barcode exists
            combined_data[barcode]['Quantity'] += quantity
            
            # Update date_delivered if older
            if date_delivered < combined_data[barcode]['DateDelivered']:
                combined_data[barcode]['DateDelivered'] = date_delivered
                combined_data[barcode]['Supplier'] = supplier
        else:
            # Add new entry for barcode
            combined_data[barcode] = {
                'Barcode': barcode,
                'Quantity': quantity,
                'DateDelivered': date_delivered,
                'Supplier': supplier
            }
    
    
    # Clear existing rows in Treeview
    for row in my_tree.get_children():
        my_tree.delete(row)
    
    # Insert aggregated data into Treeview
    for barcode, values in combined_data.items():
        my_tree.insert('', 'end', values=(values['Barcode'], '', '', values['Quantity'], '', '', values['DateDelivered'], values['Supplier']))

def create_products_window():
    global window
    window = tk.Tk()
    window.geometry("1280x800")
    window.configure(bg="#FFE1C6")
    window.title("Products")

    window_width, window_height = 1280, 800
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    canvas = Canvas(window, bg="#FFE1C6", height=800, width=1280, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    back_button = Button(window, text="Back", command=lambda: go_to_window("back"), font=("Hanuman Regular", 16), bg="#FFFFFF", relief="raised")
    back_button.place(x=1071.0, y=696.0, width=169.0, height=64.0)

    show_individual_var = IntVar(value=-1)

    def toggle_view():
        global show_individual
        show_individual = (show_individual_var.get() == 0)  # 0 for Individual View, 1 for Multiple View
        update_table(show_individual)

    loa=shared_state.current_user_loa
    if loa == "admin":
        register_product_button = Button(window, text="Register Product", command=lambda: register_product_window(), font=("Hanuman Regular", 16), bg="#83F881", relief="raised")
        register_product_button.place(x=41.0, y=691.0, width=237.84408569335938, height=73.0)

        update_product_button = Button(window, text="Update Products", command=lambda: update_products_window(), font=("Hanuman Regular", 16), bg="#81CDF8", relief="raised")
        update_product_button.place(x=617.0, y=691.0, width=237.84408569335938, height=73.0)

        add_supply_button = Button(window, text="Add Supply", command=lambda: add_supply_window(), font=("Hanuman Regular", 16), bg="#81CDF8", relief="raised")
        add_supply_button.place(x=329.0, y=691.0, width=237.84408569335938, height=73.0)

          # Variable to store checkbox state (0 for False, 1 for True)
        multiple_button = Radiobutton(window, text="Individual View", variable=show_individual_var, value=0,
                                command=toggle_view, font=("Hanuman Regular", 12), bg="#FFE1C6")
        multiple_button.place(x=41, y=148)

        individual_button = Radiobutton(window, text="Multiple View", variable=show_individual_var, value=1,
                                    command=toggle_view, font=("Hanuman Regular", 12), bg="#FFE1C6")
        individual_button.place(x=171, y=148)

    canvas.create_rectangle(41.0, 176.0, 1240.0, 658.0, fill="#FFFFFF", outline="")

    canvas.create_text(41.0, 20.0, anchor="nw", text= f"{loa}", fill="#000000", font=("Hanuman Regular", 20))

    search_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Hanuman Regular", 24))
    search_entry.place(x=41.0, y=92.0, width=300, height=47)

    def on_search():
        keyword = search_entry.get().strip()  # Get the input and strip any leading/trailing whitespace
        if keyword:  # Check if keyword is not empty
            if show_individual:
                # Show multiple rows based on the search result
                rows = search_inventory_linear(keyword)
                my_tree.delete(*my_tree.get_children())
                for row in rows:
                    my_tree.insert("", "end", values=row)
            else:
                # Show only one row for the primary key
                row = search_inventory_linear(keyword, individual=True)  # Assuming a function that fetches only one row for the primary key
                if row:
                    my_tree.delete(*my_tree.get_children())
                    my_tree.insert("", "end", values=row)
        else:
            # Handle case where keyword is empty (optional)
            update_table(show_individual=False)

    def on_enter_pressed(event):
        on_search()

    search_button = Button(window, text="Search", command=on_search, font=("Hanuman Regular", 16), bg="#FFE1C6")
    search_button.place(x=350, y=92, width=100, height=47)
    search_entry.bind("<Return>", on_enter_pressed)
    canvas.create_text(41.0, 50.0, anchor="nw", text="Search Product", fill="#000000", font=("Hanuman Regular", 28))

    # Create a style for the Treeview
    style = ttk.Style()
    style.configure("Treeview", background="#FFFFFF", foreground="#000000", rowheight=25,
                    fieldbackground="#FFFFFF", font=("Hanuman Regular", 12))

    # Create a style for the Treeview heading
    style.configure("Treeview.Heading", font=("Hanuman Regular", 14))


    # Create Treeview widget
    global my_tree
    my_tree = ttk.Treeview(window, columns=("Barcode", "Name", "Price", "Quantity", "Details", "Status", "Date Delivered", "Supplier"), selectmode="extended")
    my_tree.place(x=41.0, y=176.0, width=1199.0, height=482.0)  # Adjusted position and size to match the white rectangle

    for col, heading in enumerate(["Barcode", "Name", "Price", "Quantity", "Details", "Status", "DateDelivered", "Supplier"]):
        my_tree.heading(col, text=heading, anchor='w', command=lambda c=col: sort_treeview(my_tree, c, False))
        my_tree.column(col, anchor='center')

    # Define columns
    my_tree.heading("#0", text="", anchor="center")
    my_tree.heading("Barcode", text="Barcode", anchor="center")
    my_tree.heading("Name", text="Product Name", anchor="center")
    my_tree.heading("Price", text="Price", anchor="center")
    my_tree.heading("Quantity", text="Quantity", anchor="center")
    my_tree.heading("Details", text="Details", anchor="center")
    my_tree.heading("Status", text="Status", anchor="center")
    my_tree.heading("Date Delivered", text="Date Delivered", anchor="center")
    my_tree.heading("Supplier", text="Supplier", anchor="center")

    # Define column widths
    my_tree.column("#0", stretch=False, width=0)  # Hidden column
    my_tree.column("Barcode", anchor="center", width=50)
    my_tree.column("Name", anchor="center", width=70)
    my_tree.column("Price", anchor="center", width=30)
    my_tree.column("Quantity", anchor="center", width=30)
    my_tree.column("Details", anchor="center", width=70)
    my_tree.column("Status", anchor="center", width=50)
    my_tree.column("Date Delivered", anchor="center", width=70)
    my_tree.column("Supplier", anchor="center", width=100)

    # Create vertical scrollbar
    vsb = Scrollbar(window, orient="vertical", command=my_tree.yview)
    vsb.place(x=1240, y=176, height=482)  # Adjusted height to match the Treeview height

    # Configure Treeview to use vertical scrollbar
    my_tree.configure(yscrollcommand=vsb.set)

    update_table(show_individual=False)

    my_tree.bind('<Button-1>', on_header_click)

    window.resizable(False, False)
    window.mainloop()

if __name__ == "__main__":
    create_products_window()
