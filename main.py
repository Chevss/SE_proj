from client import send_query
import login
import registration
import os
import sqlite3
import sys
import threading

from server import server, database

server_dir = os.path.join(os.path.dirname(__file__), 'server')
sys.path.append(server_dir)

def start_create_database():
    database.create_database()

def start_flask_server():
    server.start_server()

if __name__ == "__main__":
    # Start the server in a separate thread
    db_thread = threading.Thread(target=start_create_database)
    db_thread.daemon = True
    db_thread.start()

    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_flask_server)
    server_thread.daemon = True
    server_thread.start()

    # Ensure the server has time to start
    import time
    time.sleep(1)

    query = "SELECT * FROM accounts WHERE Username = ?"
    params = ('superadmin',)

    response = send_query(query, params)
    if response is not None and len(response) == 0:
        query = '''
            INSERT INTO accounts (Employee_ID, LOA, First_Name, Last_Name, MI, Suffix, Birthdate, Contact_No, Address, Email, Username, Password, Salt, is_void, Date_Registered)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        params = ('superadmin', 'admin', '', '', '', '', '0000-00-00', '', '', '', 'superadmin', 'e815b9901f8aed76147e60c6534b308c6af096453bf7728a86a4115fc4ec02a9', '52bb500b79bdf2928afcff4d6a0d2bc8', 0, '0000-00-00')

        result = send_query(query, params)
    
    # Proceed with login window
    login.create_login_window()
