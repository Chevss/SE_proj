from tkinter import Tk, Canvas, Entry, Button, Label, StringVar, Scrollbar
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from pathlib import Path
import sqlite3
from barcode import Code39
from barcode.writer import ImageWriter
import shared_state

# Define paths
OUTPUT_PATH = Path(__file__).parent
BARCODES_PATH = OUTPUT_PATH / Path("Barcodes")

# Ensure the "Barcodes" folder exists, create if not
BARCODES_PATH.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect('Trimark_construction_supply.db')
cursor = conn.cursor()

def generate_code39_barcode(barcode_data, product_name):
    # Generate Code 39 barcode
    code39 = Code39(barcode_data, writer=ImageWriter(), add_checksum=False)
    barcode_image = code39.render()  # Render barcode as PIL Image
    return barcode_image

def go_to_window(windows):
    window.destroy()
    if windows == "back":
        import pos_admin
        pos_admin.create_pos_admin_window()

def on_select(event):
    # Function to handle tree item selection
    if tree.selection():  # Check if there is any selection
        item = tree.selection()[0]
        values = tree.item(item, 'values')
        selected_barcode_var.set(values[1])  # Display selected barcode in entry
        display_barcode_image(values[1], values[0])  # Display selected barcode image with product name

def display_barcode_image(barcode_data, product_name):
    # Ensure the barcode data does not have extra characters
    barcode_data = barcode_data.strip()
    print(f"Generating barcode for data: '{barcode_data}' and product name: '{product_name}'")
    
    # Generate Code 39 barcode image
    barcode_image = generate_code39_barcode(barcode_data, product_name)

    # Resize the barcode image if necessary
    size = (200, 100)
    barcode_image = barcode_image.resize(size)  # Resize without specifying any resampling filter

    # Convert Image object to Tkinter PhotoImage
    barcode_photo = ImageTk.PhotoImage(barcode_image)

    # Display the image on a label (assuming barcode_label is defined globally)
    barcode_label.config(image=barcode_photo)
    barcode_label.image = barcode_photo  # Keep a reference to avoid garbage collection

    barcode_label.place(x=200, y=730)

def save_barcode_image():
    # Function to save the displayed barcode image
    if selected_barcode_var.get():
        barcode_data = selected_barcode_var.get()
        product_name = tree.item(tree.selection()[0], 'values')[0]  # Get product name from selected item in Treeview

        # Generate the barcode image
        barcode_image = generate_code39_barcode(barcode_data, product_name)

        # Determine the file path with a valid image extension (e.g., .png) in the "Barcodes" folder
        barcode_image_path = BARCODES_PATH / f"{product_name}.png"

        # Save the barcode image to disk
        barcode_image.save(barcode_image_path, format="PNG")

        # Optionally provide feedback to the user that the image has been saved
        print(f"Barcode image for {product_name} saved in 'Barcodes' folder.")

def search_database():
    # Placeholder for search functionality
    query = search_entry.get().strip().lower()
    results = linear_search(query)
    
    # Clear existing items in tree view
    for item in tree.get_children():
        tree.delete(item)
    
    # Populate tree view with search results
    for i, (name, barcode) in enumerate(results, start=1):
        tree.insert('', 'end', values=(name, barcode))  # Inserting into treeview

def linear_search(query):
    # Placeholder for search functionality in SQLite
    cursor.execute("SELECT Name, Barcode FROM product WHERE LOWER(Name) LIKE ?", ('%' + query.lower() + '%',))
    results = cursor.fetchall()
    return results

def fetch_all_products():
    # Fetch all products from the database
    cursor.execute("SELECT Name, Barcode FROM product")
    return cursor.fetchall()

def update_table():
    # Clear existing items in tree view
    for item in tree.get_children():
        tree.delete(item)
    
    # Fetch all products from the database and populate the Treeview
    products = fetch_all_products()
    for product in products:
        tree.insert('', 'end', values=product)

def create_barcode_window():
    global window
    window = Tk()
    window.geometry("736x900")
    window.configure(bg="#FFE1C6")
    window.title("Barcodes")
    
    # Center the window on the screen
    window_width, window_height = 736, 900
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    canvas = Canvas(
        window,
        bg="#FFE1C6",
        height=924,
        width=736,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    canvas.create_rectangle(
        246.0,
        28.0,
        489.0,
        100.0,
        fill="#5CB0FF",
        outline=""
    )

    canvas.create_text(
        293.0,
        40.0,
        anchor="nw",
        text="Barcode",
        fill="#000000",
        font=("Hanuman Regular", 40 * -1)
    )

    back_button = Button(
        text="Back",
        font=("Hanuman Regular", 20),
        command=lambda: go_to_window("back"),
        bg="#FFFFFF",
        relief="raised"
    )
    back_button.place(x=600.0, y=813.0)

    search_button = Button(
        text="Search",
        font=("Hanuman Regular", 12),
        command=search_database,
        bg="#FFFFFF",
        relief="raised"
    )
    search_button.place(x=500.0, y=120.0)

    global search_entry
    search_entry = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=1,
        font=("Hanuman Regular", 19 * -1)
    )
    search_entry.place(x=152.0, y=122.0, width=332.0, height=30.0)


    global selected_barcode_var
    selected_barcode_var = StringVar()

    global barcode_label
    barcode_label = Label(window, bg="#FFFFFF")
    barcode_label.place(x=100, y=780)

    global tree
    tree = ttk.Treeview(window, columns=('Name', 'Barcode'), show='headings')
    tree.heading('Name', text='Name')
    tree.heading('Barcode', text='Barcode')
    tree.place(x=50, y=165, width=635, height=535)  # Adjust width and height to fit the rectangle

    tree.bind('<ButtonRelease-1>', on_select)  # Bind selection event

    vsb = Scrollbar(window, orient="vertical", command=tree.yview)
    vsb.place(x=685, y=165, height=535)
    tree.configure(yscrollcommand=vsb.set)

    save_button = Button(
        text="Save",
        font=("Hanuman Regular", 12),
        command=save_barcode_image,  # Call save function
        bg="#FFFFFF",
        relief="raised"
    )
    save_button.place(x=480.0, y=770.0)



    # Initialize the table with all products upon window creation
    update_table()

    window.resizable(False, False)
    window.mainloop()

if __name__ == "__main__":
    create_barcode_window()

