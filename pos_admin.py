import sqlite3
import tkinter as tk
import win32print
from datetime import datetime
from pathlib import Path
from tkinter import Button, Canvas, Entry, Label, messagebox, PhotoImage, simpledialog, ttk

# From user made modules
import shared_state
from maintenance import update_first_name, update_last_name, update_email, update_password, update_phone_number
from new_pass import is_valid_password
from registration import is_valid_contact_number, is_valid_email, is_valid_name
from salt_and_hash import generate_salt, hash_password
from user_logs import log_actions

# Define the path to your assets folder
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\Pos Admin")

# Initialize an empty list to store purchased items
purchase_list = []
void_list= []
def relative_to_assets(path: str) -> Path:
    """Returns the absolute path to an asset relative to ASSETS_PATH."""
    return ASSETS_PATH / Path(path)

def connect_db():
    """Connects to the SQLite database."""
    conn = sqlite3.connect('Trimark_construction_supply.db')
    return conn

def search_barcode(barcode):
    """Searches for a product in the inventory database by barcode."""
    conn = connect_db()
    cursor = conn.cursor()

    # Corrected SQL query to join product and inventory tables
    cursor.execute("""
        SELECT p.Name, i.Quantity, p.Price, p.Barcode
        FROM product p
        INNER JOIN inventory i ON p.Barcode = i.Barcode
        WHERE p.Barcode = ?
    """, (barcode,))
    
    result = cursor.fetchone()

    conn.close()
    return result

def on_barcode_entry(event):
    """Handles the event when a barcode is entered."""
    barcode_value = barcode.get()
    result = search_barcode(barcode_value)

    if result:
        if len(result) == 3:
            product_name, product_quantity, product_price = result
            product_barcode = None  # Or fetch from database if available
        elif len(result) == 4:
            product_name, product_quantity, product_price, product_barcode = result
        else:
            messagebox.showerror("Search Result Error", "Invalid result returned by search function")
            return
        
        product_found = False

        # Check if the product is already in the purchase list
        for item in purchase_list:
            if item.get('name') == product_name and item.get('barcode') == product_barcode:
                # Increment quantity and update total price
                item['quantity'] += 1
                item['total_price'] += product_price
                product_found = True
                break

        if not product_found:
            # Add new product to the purchase list
            purchase_list.append({
                'name': product_name,
                'quantity': 1,
                'price': product_price,
                'total_price': product_price,
                'barcode': product_barcode  # Include barcode in the purchase list item
            })

        # Update the display of products being purchased
        update_purchase_display()

        # Update the total label
        update_total_label()

        # Clear the barcode entry after processing
        barcode.delete(0, 'end')

    else:
        messagebox.showwarning("Search Result", "Product Not Found")

def update_purchase_display():
    """Updates the display of products being purchased."""
    # Clear previous entries in the treeview
    for item in tree.get_children():
        tree.delete(item)

    # Insert each product into the treeview
    for idx, item in enumerate(purchase_list, start=1):
        tree.insert("", "end", values=(idx, item['name'], item['quantity'], f"Php {item['price']}", f"Php {item['total_price']}"))

def update_total_label():
    """Updates the total label with the calculated total amount."""
    total_amount = sum(item['total_price'] for item in purchase_list)
    total_label.config(text=f"Total: Php {total_amount:.2f}")

def go_to_window(window_type):
    """Destroys the current window and opens another window based on window_type."""
    window.destroy()
    if window_type == "logout":
        log_actions(shared_state.current_user, "Logged Out")
        shared_state.current_user = None
        shared_state.current_user_loa = None
        import login
        login.create_login_window()
    elif window_type == "inventory":
        import products
        products.create_products_window()
    elif window_type == "register":
        import registration
        registration.create_registration_window()
    elif window_type == "barcode":
        import barcode_ad
        barcode_ad.create_barcode_window()
    elif window_type == "backup_restore":  
        import backup_restore
        backup_restore.create_backup_restore_window()
    elif window_type == "reports":  
        import reports
        reports.create_reports_window()

