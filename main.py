from client import send_query
import login
import registration
import sqlite3


if __name__ == "__main__":
    query = "SELECT * FROM accounts WHERE Username = ?"
    params = ('admin',)

    response = send_query(query, params)
    if response is not None and len(response) == 0:
        # If admin user doesn't exist, register it
        registration.save_user('admin', '', '', '', '', '', '', '', '', 'admin', 'admin', 0)
    
    # Proceed with login window
    login.create_login_window()
