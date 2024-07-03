import sqlite3
import tkinter as tk
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Frame, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from tkinter import Button, Canvas, filedialog, messagebox, ttk
from tkcalendar import DateEntry

import shared_state

# From user made module
current_data = None
sort_order = {}

company = "Tri-Mark Construction Supply"
address = "39 Scout Ybardolaza, Diliman, Quezon City, 1103 Metro Manila"
phone = "(02) 8928 5744"
report_type = ""

conn = sqlite3.connect('Trimark_construction_supply.db')
cursor = conn.cursor()

def generate_user_logs():
    global current_data, report_type
    report_type = "User Logs Report"
    update_report_type_label()
    clear_tree()
    
    from_date = from_date_entry.get_date().strftime("%Y-%m-%d")
    to_date = to_date_entry.get_date().strftime("%Y-%m-%d")
    
    cursor.execute("""
        SELECT log_id, Employee_ID, Username, action, timestamp 
        FROM user_logs 
        WHERE date(timestamp) BETWEEN ? AND ?
    """, (from_date, to_date))
    
    rows = cursor.fetchall()

    current_data = rows
    update_tree(current_data, ["Log ID", "Employee ID", "Username", "Action", "Timestamp"])

def generate_purchase_history():
    global current_data, report_type
    report_type = "Purchase History Report"
    update_report_type_label()
    clear_tree()
    
    from_date = from_date_entry.get_date().strftime("%Y-%m-%d")
    to_date = to_date_entry.get_date().strftime("%Y-%m-%d")
    
    query = """
        SELECT 
            Purchase_ID, 
            First_Name, 
            GROUP_CONCAT(Product_Name, '\n') as Products,
            GROUP_CONCAT(Purchase_Quantity, '\n') as Quantities, 
            GROUP_CONCAT(Product_Price, '\n') as Prices, 
            SUM(Total_Price) as Total_Price, 
            Amount_Given, 
            `Change`, 
            Time_Stamp
        FROM 
            purchase_history 
        WHERE date(Time_Stamp) BETWEEN ? AND ?
        GROUP BY 
            Purchase_ID, First_Name, Amount_Given, `Change`, Time_Stamp
    """
    
    cursor.execute(query, (from_date, to_date))
    rows = cursor.fetchall()

    formatted_rows = []
    for row in rows:
        formatted_row = list(row)
        formatted_row[4] = "\n".join([f"{float(price):.2f}" for price in formatted_row[4].split('\n')])
        formatted_row[5] = f"{float(formatted_row[5]):.2f}"
        formatted_row[6] = f"{float(formatted_row[6]):.2f}"
        formatted_row[7] = f"{float(formatted_row[7]):.2f}"
        formatted_rows.append(tuple(formatted_row))

    current_data = formatted_rows
    update_tree(current_data, ["Purchase ID", "Customer Name", "Products", "Quantities", "Prices", "Total Amount", "Amount Paid", "Change", "Timestamp"])

def generate_return_history():
    global current_data, report_type
    report_type = "Return History Report"
    update_report_type_label()
    clear_tree()

    from_date = from_date_entry.get_date().strftime("%Y-%m-%d")
    to_date = to_date_entry.get_date().strftime("%Y-%m-%d")

    query = """
        SELECT
            Purchase_ID,
            First_Name,
            GROUP_CONCAT(Product_Name, '\n') as Products,
            GROUP_CONCAT(Product_Price, '\n') as Prices,
            GROUP_CONCAT(Returned_Quantity, '\n') as Returned_Quantities,
            Time_Stamp,
            Amount_Given,
            Condition
        FROM
            return_history
        WHERE date(Time_Stamp) BETWEEN ? AND ?
        GROUP BY 
            Purchase_ID, First_Name, Time_Stamp
    """
    
    cursor.execute(query, (from_date, to_date))
    rows = cursor.fetchall()

    formatted_rows = []
    for row in rows:
        formatted_row = list(row)
        formatted_row[3] = "\n".join([f"{float(price):.2f}" for price in formatted_row[3].split('\n')])
        formatted_row[4] = "\n".join([quantity for quantity in formatted_row[4].split('\n')])
        formatted_row[6] = f"{float(formatted_row[6]):.2f}"
        formatted_rows.append(tuple(formatted_row))

    current_data = formatted_rows
    update_tree(current_data, ["Return ID", "Customer Name", "Products", "Prices", "Returned Quantities", "Timestamp", "Amount Given", "Condition"])

