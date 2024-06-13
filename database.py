import sqlite3
from tkinter import messagebox

# Create the table if it doesn't exist
def account_database():
    conn = sqlite3.connect('accounts.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (
        Emp_ID INTEGER PRIMARY KEY AUTOINCREMENT, -- Unique employee identifier, auto-incremented
        LOA TEXT NOT NULL,                        -- Level of Access (assuming it's a string)
        First_Name TEXT NOT NULL,                 -- First name of the employee
        Last_Name TEXT NOT NULL,                  -- Last name of the employee
        MI TEXT,                                  -- Middle initial, optional
        Suffix TEXT,                              -- Suffix, optional
        Contact_No TEXT NOT NULL,                 -- Contact number
        Address TEXT NOT NULL,                    -- Address
        Email TEXT NOT NULL UNIQUE,               -- Email address, unique to avoid duplicates
        Username TEXT NOT NULL UNIQUE,            -- Username, unique to avoid duplicates
        Password TEXT NOT NULL,                   -- Password, stored as a hash
        Salt TEXT NOT NULL,                       -- Salt for the password hash
        is_void INTEGER NOT NULL DEFAULT 0        -- Is void flag, 0 for false, 1 for true (assuming it's an integer for boolean)
        )''')
    conn.commit()

def insert_account( loa, first_name, last_name, mi, suffix, contact_no, address, email, username, password, salt, is_void):
        try:
            conn = sqlite3.connect('accounts.db')
            cursor = conn.cursor()

            # Insert data into accounts table
            cursor.execute('''
             INSERT INTO accounts (LOA, "First_Name", "Last_Name", "MI", Suffix, "Contact_No", Address, Email, Username, Password, Salt, "is_void")
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (loa, first_name, last_name, mi, suffix, contact_no, address, email, username, password, salt, is_void))
            # Commit the transaction and close the connection
            conn.commit()
        
        except sqlite3.Error as e:
            print(f"Error inserting data into accounts table: {e}")

def user_logs_database():
    conn = sqlite3.connect('user_logs.db')
    cursor = conn.cursor()
    cursor.execute('''PRAGMA foreign_keys = ON''')
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS user_logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        Employee_id INTEGER NOT NULL,
        Username TEXT NOT NULL,
        action TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        FOREIGN KEY (Employee_id) REFERENCES accounts(Emp_ID)
                   )
                   ''')
    conn.commit()

def invetory_database():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute(''' CREATE TABLE IF NOT EXISTS inventory (
        Barcode TEXT PRIMARY KEY,                -- Unique barcode identifier for each product
        Product_Name TEXT NOT NULL,              -- Name of the product
        Product_Quantity INTEGER NOT NULL,       -- Quantity of the product in stock
        Product_Price REAL NOT NULL,             -- Price of the product
        Product_Description TEXT,                -- Description of the product
        Is_Void INTEGER NOT NULL DEFAULT 0       -- Is void flag, 0 for active, 1 for inactive
                   )''')
    conn.commit()

def purchase_history_database():
    conn = sqlite3.connect('purchase_history.db')
    cursor = conn.cursor()

    # Create purchase_history table if not exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS purchase_history (
        Purchase_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        First_Name TEXT NOT NULL,
        Product_Name TEXT NOT NULL,
        Product_Price REAL NOT NULL,
        Purchase_Quantity INTEGER NOT NULL,
        Time_Stamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        Total_Price REAL NOT NULL,
        Amount_Given REAL NOT NULL,
        Change REAL NOT NULL
    )''')

    conn.commit()


account_database()
user_logs_database()
invetory_database()
purchase_history_database()

"""cursor.execute(
    '''CREATE TRIGGER calculate_total_price
        BEFORE INSERT ON purchase_history
        FOR EACH ROW
        BEGIN
            SET NEW.Total_Price = NEW.Product_Price * NEW.Purchase_Quantity;
        END'''
)
conn.commit()

cursor.execute(
    '''CREATE TRIGGER calculate_change
        BEFORE INSERT ON purchase_history
        FOR EACH ROW
        BEGIN
            SET NEW.Change = NEW.Amount_Given - NEW.Total_Price;
        END'''
)
conn.commit()
"""


