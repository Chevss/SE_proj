import login
import registration

registration.save_user('admin', 'admin', 'admin', None, None, None, None, None, None, 'admin', 'admin', 0)

if __name__ == "__main__":
    login.create_login_window()
