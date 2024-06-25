import sqlite3
from datetime import datetime
from database import create_database

create_database()

def log_actions(username, action):
    conn = sqlite3.connect('Trimark_construction_supply.db')
    cursor = conn.cursor()

    # Fetch the Employee_ID based on the username
    cursor.execute('SELECT Employee_ID FROM accounts WHERE Username = ?', (username,))
    row = cursor.fetchone()
    if row:
        employee_id = row[0]
    else:
        # Handle the case where the username does not exist in the accounts table
        print(f"Username {username} not found in accounts table.")
        conn.close()
        return

    # Insert the log entry with Employee_ID
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO user_logs (Employee_ID, Username, action, timestamp) VALUES (?, ?, ?, ?)', 
                   (employee_id, username, action, timestamp))

    conn.commit()
    conn.close()

'''
def fetch_user_logs_data():
    conn = sqlite3.connect('Trimark_construction_supply.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user_logs")
    rows = cursor.fetchall()
    
    conn.close()
    return rows

def print_inventory(rows):
    for row in rows:
        print(f"Log ID: {row[0]}, Employee ID: {row[1]}, Username: {row[2]}, Action: {row[3]}, Timestamp: {row[4]}")

# Fetch all data from the inventory table
inventory_data = fetch_user_logs_data()

# Print all data
print_inventory(inventory_data)
'''