def generate_sales_report():
    global current_data, report_type
    report_type = "Sales Report"
    update_report_type_label()
    clear_tree()

    from_date = from_date_entry.get_date().strftime("%Y-%m-%d")
    to_date = to_date_entry.get_date().strftime("%Y-%m-%d")

    query = """
        SELECT
            p.Product_Name,
            ROUND(SUM(p.Purchase_Quantity - COALESCE(r.Returned_Quantity, 0)), 2) AS Total_Quantity_Sold,
            ROUND(SUM(p.Total_Price - COALESCE(r.Returned_Quantity*r.Product_Price, 0)), 2) AS Total_Sales
        FROM
            purchase_history p
        LEFT JOIN
            return_history r ON p.Purchase_ID = r.Purchase_ID AND p.Product_Name = r.Product_Name
        WHERE
            date(p.Time_Stamp) BETWEEN ? AND ?
        GROUP BY
            p.Product_Name
    """
    
    cursor.execute(query, (from_date, to_date))
    rows = cursor.fetchall()
    overall_total_sales = sum(row[2] for row in rows)
    
    overall_total_row = ("Overall Total", "", f"{overall_total_sales:.2f}")
    formatted_rows = [(row[0], row[1], f"{row[2]:.2f}") for row in rows]
    formatted_rows.append(overall_total_row)

    current_data = formatted_rows  # Use fetched data from the database
    update_tree(current_data, ["Product Name", "Total Quantity Sold", "Total Sales"])

def generate_void_transac():
    global current_data, report_type
    report_type = "Void Transactions Report"
    update_report_type_label()
    clear_tree()
    from shared_state import void_list
    # Prepare data for the report
    rows = []
    for void_item in void_list:
        product_name = void_item.get('name', '')  # Ensure 'Void_ID' matches the key in your dictionary
        void_quantity = void_item.get('quantity', '')  # Ensure 'Product_Name' matches the key in your dictionary
        price = void_item.get('price', '')  # Ensure 'Void_Quantity' matches the key in your dictionary
        total_price = void_item.get('total_price', '')
        timestamp = void_item.get('timestamp', '')  # Ensure 'timestamp' matches the key in your dictionary

        rows.append((product_name, void_quantity, price, total_price, timestamp))

    # Print for debugging purposes
    print("Rows:", rows)

    current_data = rows
    update_tree(current_data, ["Product Name", "Quantity", "Price", "Total_Price", "Timestamp"])


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

def update_report_type_label():
    global report_type_label, report_type
    if report_type_label:
        report_type_label.config(text=f"Currently Showing: {report_type}")

# FOR SELECTING DATES
def regenerate_current_report(*args):
    if report_type == "User Logs Report":
        generate_user_logs()
    elif report_type == "Purchase History Report":
        generate_purchase_history()
    elif report_type == "Return History Report":
        generate_return_history()
    elif report_type == "Sales Report":
        generate_sales_report()
    elif report_type == "Void Transactions Report":
        generate_void_transac()

def save_current_tree_to_pdf():
    global current_data

    if not current_data:
        messagebox.showerror("Error", "No data available to print.")
        return

    from_date = from_date_entry.get_date().strftime("%Y-%m-%d")
    to_date = to_date_entry.get_date().strftime("%Y-%m-%d")
    now = datetime.now()
    date_time_str = now.strftime("%Y-%m-%d-%H%M%S")
    filename = f"{report_type.replace(' ', '_')}_{from_date}_to_{to_date}_{date_time_str}.pdf"
    
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile=filename, filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
    
    if not file_path:
        return  # User cancelled the file dialog

    # Create the PDF document
    doc = SimpleDocTemplate(file_path, pagesize=landscape(letter))
    elements = []

    # Add title
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    normal_style = styles['Normal']
    centered_style = styles['Normal']
    centered_style.alignment = 1  # Center alignment

    company_details = Paragraph(f"<b>{company}</b>", centered_style)
    address_details = Paragraph(f"{address}", centered_style)
    phone_details = Paragraph(f"{phone}", centered_style)
    report_title = Paragraph(f"<b>{report_type}</b>", title_style)

    elements.append(company_details)
    elements.append(Spacer(1, 6))
    elements.append(address_details)
    elements.append(Spacer(1, 6))
    elements.append(phone_details)
    elements.append(Spacer(1, 24))  # Add space
    elements.append(report_title)
    elements.append(Spacer(1, 24))  # Add space

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
    
    # Add generation details at the bottom
    now = datetime.now()
    date_time_str = now.strftime("%Y-%m-%d at %H:%M:%S")
    username = shared_state.current_user
    generation_details = Paragraph(f"Generated by {username} on {date_time_str}", centered_style)
    
    def draw_footer(canvas, doc):
        canvas.saveState()
        footer_frame = Frame(doc.leftMargin, doc.bottomMargin - 50, doc.width, 50, id='footer')
        footer_frame.addFromList([generation_details], canvas)
        canvas.restoreState()

    doc.build(elements, onFirstPage=draw_footer, onLaterPages=draw_footer) # Build the PDF

    messagebox.showinfo("Success", f"Data successfully saved to {file_path}")

