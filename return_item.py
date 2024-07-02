import sqlite3
from pathlib import Path
from tkinter import BooleanVar, Button, Canvas, Checkbutton, Entry, filedialog, messagebox, Tk
from tkinter import ttk

def go_to_window(windows):
    window.destroy()
    if windows == "Back":
        import pos_admin
        pos_admin.create_pos_admin_window()

def adjust_column_widths(event):
    treeview = event.widget
    total_width = treeview.winfo_width()
    column_width = total_width // len(treeview["columns"])
    for col in treeview["columns"]:
        treeview.column(col, width=column_width-1)

def create_return_item_window():
    global window, combobox, treeview
    window = Tk()
    window.title("Return Item")
    window.geometry("600x400")
    window.configure(bg="#FFE1C6")

    window_width, window_height = 600, 400
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    canvas = Canvas(window, bg="#DDD", height=400, width=600, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    canvas.create_rectangle(window_width, 0, 0, 55, fill="#000", outline="")
    canvas.create_text(240, 15, anchor="nw", text="Return Item", fill="#FFFFFF", font=("Hanuman Regular", 24 * -1))

    canvas.create_text(50, 70, anchor="nw", text="Purchase Details", fill="#000000", font=("Hanuman Regular", 16 * -1))
    purchased_products = get_purchased_products()
    combobox = ttk.Combobox(window, values=purchased_products)
    combobox.place(x=50, y=95, width=500, height=32)

    treeview = ttk.Treeview(window, columns=("Timestamp", "Quantity", "Product", "Price", "Condition"), show="headings")
    treeview.heading("Timestamp", text="Timestamp")
    treeview.heading("Quantity", text="Quantity")
    treeview.heading("Product", text="Product")
    treeview.heading("Price", text="Price")
    treeview.heading("Condition", text="Condition")
    treeview.place(x=50, y=135, width=500, height=150)
    treeview.bind("<Configure>", adjust_column_widths)

    return_item_button = Button(window, text="Normal Item", font=("Hanuman Regular", 12), bg="royalblue1", fg='#FFF', command=add_normal_item)
    return_item_button.place(x=50, y=295, width=100, height=32)

    broken_item_button = Button(window, text="Broken Item", font=("Hanuman Regular", 12), bg="royalblue1", fg='#FFF', command=add_broken_item)
    broken_item_button.place(x=160, y=295, width=100, height=32)

    process_button = Button(window, text="Process Return", font=("Hanuman Regular", 16), bg="royalblue4", fg='#FFF', command=process_return)
    process_button.place(x=50, y=350, width=210, height=32)

    delete_button = Button(window, text="Delete Selected", font=("Hanuman Regular", 12), bg="firebrick1", fg='#FFF', command=delete_selected_item)
    delete_button.place(x=340, y=295, width=125, height=32)

    clear_button = Button(window, text="Clear All", font=("Hanuman Regular", 12), bg="firebrick1", fg='#FFF', command=clear_treeview)
    clear_button.place(x=475, y=295, width=75, height=32)

    back_button = Button(window, text="Cancel Return", font=("Hanuman Regular", 16), bg="firebrick4", fg="#FFF", command=lambda:go_to_window("Back"))
    back_button.place(x=340, y=350, width=210, height=32)

    window.resizable(False, False)
    window.mainloop()

def get_purchased_products():
    conn = sqlite3.connect('Trimark_construction_supply.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT Purchase_ID, Time_Stamp, Purchase_Quantity, Product_Name, Product_Price 
        FROM purchase_history 
        WHERE NOT EXISTS (
            SELECT 1 FROM return_history 
            WHERE
                return_history.Purchase_ID = purchase_history.Purchase_ID
                AND
                return_history.Product_Name = purchase_history.Product_Name
        )
    ''')
    
    data = cursor.fetchall()

    conn.close()

    purchased_products = [f"{item[1]} | {item[2]} pc/s {item[3]} ({item[4]})" for item in data]
    return purchased_products

def select_this_product(condition):
    selected_product = combobox.get()
    if selected_product:
        # Split the selected product to extract individual fields
        timestamp, rest = selected_product.split(" | ")
        quantity, product_info = rest.split(" pc/s ")
        product_name, price = product_info.split(" (")
        price = price.rstrip(")")

        # Insert the selected product into the Treeview
        treeview.insert("", "end", values=(timestamp, quantity, product_name, price, condition))

def add_normal_item():
    select_this_product("Normal")

def add_broken_item():
    select_this_product("Broken")

def delete_selected_item():
    selected_item = treeview.selection()
    if selected_item:
        treeview.delete(selected_item)

def clear_treeview():
    for item in treeview.get_children():
        treeview.delete(item)

def get_barcode(product_name):
    conn = sqlite3.connect('Trimark_construction_supply.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Barcode FROM product WHERE Name = ?", (product_name,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def get_purchase_id(timestamp, product_name, quantity, price):
    conn = sqlite3.connect('Trimark_construction_supply.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT Purchase_ID
        FROM purchase_history
        WHERE Time_Stamp = ? AND Product_Name = ? AND Purchase_Quantity = ? AND Product_Price = ?
    ''', (timestamp, product_name, quantity, price))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def process_return():
    for item in treeview.get_children():
        values = treeview.item(item, "values")
        timestamp, quantity, product_name, price, condition = values
        barcode = get_barcode(product_name)
        purchase_id = get_purchase_id(timestamp, product_name, quantity, price)

        if condition == "Normal":
            update_inventory(barcode, int(quantity))
        elif condition == "Broken":
            add_to_broken_inventory(barcode, product_name, int(quantity), purchase_id)

        update_return_history(purchase_id, product_name, int(quantity), price)

    clear_treeview()

def update_return_history(purchase_id, product_name, returned_quantity, product_price):
    conn = sqlite3.connect('Trimark_construction_supply.db')
    cursor = conn.cursor()

    amount_given = float(returned_quantity) * float(product_price)

    cursor.execute('''
        INSERT INTO return_history (Purchase_ID, First_Name, Product_Name, Product_Price, Returned_Quantity, Time_Stamp, Amount_Given)
        SELECT Purchase_ID, First_Name, Product_Name, Product_Price, ?, CURRENT_TIMESTAMP, ?
        FROM purchase_history
        WHERE Purchase_ID = ? AND Product_Name = ?
    ''', (returned_quantity, amount_given, purchase_id, product_name))

    conn.commit()
    conn.close()

def update_inventory(barcode, quantity):
    conn = sqlite3.connect('Trimark_construction_supply.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE inventory SET Quantity = Quantity + ? WHERE Barcode = ?", (quantity, barcode))
    conn.commit()
    conn.close()

def add_to_broken_inventory(barcode, product_name, quantity, purchase_id):
    conn = sqlite3.connect('Trimark_construction_supply.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO broken_inventory (Barcode, Product_Name, Quantity, DateBroken, Original_Purchase_ID)
        VALUES (?, ?, ?, DATE('now'), ?)
    ''', (barcode, product_name, quantity, purchase_id))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_return_item_window()