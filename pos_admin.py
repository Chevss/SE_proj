from pathlib import Path
import tkinter as tk
from tkinter import ttk, Canvas, Entry, Button, PhotoImage, Label, messagebox
import sqlite3

# Define the path to your assets folder
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\Pos Admin")

# Initialize an empty list to store purchased items
purchase_list = []

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

    cursor.execute("SELECT Product_Name, Product_Quantity, Product_Price FROM inventory WHERE Barcode = ?", (barcode,))
    result = cursor.fetchone()

    conn.close()
    return result

def on_barcode_entry(event):
    """Handles the event when a barcode is entered."""
    barcode_value = barcode.get()
    result = search_barcode(barcode_value)

    if result:
        product_name, product_quantity, product_price = result
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
        import login
        login.create_login_window()
    elif window_type == "inventory":
        import inventory_admin
        inventory_admin.create_inventory_window()
    elif window_type == "register":
        import registration
        registration.create_registration_window()

def create_pos_admin_window():
    """Creates and configures the POS admin window."""
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

    # Barcode entry widget
    global barcode
    barcode = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=1,
        font=("Hanuman Regular", 28 * -1)
    )
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

    purchase_button = Button(
        text="Purchase",
        font=("Hanuman Regular", 20),
        command=lambda: print("Purchase Button"),
        bg="#83F881",
        relief="raised"
    )
    purchase_button.place(x=42.0, y=623.0, width=464.28277587890625, height=112.0)

    inventory_button = Button(
        text="Inventory",
        font=("Hanuman Regular", 20),
        command=lambda: go_to_window("inventory"),
        bg="#81CDF8",
        relief="ridge"
    )
    inventory_button.place(x=699.0, y=623.0, width=170.28277587890625, height=112.0)

    register_button = Button(
        text="Register\nAccount",
        font=("Hanuman Regular", 20),
        command=lambda: go_to_window("register"),
        bg="#81CDF8",
        relief="ridge"
    )
    register_button.place(x=699.0, y=477.0, width=170.28277587890625, height=112.0)

    reports_button = Button(
        text="Reports",
        font=("Hanuman Regular", 20),
        command=lambda: print("Reports Button"),
        bg="#81CDF8",
        relief="ridge"
    )
    reports_button.place(x=884.0, y=623.0, width=170.28277587890625, height=112.0)

    maintenance_button = Button(
        text="Maintenance",
        font=("Hanuman Regular", 20),
        command=lambda: print("Maintenance Button"),
        bg="#81CDF8",
        relief="ridge"
    )
    maintenance_button.place(x=1068.0, y=477.0, width=170.28277587890625, height=112.0)

    void_button = Button(
        text="Void",
        font=("Hanuman Regular", 20),
        command=lambda: print("Void"),
        bg="#FF9E9E",
        relief="raised"
    )
    void_button.place(x=506.0, y=623.0, width=166.0, height=112.0)

    # Draw shapes and texts on canvas
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

if __name__ == "__main__":
    create_pos_admin_window()
