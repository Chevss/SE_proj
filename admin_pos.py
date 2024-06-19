from pathlib import Path
import tkinter as tk
from tkinter import ttk, Canvas, Entry, Text, Button, PhotoImage, Label, messagebox
import sqlite3
import datetime

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\TIPQC\Downloads\SE_proj-main\assets\Pos Admin")

purchase_list = []

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def connect_db():
    conn = sqlite3.connect('Trimark_construction_supply.db')
    return conn

def search_barcode(barcode):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT Product_Name, Product_Quantity, Product_Price FROM inventory WHERE Barcode = ?", (barcode,))
    result = cursor.fetchone()

    conn.close()
    return result

def on_barcode_entry(event):
    barcode_value = barcode.get()
    result = search_barcode(barcode_value)

    if result:
        product_name, product_quantity, product_price = result

        if product_quantity > 0:  # Check if product is available
            product_found = False

            # Check if the product is already in the purchase list
            for item in purchase_list:
                if item['name'] == product_name:
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
                    'total_price': product_price
                })

            # Update the display of products being purchased
            update_purchase_display()

            # Update the total label
            update_total_label()

            # Clear the barcode entry after processing
            barcode.delete(0, 'end')

        else:
            messagebox.showwarning("Product Unavailable", "This product is currently out of stock.")

    else:
        messagebox.showwarning("Search Result", "Product Not Found")

def update_purchase_display():
    # Clear previous entries in the treeview
    for item in tree.get_children():
        tree.delete(item)

    # Insert each product into the treeview
    for idx, item in enumerate(purchase_list, start=1):
        tree.insert("", "end", values=(idx, item['name'], item['quantity'], f"Php {item['price']:.2f}", f"Php {item['total_price']:.2f}"))


def update_total_label():
    total_amount = sum(item['total_price'] for item in purchase_list)
    total_label.config(text=f"Total: Php {total_amount:.2f}")

def go_to_window(windows):
    window.destroy()
    if windows == "logout":
        import login
        login.create_login_window()
    elif windows == "inventory":
        import inventory_admin
        inventory_admin.create_inventory_window()

def create_pos_admin_window():
    global window
    window = tk.Tk()
    window.geometry("1280x800")
    window.configure(bg="#FFE1C6")
    window.title("POS")

    window_width, window_height = 1280, 800
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Set the window geometry and position
    window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    global canvas
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
    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(975.0, 157.0, image=entry_image_1)

    global barcode
    barcode = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        font=("Hanuman Regular", 24 * -1)
    )
    barcode.place(x=699.0, y=127.0, width=552.0, height=58.0)
    barcode.bind("<Return>", on_barcode_entry)  # Bind the Return (Enter) key to trigger the search

    # Create treeview widget with columns
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

    # Configure the font for the treeview headings and rows
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 14, "bold"))
    style.configure("Treeview", font=("Arial", 12))

    # Place the treeview to match the white rectangle's size and position
    tree.place(x=41.0, y=127.0, width=631.0, height=608.0)

    # Total Label
    global total_label
    total_label = Label(window, text="Total: Php 0.00", font=("Arial", 20, "bold"), bg="#FFE1C6")
    total_label.place(x=699.0, y=200.0)  # Adjust Y position as needed

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    logout_button = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: go_to_window("logout"),
        relief="flat"
    )
    logout_button.place(x=1071.0, y=691.0, width=168.86373901367188, height=44.19459533691406)

    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    help_button = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("Help Button"),
        relief="flat"
    )
    help_button.place(x=1071.0, y=623.0, width=168.86373901367188, height=44.19459533691406)

    button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
    purchase_button = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=open_purchase_window,
        relief="flat"
    )
    purchase_button.place(x=699.0, y=623.0, width=170.28277587890625, height=112.0)

    button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
    inventory_button = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: go_to_window("inventory"),
        relief="flat"
    )
    inventory_button.place(x=699.0, y=479.0, width=170.28277587890625, height=112.0)

    button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
    reports_button = Button(
        image=button_image_5,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("Reports Button"),
        relief="flat"
    )
    reports_button.place(x=884.0, y=478.0, width=170.28277587890625, height=112.0)

    button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
    maintenance_button = Button(
        image=button_image_6,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("Maintenance Button"),
        relief="flat"
    )
    maintenance_button.place(x=1068.0, y=477.0, width=170.28277587890625, height=112.0)

    button_image_7 = PhotoImage(file=relative_to_assets("button_7.png"))
    edit_button = Button(
        image=button_image_7,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("Edit Button"),
        relief="flat"
    )
    edit_button.place(x=884.0, y=623.0, width=166.0, height=112.0)

    canvas.create_rectangle(
        41.0,
        127.0,
        672.0,
        735.0,
        fill="#FFFFFF",
        outline=""
    )

    canvas.create_rectangle(
        41.0,
        62.0,
        672.0,
        127.0,
        fill="#FF4E4E",
        outline=""
    )

    canvas.create_text(
        286.0,
        71.0,
        anchor="nw",
        text="Checkout",
        fill="#FFFFFF",
        font=("Hanuman Regular", 32 * -1)
    )

    canvas.create_text(
        699.0,
        85.0,
        anchor="nw",
        text="Barcode or Product Name",
        fill="#000000",
        font=("Hanuman Regular", 28 * -1)
    )

    canvas.create_text(
        41.0,
        20.0,
        anchor="nw",
        text="Admin",
        fill="#000000",
        font=("Hanuman Regular", 20 * -1)
    )

    window.resizable(False, False)
    window.mainloop()

