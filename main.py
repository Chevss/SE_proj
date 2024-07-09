import login
import registration
import database
import sqlite3


if __name__ == "__main__":
    database.create_database()
    conn = sqlite3.connect('Trimark_construction_supply.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM accounts WHERE Username = ?", ('admin',))
    if not cursor.fetchone():
        registration.save_user('admin', '', '', '', '', '', '', '', '', 'admin', 'admin', 0)
    # save_user(loa, first_name, last_name, mi, suffix, birthdate, contact_number, home_address, email, username, password, is_void):
    login.create_login_window()
