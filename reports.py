import tkinter as tk
from tkinter import Button, Canvas, ttk

current_tree = None # For printing

# TEMPORARY DATA
def generate_user_logs():
    clear_tree()
    tree["columns"] = ("ID", "Username", "Action", "Timestamp")
    tree.heading("ID", text="ID")
    tree.heading("Username", text="Username")
    tree.heading("Action", text="Action")
    tree.heading("Timestamp", text="Timestamp")
    
    # Dummy data for user logs
    data = [
        (1, "user1", "login", "2024-06-26 08:00"),
        (2, "user2", "logout", "2024-06-26 09:00"),
        (3, "user3", "login", "2024-06-26 10:00"),
    ]
    
    for record in data:
        tree.insert("", tk.END, values=record)

def generate_purchase_history():
    clear_tree()
    tree["columns"] = ("OrderID", "Product", "Quantity", "Date")
    tree.heading("OrderID", text="OrderID")
    tree.heading("Product", text="Product")
    tree.heading("Quantity", text="Quantity")
    tree.heading("Date", text="Date")
    
    # Dummy data for purchase history
    data = [
        (101, "Laptop", 1, "2024-06-20"),
        (102, "Mouse", 2, "2024-06-21"),
        (103, "Keyboard", 1, "2024-06-22"),
    ]
    
    for record in data:
        tree.insert("", tk.END, values=record)

def generate_sales_report():
    clear_tree()
    tree["columns"] = ("SaleID", "Product", "Amount", "Date")
    tree.heading("SaleID", text="SaleID")
    tree.heading("Product", text="Product")
    tree.heading("Amount", text="Amount")
    tree.heading("Date", text="Date")
    
    # Dummy data for sales report
    data = [
        (201, "Laptop", "$1200", "2024-06-18"),
        (202, "Monitor", "$300", "2024-06-19"),
        (203, "Printer", "$150", "2024-06-20"),
    ]
    
    for record in data:
        tree.insert("", tk.END, values=record)

# Clear tree
def clear_tree():
    for item in tree.get_children():
        tree.delete(item)

def create_reports_window():
    global window, tree

    window = tk.Tk()
    window.title("Reports")
    window.geometry("1140x720")
    window.configure(bg="#FFE1C6")

    window_width, window_height = 1140, 720
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    canvas = Canvas(window, bg="#FFE1C6", height=800, width=1280, bd=0, highlightthickness=0, relief="ridge")
    canvas.pack()




    user_logs_btn = Button(window, text="User Logs", command=generate_user_logs, font=("Hanuman Regular", 16), bg="#F8D48E", relief="raised")
    user_logs_btn.place(x=20, y=20, height=50, width=200)

    purchase_history_btn = Button(window, text="Purchase History", command=generate_purchase_history, font=("Hanuman Regular", 16), bg="#F8D48E", relief="raised")
    purchase_history_btn.place(x=320, y=20, height=50, width=200)

    sales_report_btn = Button(window, text="Sales Report", command=generate_sales_report, font=("Hanuman Regular", 16), bg="#F8D48E", relief="raised")
    sales_report_btn.place(x=620, y=20, height=50, width=200)

    print_btn = Button(window, text="Print", command=None, font=("Hanuman Regular", 16), bg="#FFFFFF", relief="raised")
    print_btn.place(x=920, y=20, height=50, width=200)


    # Create the tree view
    tree = ttk.Treeview(window)
    tree["columns"] = ("ID", "Username", "Action", "Timestamp")
    tree.heading("#0", text="Index")
    tree.heading("ID", text="ID")
    tree.heading("Username", text="Username")
    tree.heading("Action", text="Action")
    tree.heading("Timestamp", text="Timestamp")
    tree.place(x=20, y=90, height=480, width=1100)






    window.resizable(False, False)
    window.mainloop()

if __name__ == "__main__":
    create_reports_window()