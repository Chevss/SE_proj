import sqlite3
from datetime import datetime

def create_database():
    conn = sqlite3.connect('Trimark_construction_supply.db')
    cursor = conn.cursor()

    # Accounts
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
        Employee_ID TEXT PRIMARY KEY,             -- Unique employee identifier, auto-incremented
        LOA TEXT NOT NULL,                        -- Level of Access (assuming it's a string)
        First_Name TEXT NOT NULL,                 -- First name of the user
        Last_Name TEXT NOT NULL,                  -- Last name of the user
        MI TEXT,                                  -- Middle initial, optional
        Suffix TEXT,                              -- Suffix, optional
        Birthdate TEXT NOT NULL,                  -- Birthdate of the user
        Contact_No TEXT NOT NULL,                 -- Contact number
        Address TEXT NOT NULL,                    -- Address
        Email TEXT NOT NULL UNIQUE,               -- Email address, unique to avoid duplicates
        Username TEXT NOT NULL UNIQUE,            -- Username, unique to avoid duplicates
        Password TEXT NOT NULL,                   -- Password, stored as a hash
        Salt TEXT NOT NULL,                       -- Salt for the password hash
        is_void INTEGER NOT NULL DEFAULT 0,       -- Is void flag, 0 for false, 1 for true (assuming it's an integer for boolean)
        Date_Registered TIMESTAMP NOT NULL        -- Logs the date of registration
        )
    ''')
    
    # User Logs
    cursor.execute('''PRAGMA foreign_keys = ON''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        --Employee_id INTEGER NOT NULL,
        Username TEXT NOT NULL,
        action TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
        --FOREIGN KEY (Employee_id) REFERENCES accounts (Emp_ID)
        )
    ''')
    
    # Inventory
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
        Barcode TEXT PRIMARY KEY,                -- Unique barcode identifier for each product
        Product_Name TEXT NOT NULL,              -- Name of the product
        Product_Quantity INTEGER NOT NULL,       -- Quantity of the product in stock
        Product_Price REAL NOT NULL,             -- Price of the product
        Product_Description TEXT,                -- Description of the product
        Date_Delivered TIMESTAMP NOT NULL,
        Is_Void INTEGER NOT NULL DEFAULT 0       -- Is void flag, 0 for active, 1 for inactive
        )
    ''')
    
    # Purchase History
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchase_history (
        Purchase_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        First_Name TEXT NOT NULL,
        Product_Name TEXT NOT NULL,
        Product_Price REAL NOT NULL,
        Purchase_Quantity INTEGER NOT NULL,
        Time_Stamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        Total_Price REAL NOT NULL,
        Amount_Given REAL NOT NULL,
        Change REAL NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def insert_account(loa, first_name, last_name, mi, suffix, contact_no, address, email, username, password, salt, is_void):
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
        conn.close()
    
    except sqlite3.Error as e:
        print(f"Error inserting data into accounts table: {e}")

def insert_product(Barcode, Product_Name, Product_Quantity, Product_Price, Product_Description, Date_Delivered):
    try:
        conn = sqlite3.connect('Trimark_construction_supply.db')
        cursor = conn.cursor()

        # Check if Barcode already exists
        cursor.execute('SELECT Barcode FROM inventory WHERE Barcode = ?', (Barcode,))
        existing = cursor.fetchone()

        if existing:
            # Barcode exists, handle accordingly (update or ignore)
            print(f"Barcode {Barcode} already exists in inventory.")
            # Example: Update existing record
            cursor.execute('''
                UPDATE inventory
                SET Product_Name = ?,
                    Product_Quantity = ?,
                    Product_Price = ?,
                    Product_Description = ?,
                    Date_Delivered = ?
                WHERE Barcode = ?
            ''', (Barcode, Product_Name, Product_Quantity, Product_Price, Product_Description, Date_Delivered))
        else:
            # Insert new record
            cursor.execute('''
                INSERT INTO inventory (Barcode, Product_Name, Product_Quantity, Product_Price, Product_Description, Date_Delivered)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (Barcode, Product_Name, Product_Quantity, Product_Price, Product_Description, Date_Delivered))

        # Commit the transaction and close the connection
        conn.commit()
        conn.close()
    
    except sqlite3.Error as e:
        print(f"Error inserting data into inventory table: {e}")

"""datetm = datetime.now()
insert_product("012045893", "Old spice Canyonas", 2, 399.00, "na", datetm)
inse`rt_product('123456789', 'Product A', 100, 19.99, 'Description of Product A', datetm)"""

def print_table_schema(table_name):
    conn = sqlite3.connect('Trimark_construction_supply.db')
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    
    print(f"Table: {table_name}")
    print("Type\t\tColumn Name")
    print("-" * 30)
    for column in columns:
        print(f"{column[2]}\t\t{column[1]}")
    print()
    conn.close()

def print_table_data(table_name):
    conn = sqlite3.connect('Trimark_construction_supply.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")  # Limiting to 5 rows for brevity
    rows = cursor.fetchall()
    
    print(f"Table: {table_name}")
    for row in rows:
        print(row)
    print()
    conn.close()

if __name__ == "__main__":
    create_database()
    tables = ['accounts', 'user_logs', 'inventory', 'purchase_history']
    
    # Print schema for each table
    for table in tables:
        print_table_schema(table)
    
    # Print sample data for each table
    for table in tables:
        print_table_data(table)



"""insert_account( 'admin', "Chevy Joel", 'Gaiti', 'B', "", '09655431219', 'blk 7, lot 17 UBB', 'chevy023.gaiti@gmail.com', username, password, salt, is_void)"""



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


