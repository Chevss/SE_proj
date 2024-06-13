import sqlite3
from tkinter import messagebox
import secrets
import hashlib

# Connect to SQLite database
conn = sqlite3.connect('accounts.db')
cursor = conn.cursor()

# Create table if not exists
try:
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        Emp_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Loa TEXT NOT NULL,
        FirstName TEXT NOT NULL,
        LastName TEXT NOT NULL,
        MI TEXT,
        Suffix TEXT,
        ContactNo TEXT NOT NULL,
        Address TEXT NOT NULL,
        Email TEXT NOT NULL UNIQUE,
        Username TEXT NOT NULL UNIQUE,
        Password TEXT NOT NULL,
        Salt TEXT NOT NULL,
        is_void INTEGER DEFAULT 0
    )''')
    conn.commit()
except sqlite3.Error as e:
    print("Error occurred while creating the table:", e)

cursor.execute("SELECT * FROM accounts")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
