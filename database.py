import sqlite3
from tkinter import messagebox
import secrets
import hashlib

# Connect to SQLite database
conn = sqlite3.connect('accounts.db')
cursor = conn.cursor()
# Create table if not exists
try:
    # Create the table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (
                        username TEXT PRIMARY KEY,
                        salt TEXT,
                        hashed_password TEXT,
                        Loa TEXT)''')
    conn.commit()
except sqlite3.Error as e:
    print("Error occurred while creating the table:", e)
"""cursor.execute("SELECT * FROM accounts")

rows = cursor.fetchall()

for row in rows:
    print(row)"""

