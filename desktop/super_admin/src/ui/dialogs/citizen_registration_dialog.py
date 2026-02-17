from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QComboBox, QDateEdit, QMessageBox)
from PyQt6.QtCore import Qt, QDate
import requests
from app_config import Endpoints

class CitizenRegistrationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Register New Citizen")
        self.resize(500, 600)
        self.setStyleSheet("""
            QDialog { background-color: #252525; color: white; }
            QLabel { color: #ddd; font-size: 14px; margin-bottom: 5px; }
            QLineEdit, QComboBox, QDateEdit { 
                padding: 10px; 
                background-color: #333; 
                border: 1px solid #444; 
                border-radius: 5px; 
                color: white; 
                font-size: 14px;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus { border: 1px solid #0088cc; }
            QPushButton { 
                background-color: #0088cc; color: white; padding: 12px; border-radius: 5px; font-weight: bold;
            }
            QPushButton:hover { background-color: #0099dd; }
            QPushButton#CancelBtn { background-color: #444; }
            QPushButton#CancelBtn:hover { background-color: #555; }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("New Citizen Registration")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: white; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Fields
        self.fname_input = self.add_field(layout, "First Name")
        self.lname_input = self.add_field(layout, "Last Name")
        self.nid_input = self.add_field(layout, "National ID (Unique)")
        
        layout.addWidget(QLabel("Date of Birth"))
        self.dob_input = QDateEdit()
        self.dob_input.setDisplayFormat("yyyy-MM-dd")
        self.dob_input.setDate(QDate.currentDate().addYears(-18))
        self.dob_input.setCalendarPopup(True)
        layout.addWidget(self.dob_input)
        
        layout.addWidget(QLabel("Gender"))
        self.gender_input = QComboBox()
        self.gender_input.addItems(["Male", "Female", "Other"])
        layout.addWidget(self.gender_input)
        
        self.county_input = self.add_field(layout, "County of Birth")
        self.phone_input = self.add_field(layout, "Phone Number")
        
        layout.addStretch()
        
        # Buttons
        btn_layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("CancelBtn")
        cancel_btn.clicked.connect(self.reject)
        
        submit_btn = QPushButton("Register Citizen")
        submit_btn.clicked.connect(self.submit_registration)
        
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(submit_btn)
        layout.addLayout(btn_layout)

    def add_field(self, layout, label_text):
        layout.addWidget(QLabel(label_text))
        field = QLineEdit()
        layout.addWidget(field)
        return field

    def submit_registration(self):
        # Validate
        if not self.nid_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "National ID is required.")
            return

        gender_map = {"Male": "M", "Female": "F", "Other": "O"}
        
        data = {
            "first_name": self.fname_input.text().strip(),
            "last_name": self.lname_input.text().strip(),
            "national_id": self.nid_input.text().strip(),
            "date_of_birth": self.dob_input.date().toString("yyyy-MM-dd"),
            "gender": gender_map.get(self.gender_input.currentText(), "O"),
            "county_of_birth": self.county_input.text().strip(),
            "phone_number": self.phone_input.text().strip(),
            # Defaults
            "place_of_birth": self.county_input.text().strip() or "Unknown",
            "is_alive": True
        }
        
        try:
            url = Endpoints.CITIZENS
            response = requests.post(url, json=data, timeout=5)
            
            if response.status_code == 201:
                QMessageBox.information(self, "Success", "Citizen registered successfully!")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", f"Failed to register citizen.\nStatus: {response.status_code}\nResponse: {response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Network Error", f"Could not connect to backend.\nError: {e}")