def create_pos_admin_window():
    # Creates and configures the POS admin window.
    global window
    window = tk.Tk()
    window.geometry("1280x800")
    window.configure(bg="#FFE1C6")
    window.title("POS")

    # Center the window on the screen
    window_width, window_height = 1280, 800
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    # Create a canvas to place widgets on
    global canvas
    canvas = Canvas(window, bg="#FFE1C6", height=800, width=1280, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    # Barcode entry widget
    global barcode
    barcode = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=1, font=("Hanuman Regular", 28 * -1))
    barcode.place(x=699.0, y=127.0, width=552.0, height=58.0)
    barcode.bind("<Return>", on_barcode_entry)  # Bind the Return (Enter) key to trigger the search

    # Treeview widget to display purchased items
    global tree
    tree = ttk.Treeview(window, columns=("Index", "Product Name", "Quantity", "Price", "Total Price"), show="headings")
    tree.heading("Index", text="Index", anchor=tk.CENTER)
    tree.heading("Product Name", text="Product Name", anchor=tk.CENTER)
    tree.heading("Quantity", text="Quantity", anchor=tk.CENTER)
    tree.heading("Price", text="Price", anchor=tk.CENTER)
    tree.heading("Total Price", text="Total Price", anchor=tk.CENTER)
    tree.column("Index", width=50, anchor=tk.CENTER)
    tree.column("Product Name", width=200, anchor=tk.CENTER)
    tree.column("Quantity", width=100, anchor=tk.CENTER)
    tree.column("Price", width=100, anchor=tk.CENTER)
    tree.column("Total Price", width=120, anchor=tk.CENTER)
    tree.place(x=41.0, y=127.0, width=631.0, height=496.0)

    # Total Label
    global total_label
    total_label = Label(window, text="Total: Php 0.00", font=("Arial", 30, "bold"), bg="#FFE1C6")
    total_label.place(x=699.0, y=200.0)

    # Buttons for various actions
    logout_button = Button(text="Logout", font=("Hanuman Regular", 16), command=lambda: go_to_window("logout"), bg="#FFFFFF", relief="raised")
    logout_button.place(x=1071.0, y=691.0, width=168.86373901367188, height=44.19459533691406)

    help_button = Button(text="Help", font=("Hanuman Regular", 16), command=lambda: print("Help"), bg="#FFFFFF", relief="raised")
    help_button.place(x=1071.0, y=623.0, width=168.86373901367188, height=44.19459533691406)

    purchase_button = Button(text="Purchase", font=("Hanuman Regular", 20), command=open_purchase_window, bg="#83F881", relief="raised")
    purchase_button.place(x=42.0, y=623.0, width=464.28277587890625, height=112.0)

    inventory_button = Button(text="Inventory", font=("Hanuman Regular", 20), command=lambda: go_to_window("inventory"), bg="#81CDF8", relief="ridge")
    inventory_button.place(x=699.0, y=623.0, width=170.28277587890625, height=112.0)


    loa = "admin"
    if loa == "admin":
        # Accounts (Register) button
        register_button = Button(text="Accounts", font=("Hanuman Regular", 20), command=lambda: go_to_window("register"), bg="#81CDF8", relief="ridge")
        register_button.place(x=699.0, y=477.0, width=170.28277587890625, height=112.0)

        reports_button = Button(text="Reports", font=("Hanuman Regular", 20), command=lambda: go_to_window("reports"), bg="#81CDF8", relief="ridge")
        reports_button.place(x=884.0, y=477.0, width=170.28277587890625, height=112.0)

        backup_restore = Button(text="Backup\nRestore", font=("Hanuman Regular", 20), command=lambda: go_to_window("backup_restore"), bg="#81CDF8", relief="ridge")
        backup_restore.place(x=1068.0, y=477.0, width=170.28277587890625, height=112.0)

    barcodes_button = Button(text="Barcode", font=("Hanuman Regular", 20), command=lambda: go_to_window("barcode"), bg="#81CDF8", relief="ridge")
    barcodes_button.place(x=884.0, y=623.0, width=170.28277587890625, height=112.0)

    # Void button function
    def void_items():
        void_list  # Access void_list from the outer scope

        # Move items from purchase_list to void_list
        void_list.extend(purchase_list)
        print(void_list)
        purchase_list.clear()

        # Update display of products being purchased and total label
        update_purchase_display()
        update_total_label()

        action = "Voided transaction."
        log_actions(shared_state.current_user, action)

    void_button = Button(text="Void", font=("Hanuman Regular", 20), command=void_items, bg="#FF9E9E", relief="raised")
    void_button.place(x=506.0, y=623.0, width=166.0, height=112.0)

    # Draw shapes and texts on canvas
    canvas.create_rectangle(41.0, 62.0, 672.0, 127.0, fill="#FF4E4E", outline="")
    canvas.create_text(286.0, 71.0, anchor="nw", text="Checkout", fill="#FFFFFF", font=("Hanuman Regular", 32 * -1))
    canvas.create_text(699.0, 85.0, anchor="nw", text="Barcode or Product Name", fill="#000000", font=("Hanuman Regular", 28 * -1))
    canvas.create_text(91.0, 20.0, anchor="nw",
        text=f"{str(shared_state.current_user_loa).capitalize()}, {shared_state.current_user}",
        fill="#000000",
        font=("Hanuman Regular", 20 * -1, "bold")
    )

    def show_hamburger_menu():
        """Shows the hamburger menu with options."""
        menu = tk.Menu(window, tearoff=0)
        menu_items = [
            ("Change First Name", "first_name"),
            ("Change Last Name", "last_name"),
            ("Change Password", "password"),
            ("Change Email", "email"),
            ("Change Phone Number", "phone_number")
        ]

        for label, command_name in menu_items:
            menu.add_command(label=label, command=lambda cmd=command_name: perform_action(cmd))

        # Calculate position for the menu
        x_coord = hamburger_button.winfo_rootx()
        y_coord = hamburger_button.winfo_rooty() + hamburger_button.winfo_height()
        menu.tk_popup(x_coord, y_coord)

    def perform_action(command_name):
        """Performs the appropriate action based on the command_name."""
        if shared_state.current_user:
            username = shared_state.current_user  # Assuming current_user stores the username
            employee_id = get_employee_id(username) # Fetch the Employee_ID using the username

            if command_name == "first_name":
                new_first_name = simpledialog.askstring("Change First Name", "Enter new first name:")
                if new_first_name:
                    if is_valid_name(new_first_name):
                        update_first_name(employee_id, new_first_name)
                    else:
                        messagebox.showerror("Error", "Invalid first name format")

            elif command_name == "last_name":
                new_last_name = simpledialog.askstring("Change Last Name", "Enter new last name:")
                if new_last_name:
                    if is_valid_name(new_last_name):
                        update_last_name(employee_id, new_last_name)
                    else:
                        messagebox.showerror("Error", "Invalid last name format")

            elif command_name == "password":
                new_password = simpledialog.askstring("Change Password", "Enter new password:")
                if new_password:
                    valid, message = is_valid_password(new_password)
                    if valid:
                        repeat_password = simpledialog.askstring("Change Password", "Repeat new password:")
                        if new_password == repeat_password:
                            salt = generate_salt()
                            hashed_password = hash_password(new_password, salt)
                            update_password(employee_id, hashed_password, salt)
                        else:
                            messagebox.showerror("Error", "Passwords do not match")
                    else:
                        messagebox.showerror("Error", message)

            elif command_name == "email":
                new_email = simpledialog.askstring("Change Email", "Enter new email:")
                if new_email:
                    valid, message = is_valid_email(new_email)
                    if valid:
                        unique, unique_message = check_email_uniqueness(new_email, current_email=username)
                        if unique:
                            update_email(employee_id, new_email)
                        else:
                            messagebox.showerror("Error", unique_message)
                    else:
                        messagebox.showerror("Error", message)

            elif command_name == "phone_number":
                new_phone_number = simpledialog.askstring("Change Phone Number", "Enter new phone number:")
                if new_phone_number:
                    if is_valid_contact_number(new_phone_number):
                        update_phone_number(employee_id, new_phone_number)
                    else:
                        messagebox.showerror("Error", "Invalid phone number format")

    # Hamburger menu icon
    hamburger_icon = PhotoImage(file=relative_to_assets("hamburger.png"))
    hamburger_icon_resized = hamburger_icon.subsample(6, 6)
    hamburger_button = Button(window, image=hamburger_icon_resized, borderwidth=0, highlightthickness=0, command=show_hamburger_menu, relief="flat")
    hamburger_button.image = hamburger_icon  # Keep a reference to the image to prevent garbage collection
    hamburger_button.place(x=41, y=15)

    # Update display of products being purchased and total label
    update_purchase_display()
    update_total_label()

    window.mainloop()

