from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QFrame, QMessageBox, QHBoxLayout)
from PyQt6.QtCore import Qt, pyqtSignal
import requests
from app_config import Endpoints
import qtawesome as qta

class LoginWindow(QWidget):
    login_successful = pyqtSignal(dict) # Emits user data on success

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CitizenZero - Admin Login")
        self.setFixedSize(400, 500)
        self.setStyleSheet("background-color: #1a1a1a; color: white;")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Main Card
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #252525;
                border-radius: 10px;
                border: 1px solid #3d3d3d;
            }
        """)
        layout.addWidget(card)
        
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(20)
        card_layout.setContentsMargins(40, 40, 40, 40)
        
        # Header (Logo)
        # Using Icon for now
        icon_label = QLabel()
        icon = qta.icon('fa5s.fingerprint', color='#00ff00')
        icon_label.setPixmap(icon.pixmap(64, 64))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("border: none; background: transparent;")
        card_layout.addWidget(icon_label)
        
        title_label = QLabel("SUPER ADMIN")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px; border: none; background: transparent;")
        card_layout.addWidget(title_label)
        
        # Inputs
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username / Admin ID")
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                background-color: #333;
                border: 1px solid #444;
                border-radius: 5px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #00ff00;
            }
        """)
        card_layout.addWidget(self.username_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(self.username_input.styleSheet())
        card_layout.addWidget(self.password_input)
        
        # Button
        self.login_btn = QPushButton("LOGIN")
        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #0088cc;
                color: white;
                font-weight: bold;
                padding: 12px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0099dd;
            }
            QPushButton:pressed {
                background-color: #0077bb;
            }
        """)
        self.login_btn.clicked.connect(self.handle_login)
        card_layout.addWidget(self.login_btn)
        
        # Close Button (since frameless)
        close_btn = QPushButton("Exit", self)
        close_btn.setGeometry(350, 10, 40, 20)
        close_btn.setStyleSheet("background: transparent; color: #888; border: none;")
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self.close)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter credentials")
            return

        self.login_btn.setText("Authenticating...")
        self.login_btn.setEnabled(False)
        
        # Real Auth Call
        try:
            url = Endpoints.LOGIN
            payload = {
                "username": username,
                "password": password
            }
            
            response = requests.post(url, json=payload, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                # self.login_successful.emit({"username": username, "role": "super_admin", "tokens": data.get('tokens')})
                # Close handled by main controller usually, or here
                self.login_successful.emit(data)
                self.close()
            elif response.status_code == 403:
                QMessageBox.warning(self, "Access Denied", "You do not have admin privileges.")
            else:
                 QMessageBox.warning(self, "Failed", "Invalid Credentials")
                 
        except Exception as e:
             QMessageBox.critical(self, "Connection Error", f"Could not connect to Auth Service: {e}")
        finally:
             self.login_btn.setText("LOGIN")
             self.login_btn.setEnabled(True)

    def mousePressEvent(self, event):
        # Allow dragging the frameless window
        self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = event.globalPosition().toPoint() - self.oldPos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPosition().toPoint()
