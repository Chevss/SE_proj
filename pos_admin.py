import hashlib
import secrets
import sqlite3
import tkinter as tk
from pathlib import Path
from tkinter import Button, Canvas, Entry, Label, messagebox, PhotoImage, simpledialog, ttk

import shared_state
from new_pass import is_valid_password
from registration import is_valid_contact_number, is_valid_email, is_valid_name
from user_logs import log_actions

# Define the path to your assets folder
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\Pos Admin")

# Initialize an empty list to store purchased items
purchase_list = []

def relative_to_assets(path: str) -> Path:
    """Returns the absolute path to an asset relative to ASSETS_PATH."""
    return ASSETS_PATH / Path(path)

def generate_salt():
    return secrets.token_hex(16)

def hash_password(password, salt):
    return hashlib.sha256((password + salt).encode()).hexdigest()

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
        log_actions(shared_state.current_user, "Logged Out")
        shared_state.current_user = None
        import login
        login.create_login_window()
    elif window_type == "inventory":
        import inventory_admin
        inventory_admin.create_inventory_window()
    elif window_type == "register":
        import registration
        registration.create_registration_window()

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
                    valid = is_valid_contact_number(new_phone_number)
                    if valid:
                        update_phone_number(employee_id, new_phone_number)
                    else:
                        messagebox.showerror("Error", "Invalid contact number format")
        else:
            messagebox.showerror("Error", "No user logged in")

    # Hamburger menu icon
    hamburger_icon = PhotoImage(file=relative_to_assets("hamburger.png"))
    hamburger_icon_resized = hamburger_icon.subsample(6, 6)
    hamburger_button = Button(window, image=hamburger_icon_resized, borderwidth=0, highlightthickness=0, command=show_hamburger_menu, relief="flat")
    hamburger_button.image = hamburger_icon  # Keep a reference to the image to prevent garbage collection
    hamburger_button.place(x=110, y=15)

    window.resizable(False, False)
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

def update_first_name(employee_id, new_first_name):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE accounts SET First_Name = ? WHERE Employee_ID = ?", (new_first_name, employee_id))
        conn.commit()
        messagebox.showinfo("Success", "First Name updated successfully")
    except sqlite3.Error as e:
        conn.rollback()
        messagebox.showerror("Error", f"Error updating First Name: {e}")
    finally:
        conn.close()

def update_last_name(employee_id, new_last_name):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE accounts SET Last_Name = ? WHERE Employee_ID = ?", (new_last_name, employee_id))
        conn.commit()
        messagebox.showinfo("Success", "Last Name updated successfully")
    except sqlite3.Error as e:
        conn.rollback()
        messagebox.showerror("Error", f"Error updating Last Name: {e}")
    finally:
        conn.close()

def update_password(employee_id, new_password, salt):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE accounts SET Password = ?, Salt = ? WHERE Employee_ID = ?", (new_password, salt, employee_id))
        conn.commit()
        messagebox.showinfo("Success", "Password updated successfully")
    except sqlite3.Error as e:
        conn.rollback()
        messagebox.showerror("Error", f"Error updating Password: {e}")
    finally:
        conn.close()

def update_email(employee_id, new_email):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE accounts SET Email = ? WHERE Employee_ID = ?", (new_email, employee_id))
        conn.commit()
        messagebox.showinfo("Success", "Email updated successfully")
    except sqlite3.Error as e:
        conn.rollback()
        messagebox.showerror("Error", f"Error updating Email: {e}")
    finally:
        conn.close()

def update_phone_number(employee_id, new_phone_number):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE accounts SET Contact_No = ? WHERE Employee_ID = ?", (new_phone_number, employee_id))
        conn.commit()
        messagebox.showinfo("Success", "Phone Number updated successfully")
    except sqlite3.Error as e:
        conn.rollback()
        messagebox.showerror("Error", f"Error updating Phone Number: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    create_pos_admin_window()