def get_employee_id(username):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # Execute a SELECT query to fetch Employee_ID based on the Username
        cursor.execute("SELECT Employee_ID FROM accounts WHERE Username = ?", (username,))
        employee_id = cursor.fetchone()  # Fetch the first row

        if employee_id:
            return employee_id[0]  # Return the Employee_ID (assuming it's the first column in the result)
        else:
            return None  # Return None if no employee ID found for the given username

    except sqlite3.Error as e:
        print(f"Error fetching employee ID: {e}")
        return None

    finally:
        conn.close()

def check_email_uniqueness(email, current_email=None):
    """Check if the email is unique among existing emails in the database."""
    conn = connect_db()
    cursor = conn.cursor()

    # Fetch existing emails from the database
    cursor.execute("SELECT Email FROM accounts")
    existing_emails = [row[0] for row in cursor.fetchall()]

    conn.close()

    if email in existing_emails and email != current_email:
        return False, "Email already in use"
    return True, ""
    
def insert_purchase_history(purchase_list, total_amount, customer_money, change, cashier_name, customer_name, purchase_id):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # Insert each item in the purchase list into the purchase_history table
        for item in purchase_list:
            cursor.execute('''
                INSERT INTO purchase_history (
                    Purchase_ID, First_Name, Product_Name, Product_Price, Purchase_Quantity, 
                    Total_Price, Amount_Given, Change
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                purchase_id, customer_name, item['name'], item['price'], item['quantity'],
                item['total_price'], customer_money, change
            ))

        conn.commit()
        print("Purchase history inserted successfully.")

    except sqlite3.Error as e:
        conn.rollback()
        print(f"Error inserting purchase history: {e}")

    finally:
        conn.close()

def open_purchase_window():
    conn = connect_db()
    cursor = conn.cursor()
    purchase_window = tk.Toplevel(window)
    purchase_window.title("Purchase")
    purchase_window.geometry("400x300")
    
    print(purchase_list)

    tk.Label(purchase_window, text="Customer Name (optional):").pack(pady=5)
    customer_name_entry = tk.Entry(purchase_window)
    customer_name_entry.pack(pady=5)

    tk.Label(purchase_window, text="Customer Contact Number (optional):").pack(pady=5)
    customer_contact_entry = tk.Entry(purchase_window)
    customer_contact_entry.pack(pady=5)

    tk.Label(purchase_window, text="Customer Money:").pack(pady=5)
    customer_money_entry = tk.Entry(purchase_window)
    customer_money_entry.pack(pady=5)

    cursor.execute("""
        SELECT First_Name, Last_Name
        FROM accounts
        WHERE Username = ?
    """, (shared_state.current_user,))
    
    cashier_name = cursor.fetchone()
    
    conn.close()
    cashier_name = f"{cashier_name[0]} {cashier_name[1]}" if cashier_name and len(cashier_name) >= 2 else "Unknown Cashier"
    tk.Button(purchase_window, text="Process Purchase", command=lambda: process_purchase(cashier_name, customer_name_entry.get(), customer_contact_entry.get(), customer_money_entry.get(), purchase_window)).pack(pady=20)

def process_purchase(cashier_name, customer_name, customer_contact, customer_money, purchase_window):
    try:
        customer_money = float(customer_money)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid amount for customer money.")
        return

    total_amount = sum(item.get('total_price', 0) for item in purchase_list)

    if customer_money < total_amount:
        messagebox.showerror("Insufficient Funds", "Customer money is less than the total amount.")
        return

    if not check_product_availability(purchase_list):
        messagebox.showerror("Unavailable Product", "One or more products in the purchase list are unavailable.")
        return

    if not update_inventory(purchase_list):
        messagebox.showerror("Inventory Error", "An error occurred while updating the inventory.")
        return

    change = customer_money - total_amount
    purchase_id = datetime.now().strftime("%Y%m%d%H%M%S")
    create_receipt(cashier_name, customer_name, customer_contact, customer_money, change, purchase_list)
    messagebox.showinfo("Purchase Complete", f"Purchase successful!\nChange: Php {change:.2f}")

    # Generate a unique Purchase_ID for this transaction
    

    insert_purchase_history(purchase_list, total_amount, customer_money, change, cashier_name, customer_name, purchase_id)

    action = "Checked out and generated PDF file for the receipt."
    log_actions(shared_state.current_user, action)

    purchase_list.clear()
    update_purchase_display()
    update_total_label()
    purchase_window.destroy()

def check_product_availability(purchase_list):
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        for item in purchase_list:
            if 'barcode' not in item:
                print(f"Error: 'barcode' key missing in item: {item}")
                continue  # Skip items without barcode

            cursor.execute("SELECT Status FROM product WHERE Barcode = ?", (item['barcode'],))
            status = cursor.fetchone()

            if not status or status[0] != 'Available':
                return False
        return True

    except sqlite3.Error as e:
        print(f"Error checking product availability: {e}")
        return False

    finally:
        conn.close()

def update_inventory(purchase_list):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # Start a transaction
        conn.execute("BEGIN TRANSACTION;")

        for item in purchase_list:
            if 'barcode' not in item:
                print(f"Error: 'barcode' key missing in item: {item}")
                continue  # Skip items without barcode

            barcode = item['barcode']
            remaining_quantity = item['quantity']

            # Retrieve the current available quantities for the product in inventory
            cursor.execute("""
                SELECT InventoryID, Quantity
                FROM inventory
                WHERE Barcode = ? AND Quantity > 0
                ORDER BY DateDelivered ASC
            """, (barcode,))
            quantities = cursor.fetchall()

            for inventory_id, quantity in quantities:
                if remaining_quantity <= 0:
                    break

                if quantity >= remaining_quantity:
                    new_quantity = quantity - remaining_quantity
                    cursor.execute("UPDATE inventory SET Quantity = ? WHERE InventoryID = ?", (new_quantity, inventory_id))
                    remaining_quantity = 0
                else:
                    remaining_quantity -= quantity
                    cursor.execute("UPDATE inventory SET Quantity = 0 WHERE InventoryID = ?", (inventory_id,))

        # Commit the transaction
        conn.commit()
        print("Inventory updated successfully.")
        return True

    except sqlite3.Error as e:
        # Rollback the transaction in case of an error
        conn.rollback()
        print(f"Error updating inventory: {e}")
        return False

    finally:
        # Close the database connection
        conn.close()

def create_receipt(cashier_name, customer_name, customer_contact, customer_money, change, purchase_list):
    # Adjusting the width for 58mm receipt paper
    receipt_text = f"""
********************************
  Trimark Construction Supply
********************************
   No. 39 Scout Ybardolaza St. 
    Sacred Heart, Quezon City
     Tel. No. (02) 926-2329 
********************************
Cashier: {cashier_name}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
********************************
Customer Name: {customer_name}
Customer Contact: {customer_contact}
********************************
Items:
"""

    max_item_name_length = 30  # Adjust this as needed for your receipt layout

    subtotal = 0.0
    for item in purchase_list:
        # Determine how much space is left for the item name after accommodating the quantity and other text
        available_name_space = max_item_name_length - len(f" x {item['quantity']:2} - Php {item['total_price']:.2f}")

        # Truncate or pad the item name accordingly
        truncated_name = item['name'][:available_name_space].ljust(available_name_space)

        # Format the item line with adjusted spacing
        item_line = f"{truncated_name} x {item['quantity']:2} - Php {item['total_price']:.2f}\n"
        receipt_text += item_line

        # Accumulate subtotal
        subtotal += item['total_price']



    receipt_text += f"""
********************************
Total: Php {subtotal:.2f}
********************************
Bill Given: Php {customer_money:.2f}
Change: Php {change:.2f}
********************************
Thank you for your purchase!
********************************

        """
    
    print_receipt(receipt_text)

def print_receipt(receipt_text):
    # ESC/POS commands
    ESC = chr(23)
    GS = chr(25)
    initialize_printer = ESC 
    select_small_font = ESC 
    cut_paper = GS 

    # Combine commands with the receipt text
    full_text = initialize_printer + select_small_font + receipt_text + cut_paper

    # Get the default printer
    printer_name = win32print.GetDefaultPrinter()
    hPrinter = win32print.OpenPrinter(printer_name)
    try:
        # Start a print job
        hJob = win32print.StartDocPrinter(hPrinter, 1, ("Receipt", None, "RAW"))
        win32print.StartPagePrinter(hPrinter)
        
        # Send the receipt text to the printer
        win32print.WritePrinter(hPrinter, full_text.encode('utf-8'))
        
        # End the print job
        win32print.EndPagePrinter(hPrinter)
        win32print.EndDocPrinter(hPrinter)
    finally:
        win32print.ClosePrinter(hPrinter)

if __name__ == "__main__":
    create_pos_admin_window()
