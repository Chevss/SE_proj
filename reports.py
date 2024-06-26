import sqlite3
import tkinter as tk
import tkinter.font as tkfont
import win32print
import win32api
from tkinter import Button, Canvas, filedialog, messagebox, ttk
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph

current_data = None
sort_order = {}

conn = sqlite3.connect('Trimark_construction_supply.db')
cursor = conn.cursor()

def generate_user_logs():
    global current_data
    clear_tree()
    
    cursor.execute("SELECT log_id, Employee_ID, Username, action, timestamp FROM user_logs")
    rows = cursor.fetchall()

    current_data = rows
    update_tree(current_data, ["Log ID", "Employee ID", "Username", "Action", "Timestamp"])

def generate_purchase_history():
    global current_data
    clear_tree()
    
    cursor.execute("SELECT Purchase_ID, First_Name, Product_Name, Purchase_Quantity, Product_Price, Total_Price, Amount_Given, Change, Time_Stamp FROM purchase_history")
    rows = cursor.fetchall()

    current_data = rows
    update_tree(current_data, ["Purchase ID", "Customer Name", "Product", "Quantity", "Price", "Total Amount", "Amount Paid", "Change", "Timestamp"])

def generate_sales_report():
    global current_data
    clear_tree()
    
    current_data = ""
    update_tree(current_data, [""])

def update_tree(data, columns):
    clear_tree()
    tree["columns"] = columns

    window_width = 1082  # Width of the treeview in the window
    scrollbar_width = 20  # Approximate width of the scrollbar
    available_width = window_width - scrollbar_width
    column_width = available_width // len(columns)  # Calculate equal column width

    for col in columns:
        tree.heading(col, text=col, command=lambda _col=col: sort_column(_col))
        tree.column(col, width=column_width)  # Set each column to equal width
    
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

def save_current_tree_to_pdf():
    global current_data

    if not current_data:
        messagebox.showerror("Error", "No data available to print.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
    
    if not file_path:
        return  # User cancelled the file dialog

    # Create the PDF document
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    elements = []

    # Add title
    styles = getSampleStyleSheet()
    title = Paragraph("Report", styles['Title'])
    elements.append(title)

    # Create table data
    table_data = [tree["columns"]]  # Add column headers
    for row in current_data:
        table_data.append(list(row))

    # Create table
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)

    doc.build(elements) # Build the PDF

    messagebox.showinfo("Success", f"Data successfully saved to {file_path}")

def print_current_tree():
    global current_data

    if not current_data:
        messagebox.showerror("Error", "No data available to print.")
        return

    printer_name = win32print.GetDefaultPrinter()  # Get the default printer
    if not printer_name:
        messagebox.showerror("Error", "No default printer found.")
        return

    try:
        # Create the print job
        hPrinter = win32print.OpenPrinter(printer_name)
        hJob = win32print.StartDocPrinter(hPrinter, 1, ("Report", None, "RAW"))
        win32print.StartPagePrinter(hPrinter)

        # Print table data
        table_data = [tree["columns"]]  # Add column headers
        for row in current_data:
            table_data.append(list(row))

        row_height = 15
        x_start = 50
        y_start = 50
        line_height = 20
        for i, row in enumerate(table_data):
            for j, col in enumerate(row):
                win32print.TextOut(hPrinter, x_start + j * 120, y_start + i * line_height, str(col))

        win32print.EndPagePrinter(hPrinter)
        win32print.EndDocPrinter(hPrinter)
        win32print.ClosePrinter(hPrinter)

        messagebox.showinfo("Success", "Printing completed.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to print: {str(e)}")

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
    user_logs_btn.place(x=20, y=620, height=50, width=200)

    purchase_history_btn = Button(window, text="Purchase History", command=generate_purchase_history, font=("Hanuman Regular", 16), bg="#F8D48E", relief="raised")
    purchase_history_btn.place(x=320, y=620, height=50, width=200)

    sales_report_btn = Button(window, text="Sales Report", command=generate_sales_report, font=("Hanuman Regular", 16), bg="#F8D48E", relief="raised")
    sales_report_btn.place(x=620, y=620, height=50, width=200)

    back_btn = Button(window, text="Back", command=lambda: go_to_window("back"), font=("Hanuman Regular", 16), bg="#FFFFFF", relief="raised")
    back_btn.place(x=920, y=620, height=50, width=200)

    save_pdf_btn = Button(window, text="Save as PDF", command=save_current_tree_to_pdf, font=("Hanuman Regular", 16), bg="#FFFFFF", relief="raised")
    save_pdf_btn.place(x=620, y=20, height=50, width=200)

    print_btn = Button(window, text="Print", command=print_current_tree, font=("Hanuman Regular", 16), bg="#FFFFFF", relief="raised")
    print_btn.place(x=920, y=20, height=50, width=200)

    tree = ttk.Treeview(window, show='headings')
    # tree["columns"] = ("Log ID", "Employee ID", "Username", "Action", "Timestamp")
    # tree.heading("Log ID", text="Log ID")
    # tree.heading("Employee ID", text="Employee ID")
    # tree.heading("Username", text="Username")
    # tree.heading("Action", text="Action")
    # tree.heading("Timestamp", text="Timestamp")
    tree.place(x=20, y=90, height=480, width=1082)
    tree_scroll = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
    tree_scroll.place(x=1102, y=90, height=480)
    tree.configure(yscrollcommand=tree_scroll.set)

    # generate_user_logs() # default

    window.resizable(False, False)
    window.mainloop()

if __name__ == "__main__":
    create_reports_window()
