import tkinter as tk
from tkinter import Button, Entry, Label, messagebox, simpledialog, ttk
from pathlib import Path
import sqlite3
from datetime import datetime

# Define the path to your assets folder
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\Pos Admin")

# Initialize an empty list to store purchased items
purchase_list = []
void_list = []

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

        # Ensure product_quantity is not zero
        if product_quantity <= 0:
            messagebox.showwarning("Quantity Error", f"The quantity of '{product_name}' is zero or negative. Please check.")
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

def open_manual_entry():
    """Opens a dialog box to manually input a barcode."""
    manual_barcode = simpledialog.askstring("Manual Barcode Entry", "Enter Barcode:")
    if manual_barcode:
        barcode.delete(0, 'end')
        barcode.insert(0, manual_barcode)

def open_quantity_input():
    """Prompts the user to enter quantity for the scanned product."""
    if purchase_list:
        quantity = simpledialog.askinteger("Quantity Input", "Enter Quantity:")
        if quantity:
            # Update the quantity of the last scanned item
            purchase_list[-1]['quantity'] = quantity
            purchase_list[-1]['total_price'] = purchase_list[-1]['price'] * quantity

            # Update the display
            update_purchase_display()
            update_total_label()
    else:
        messagebox.showwarning("No Product Scanned", "Please scan a product first.")

def create_pos_admin_window():
    # Creates and configures the POS admin window.
    global window
    window = tk.Tk()
    window.geometry("1280x800")
    window.configure(bg="#FFE1C6")
    window.title("POS")

    # Barcode entry widget
    global barcode
    barcode = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=1, font=("Hanuman Regular", 28))
    barcode.place(x=699.0, y=127.0, width=552.0, height=58.0)
    barcode.bind("<Return>", on_barcode_entry)  # Bind the Return (Enter) key to trigger the search

    # Manual Input Button
    manual_button = Button(text="Manual Input", font=("Hanuman Regular", 16), command=open_manual_entry, bg="#FFFFFF", relief="raised")
    manual_button.place(x=699.0, y=191.0, width=150, height=44)

    # Quantity Input Button
    quantity_button = Button(text="Quantity", font=("Hanuman Regular", 16), command=open_quantity_input, bg="#FFFFFF", relief="raised")
    quantity_button.place(x=859.0, y=191.0, width=150, height=44)

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
    tree.place(x=41.0, y=250.0, width=1210.0, height=500.0)

    # Total Label
    global total_label
    total_label = Label(window, text="Total: Php 0.00", font=("Arial", 30, "bold"), bg="#FFE1C6")
    total_label.place(x=699.0, y=770.0)

    window.mainloop()

if __name__ == "__main__":
    create_pos_admin_window()
