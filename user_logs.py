from client import send_query
from datetime import datetime
import sqlite3

def log_actions(username, action):
    # Fetch the Employee_ID based on the username
    query_employee_id = 'SELECT Employee_ID FROM accounts WHERE Username = ?'
    params_employee_id = (username,)
    result_employee_id = send_query(query_employee_id, params_employee_id)
    
    if result_employee_id and isinstance(result_employee_id, list) and len(result_employee_id) > 0:
        employee_id = result_employee_id[0][0]  # Assuming Employee_ID is the first column in the result
    else:
        # Handle the case where the username does not exist in the accounts table
        print(f"Username {username} not found in accounts table.")
        return

    # Insert the log entry with Employee_ID
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query_insert_log = 'INSERT INTO user_logs (Employee_ID, Username, action, timestamp) VALUES (?, ?, ?, ?)'
    params_insert_log = (employee_id, username, action, timestamp)
    result_insert = send_query(query_insert_log, params_insert_log)
