import tkinter as tk
from tkinter import Button, Canvas, ttk

current_tree = None # For printing
sort_order = {}

# TEMPORARY DATA
def generate_user_logs():
    global current_data
    clear_tree()
    
    # Dummy data for user logs
    current_data = [
        (1, "user1", "login", "2024-06-26 08:00"),
        (2, "user4", "logout", "2024-06-26 09:00"),
        (3, "user3", "login", "2024-06-26 10:00"),
        (4, "user2", "changed password", "2024-06-26 12:00"),
    ]
    update_tree(current_data, ["ID", "Username", "Action", "Timestamp"])

def generate_purchase_history():
    global current_data
    clear_tree()
    
    # Dummy data for purchase history
    current_data = [
        (101, "Laptop", 1, "2024-06-20"),
        (102, "Mouse", 2, "2024-06-21"),
        (103, "Keyboard", 1, "2024-06-22"),
        (104, "Apple", 3, "2024-06-23"),
    ]
    update_tree(current_data, ["OrderID", "Product", "Quantity", "Date"])

def generate_sales_report():
    global current_data
    clear_tree()
    
    # Dummy data for sales report
    current_data = [
        (201, "Laptop", "$1200", "2024-06-18"),
        (202, "Monitor", "$300", "2024-06-19"),
        (203, "Printer", "$150", "2024-06-20"),
        (204, "Apple", "$1050", "2024-06-21"),
    ]
    update_tree(current_data, ["SaleID", "Product", "Amount", "Date"])

def update_tree(data, columns):
    clear_tree()
    tree["columns"] = columns
    for col in columns:
        tree.heading(col, text=col, command=lambda _col=col: sort_column(_col))
    for record in data:
        tree.insert("", tk.END, values=record)

def clear_tree():
    for item in tree.get_children():
        tree.delete(item)

def sort_column(col):
    global current_data
    if col not in sort_order:
        sort_order[col] = False  # Initialize sorting order as ascending
    
    sort_order[col] = not sort_order[col]  # Toggle sorting order
    current_data.sort(key=lambda x: x[tree["columns"].index(col)], reverse=sort_order[col])
    update_tree(current_data, tree["columns"])

def go_to_window(windows):
    window.destroy()
    if windows == "back":
        import pos_admin
        pos_admin.create_pos_admin_window()

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
    canvas.place(x=0, y=0)

    user_logs_btn = Button(window, text="User Logs", command=generate_user_logs, font=("Hanuman Regular", 16), bg="#F8D48E", relief="raised")
    user_logs_btn.place(x=20, y=20, height=50, width=200)

    purchase_history_btn = Button(window, text="Purchase History", command=generate_purchase_history, font=("Hanuman Regular", 16), bg="#F8D48E", relief="raised")
    purchase_history_btn.place(x=320, y=20, height=50, width=200)

    sales_report_btn = Button(window, text="Sales Report", command=generate_sales_report, font=("Hanuman Regular", 16), bg="#F8D48E", relief="raised")
    sales_report_btn.place(x=620, y=20, height=50, width=200)

    print_btn = Button(window, text="Print", command=None, font=("Hanuman Regular", 16), bg="#FFFFFF", relief="raised")
    print_btn.place(x=920, y=20, height=50, width=200)

    back_btn = Button(window, text="Back", command=lambda: go_to_window("back"), font=("Hanuman Regular", 16), bg="#FFFFFF", relief="raised")
    back_btn.place(x=920, y=620, height=50, width=200)

    tree = ttk.Treeview(window)
    tree["columns"] = ("ID", "Username", "Action", "Timestamp")
    tree.heading("#0", text="Index")
    tree.heading("ID", text="ID")
    tree.heading("Username", text="Username")
    tree.heading("Action", text="Action")
    tree.heading("Timestamp", text="Timestamp")
    tree.place(x=20, y=90, height=480, width=1082)
    tree_scroll = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
    tree_scroll.place(x=1102, y=90, height=480)
    tree.configure(yscrollcommand=tree_scroll.set)

    window.resizable(False, False)
    window.mainloop()

if __name__ == "__main__":
    create_reports_window()
