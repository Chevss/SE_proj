import json
from tkinter import Tk, Canvas, Text, Button, Toplevel, END, messagebox, Label, Entry
from portalocker import lock, unlock, LOCK_EX

import shared_state
# Load or initialize the FAQ data
FAQ_FILE = 'faqs.json'

# Default FAQs
default_faqs = [
    {"question": "What is the primary purpose of the product management system?", "answer": "The system aims to automate and improve the efficiency of daily transactions, inventory management, and record-keeping at Tri-Mark Construction Supply using barcode technology."},
    {"question": "How will the barcode technology be implemented in the system?", "answer": "Barcode technology will be used to encode product information, which can be scanned for quick and accurate data collection during transactions and inventory checks."},
    {"question": "What are the main modules included in the product management system?", "answer": "The system includes a POS module, Barcode module, Security module, Records Database module, Reports module, Inventory module, Search module, Maintenance module, Help module, and About module."},
    {"question": "How does the POS module function?", "answer": "The POS module handles all store transactions, including scanning barcodes, calculating total prices, processing payments, and printing receipts."},
    {"question": "What security measures are in place to protect data within the system?", "answer": "The system includes a security module that manages user authentication and access levels, ensuring only authorized personnel can access sensitive data."},
    {"question": "How does the system handle inventory management?", "answer": "The inventory module tracks all products and their quantities, updates stock levels after transactions, and generates reports on inventory status."},
    {"question": "Can new employees easily learn to use the system?", "answer": "Yes, the system features an easy-to-use interface with labeled buttons and a help module containing FAQs and a user manual to minimize the need for extensive training."},
    {"question": "What should I do if I encounter an issue with the system?", "answer": "The Maintenance module provides information on system issues and updates. Users can also refer to the Help module or contact support for assistance."},
    {"question": "How does the system improve record-keeping and reporting?", "answer": "The Records Database module stores all transaction data securely, allowing for accurate record-keeping. The Reports module can generate various reports based on stored data."},
    {"question": "Is the system accessible online?", "answer": "No, the system is LAN-based and designed for use within Tri-Mark Construction Supply's local network, enhancing security and reliability."}
]

try:
    with open(FAQ_FILE, 'r') as file:
        faqs = json.load(file)
except FileNotFoundError:
    faqs = default_faqs

# Ensure faqs is a list
if not isinstance(faqs, list):
    faqs = default_faqs

# Function to save the FAQs to a JSON file with restricted permissions
def save_faqs():
    with open(FAQ_FILE, 'w') as file:
        lock(file, LOCK_EX)  # Acquire an exclusive lock
        json.dump(faqs, file)
        unlock(file)  # Release the lock

def center_window(curr_window, win_width, win_height):
    window_width, window_height = win_width, win_height
    screen_width = curr_window.winfo_screenwidth()
    screen_height = curr_window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    curr_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

# Function to go to another window
def go_to_window(windows):
    window.destroy()
    if windows == "back":
        import pos_admin
        pos_admin.create_pos_admin_window()

