import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
try:
    from ui.main_window import MainWindow
    # from ui.styles import theme_loader
except ImportError:
    # Handle running from src root vs project root
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from ui.main_window import MainWindow
    # We might add a theme loader helper later

import os

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("CitizenZero Super Admin")
    
    # Load Theme
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        theme_path = os.path.join(base_dir, "ui", "styles", "dark_theme.qss")
        with open(theme_path, "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print(f"Warning: {theme_path} not found")

    controller = AppController()
    controller.start()
    
    sys.exit(app.exec())

class AppController:
    def __init__(self):
        self.login_window = None
        self.main_window = None

    def start(self):
        self.show_login()

    def show_login(self):
        # Lazy import to avoid circular dependencies if any
        from ui.login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.login_successful.connect(self.show_main)
        self.login_window.show()

    def show_main(self, user_data):
        print(f"Login Success: {user_data.get('username')}")
        self.main_window = MainWindow()
        # Optionally pass user data to main window
        # self.main_window.set_user(user_data) 
        self.main_window.show()
        
        # Login window closes itself via self.close() inside it
        self.login_window = None

if __name__ == "__main__":
    main()
