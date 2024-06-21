import sqlite3
from datetime import datetime
from database import create_database

create_database()

def log_actions(username, action):
    conn = sqlite3.connect('Trimark_construction_supply.db')
    cursor = conn.cursor()

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO user_logs (username, action, timestamp) VALUES (?, ?, ?)', (username, action, timestamp))

    conn.commit()
    conn.close()

def fetch_user_logs_data():
    conn = sqlite3.connect('Trimark_construction_supply.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user_logs")
    rows = cursor.fetchall()
    
    conn.close()
    return rows

def print_inventory(rows):
    for row in rows:
        print(f"Log ID: {row[0]}, Username: {row[1]}, Action: {row[2]}, Timestamp: {row[3]}")

# Fetch all data from the inventory table
inventory_data = fetch_user_logs_data()

# Print all data
print_inventory(inventory_data)