# Function to create the Help window
def create_help_window():
    global window
    window = Tk()
    window.geometry("972x835")
    window.configure(bg = "#FFE1C6")

    center_window(window,972,835)

    canvas = Canvas(
        window,
        bg = "#FFE1C6",
        height = 835,
        width = 972,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    canvas.place(x = 0, y = 0)
    
    canvas.create_rectangle(
        365.0,
        40.0,
        608.0,
        139.0,
        fill="#5CB0FF",
        outline="")

    canvas.create_text(
        439.0,
        66.0,
        anchor="nw",
        text="FAQs",
        fill="#000000",
        font=("Hanuman Regular", 40 * -1)
    )

    back_button = Button(text="Back", font=("Hanuman Regular", 16), command=lambda: go_to_window("back"), bg="#FFFFFF", relief="raised")
    back_button.place(x=785.0, y=727.0, height=50, width=125)
    
    if shared_state.current_user_loa == "admin":
        add_faq_button = Button(text="Add FAQ", font=("Hanuman Regular", 16), command=open_add_faq_window, bg="#F8D48E", relief="raised")
        add_faq_button.place(x=315.0, y=727.0, height=50, width=125)

        edit_faq_button = Button(text="Edit FAQ", font=("Hanuman Regular", 16), command=open_edit_faq_window, bg="#F8D48E", relief="raised")
        edit_faq_button.place(x=515.0, y=727.0, height=50, width=125)

    
    global faq_entry
    faq_entry = Text(
        bd=0,
        bg="#FFE1C6",  # Match background color
        fg="#000716",
        highlightthickness=0,
        wrap='word'  # Prevent cutting words
    )
    faq_entry.place(
        x=102.0,
        y=180.0,
        width=768.0,
        height=511.0
    )

    # Display the FAQs in the required format
    display_faqs(faq_entry)
    window.resizable(False, False)
    window.mainloop()

# Function to display FAQs
def display_faqs(faq_entry):
    faq_entry.delete(1.0, END)
    for i, faq in enumerate(faqs, 1):
        if isinstance(faq, dict) and 'question' in faq and 'answer' in faq:
            faq_entry.insert(END, f"{i}.) {faq['question']}\n", 'bold')
            faq_entry.tag_configure('bold', font=('Hanuman Regular', 20, 'bold'))
            faq_entry.insert(END, f"- {faq['answer']}\n\n", 'normal')
            faq_entry.tag_configure('normal', font=('Hanuman Regular', 16, 'normal'))
        else:
            # Handle unexpected data
            print(f"Unexpected faq format at index {i}: {faq}")

    faq_entry.config(state='disabled')

# Function to open the Add FAQ window
def open_add_faq_window():
    add_window = Toplevel(window)
    add_window.geometry("400x300")
    add_window.title("Add FAQ")

    center_window(add_window, 400, 300)

    Label(add_window, text="Question:").pack(pady=10)
    question_entry = Text(add_window, width=50, height=1)  # Set height to 1 line
    question_entry.place(x=50, y=35, width=300, height=20)

    Label(add_window, text="Answer:").pack(pady=15)
    answer_entry = Text(add_window, height=5)  # Adjust height as needed
    answer_entry.place(x=50, y=80, width=300, height=75)

    Button(add_window, text="Add", command=lambda: add_faq(question_entry.get("1.0", "end-1c"), answer_entry.get("1.0", "end-1c"), add_window)).place(x=190, y=250)


# Function to add a new FAQ
def add_faq(question, answer, add_window):
    faq_entry.config(state='normal')
    if question and answer:
        faqs.append({"question": question, "answer": answer})  # Append to the list
        save_faqs()
        display_faqs(faq_entry)
        add_window.destroy()
    else:
        messagebox.showerror("Input Error", "Please enter both a question and an answer.")

# Function to open the Edit FAQ window
def open_edit_faq_window():
    edit_window = Toplevel(window)
    edit_window.geometry("400x300")
    edit_window.title("Edit FAQ")

    center_window(edit_window, 400, 300)

    Label(edit_window, text="Question to edit:").pack(pady=10)
    question_entry = Entry(edit_window, width=50)
    question_entry.pack()

    Button(edit_window, text="Find", command=lambda: find_faq(question_entry.get(), edit_window)).pack(pady=20)


# Function to find and edit an FAQ
def find_faq(question, edit_window):
    for faq in faqs:
        if faq['question'] == question:
            edit_faq_window = Toplevel(edit_window)
            edit_faq_window.geometry("400x300")
            edit_faq_window.title("Edit FAQ")

            center_window(edit_faq_window, 400, 300)

            Label(edit_faq_window, text="Answer:").pack(pady=10)
            answer_entry = Text(edit_faq_window, height=5, width=40)
            answer_entry.pack(pady=5)
            answer_entry.insert("1.0", faq['answer'])

            Button(edit_faq_window, text="Save", command=lambda: save_edited_faq(question, answer_entry.get("1.0", "end-1c"), edit_faq_window, edit_window)).pack(pady=20)
            return

    messagebox.showerror("Error", "Question not found in the FAQ list.")

# Function to save the edited FAQ
def save_edited_faq(question, new_answer, edit_faq_window, edit_window):
    faq_entry.config(state='normal')
    for faq in faqs:
        if faq['question'] == question:
            faq['answer'] = new_answer
            save_faqs()
            edit_faq_window.destroy()
            edit_window.destroy()
            display_faqs(faq_entry)
            return

if __name__ == "__main__":
    create_help_window()