def go_to_window(windows):
    window.destroy()
    if windows == "back":
        import pos_admin
        pos_admin.create_pos_admin_window()

def create_reports_window():
    global window, tree, from_date_entry, to_date_entry, report_type_label

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

    from_date_label = tk.Label(window, text="From Date:", font=("Hanuman Regular", 12), bg="#FFE1C6")
    from_date_label.place(x=20, y=20)
    from_date_entry = DateEntry(window, font=("Hanuman Regular", 12), width=8, background='darkblue', foreground='white', borderwidth=2)
    from_date_entry.place(x=105, y=20)

    to_date_label = tk.Label(window, text="To Date:", font=("Hanuman Regular", 12), bg="#FFE1C6")
    to_date_label.place(x=220, y=20)
    to_date_entry = DateEntry(window, font=("Hanuman Regular", 12), width=8, background='darkblue', foreground='white', borderwidth=2)
    to_date_entry.place(x=285, y=20)

    from_date_entry.bind("<<DateEntrySelected>>", regenerate_current_report)
    to_date_entry.bind("<<DateEntrySelected>>", regenerate_current_report)

    report_type_label = tk.Label(window, text=f"Currently Showing: None", font=("Hanuman Regular", 12), bg="#FFE1C6")
    report_type_label.place(x=20, y=60)

    user_logs_btn = Button(window, text="User Logs", command=generate_user_logs, font=("Hanuman Regular", 16), bg="#F8D48E", relief="raised")
    user_logs_btn.place(x=20, y=585, height=50, width=200)

    purchase_history_btn = Button(window, text="Purchase History", command=generate_purchase_history, font=("Hanuman Regular", 16), bg="#F8D48E", relief="raised")
    purchase_history_btn.place(x=20, y=645, height=50, width=200)

    return_history_btn = Button(window, text="Return History", command=generate_return_history, font=("Hanuman Regular", 16), bg="#F8D48E", relief="raised")
    return_history_btn.place(x=240, y=645, height=50, width=200)

    sales_report_btn = Button(window, text="Sales Report", command=generate_sales_report, font=("Hanuman Regular", 16), bg="#F8D48E", relief="raised")
    sales_report_btn.place(x=460, y=585, height=50, width=200)

    void_transac_btn = Button(window, text="Void Transac", command=generate_void_transac, font=("Hanuman Regular", 16), bg="#F8D48E", relief="raised")
    void_transac_btn.place(x=240, y=585, height=50, width=200)

    back_btn = Button(window, text="Back", command=lambda: go_to_window("back"), font=("Hanuman Regular", 16), bg="#FFFFFF", relief="raised")
    back_btn.place(x=920, y=645, height=50, width=200)

    save_pdf_btn = Button(window, text="Save as PDF", command=save_current_tree_to_pdf, font=("Hanuman Regular", 16), bg="#FFFFFF", relief="raised")
    save_pdf_btn.place(x=920, y=20, height=50, width=200)

    tree = ttk.Treeview(window, show='headings')
    tree.place(x=20, y=90, height=480, width=1082)
    tree_scroll = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
    tree_scroll.place(x=1102, y=90, height=480)
    tree.configure(yscrollcommand=tree_scroll.set)
    ttk.Style().configure('Treeview', rowheight=25)

    window.resizable(False, False)
    window.mainloop()

if __name__ == "__main__":
    create_reports_window()
    