def open_purchase_window():
    purchase_window = tk.Toplevel(window)
    purchase_window.title("Purchase")
    purchase_window.geometry("400x300")

    tk.Label(purchase_window, text="Customer Name (optional):").pack(pady=5)
    customer_name_entry = tk.Entry(purchase_window)
    customer_name_entry.pack(pady=5)

    tk.Label(purchase_window, text="Customer Contact Number (optional):").pack(pady=5)
    customer_contact_entry = tk.Entry(purchase_window)
    customer_contact_entry.pack(pady=5)

    tk.Label(purchase_window, text="Customer Money:").pack(pady=5)
    customer_money_entry = tk.Entry(purchase_window)
    customer_money_entry.pack(pady=5)

    tk.Button(purchase_window, text="Process Purchase", command=lambda: process_purchase(customer_name_entry.get(), customer_contact_entry.get(), customer_money_entry.get(), purchase_window)).pack(pady=20)

def process_purchase(customer_name, customer_contact, customer_money, purchase_window):
    try:
        customer_money = float(customer_money)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid amount for customer money.")
        return

    total_amount = sum(item['total_price'] for item in purchase_list)

    if customer_money < total_amount:
        messagebox.showerror("Insufficient Funds", "Customer money is less than the total amount.")
        return

    change = customer_money - total_amount
    update_inventory()
    print_receipt(customer_name, customer_contact, customer_money, change)
    messagebox.showinfo("Purchase Complete", f"Purchase successful!\nChange: Php {change:.2f}")
    purchase_list.clear()
    update_purchase_display()
    update_total_label()
    purchase_window.destroy()

def update_inventory():
    conn = connect_db()
    cursor = conn.cursor()

    for item in purchase_list:
        cursor.execute("SELECT Product_Quantity, Barcode FROM inventory WHERE Product_Name = ? AND Is_Void = 0 ORDER BY Date_Delivered ASC", (item['name'],))
        quantities = cursor.fetchall()

        remaining_quantity = item['quantity']
        for quantity, barcode in quantities:
            if remaining_quantity <= 0:
                break

            if quantity >= remaining_quantity:
                new_quantity = quantity - remaining_quantity
                cursor.execute("UPDATE inventory SET Product_Quantity = ? WHERE Barcode = ?", (new_quantity, barcode))
                remaining_quantity = 0
            else:
                remaining_quantity -= quantity
                cursor.execute("UPDATE inventory SET Product_Quantity = 0 WHERE Barcode = ?", (barcode,))

    conn.commit()
    conn.close()

def print_receipt(customer_name, customer_contact, customer_money, change):
    receipt_text = f"""
    Shop Name: Trimark Construction Supply
    Shop Address: [Insert Shop Address]
    Shop Contact Number: [Insert Shop Contact Number]
    Cashier: [Insert Cashier Name]
    Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    ---------------------------------------
    Customer Name: {customer_name}
    Customer Contact Number: {customer_contact}
    ---------------------------------------
    Items:
    """
    for item in purchase_list:
        receipt_text += f"{item['name']} x {item['quantity']} - Php {item['total_price']:.2f}\n"

    receipt_text += f"""
    ---------------------------------------
    Total: Php {sum(item['total_price'] for item in purchase_list):.2f}
    Bill Given: Php {customer_money:.2f}
    Change: Php {change:.2f}
    ---------------------------------------
    Thank you for your purchase!
    """

    # Print receipt (for demonstration purposes, we'll just print to console)
    print(receipt_text)

if __name__ == "__main__":
    create_pos_admin_window()
