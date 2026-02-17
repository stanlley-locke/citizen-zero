from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, QLabel, QPushButton, QFrame, QMessageBox, QScrollArea)
from PyQt6.QtCore import Qt
import requests

CONFIG_API = "http://127.0.0.1:8006/api/v1/config/"

class NetworkConfigWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.inputs = {}
        self.init_ui()
        self.load_config()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("Network API Configuration")
        header.setStyleSheet("font-size: 22px; font-weight: bold; color: white; margin-bottom: 20px;")
        layout.addWidget(header)
        
        # Scroll Area for Form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")
        
        content = QWidget()
        self.form_layout = QFormLayout(content)
        self.form_layout.setSpacing(20)
        self.form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        # Actions
        btn_save = QPushButton("Save Network Settings")
        btn_save.setStyleSheet("""
            QPushButton { background-color: #05B8CC; color: white; font-weight: bold; padding: 12px; border-radius: 6px; }
            QPushButton:hover { background-color: #04abcd; }
        """)
        btn_save.clicked.connect(self.save_config)
        layout.addWidget(btn_save)

    def add_field(self, key, value):
        lbl = QLabel(key.replace("_", " ").title())
        lbl.setStyleSheet("color: #ccc; font-size: 14px; font-weight: bold;")
        
        inp = QLineEdit(str(value))
        inp.setStyleSheet("""
            QLineEdit { background-color: #222; color: #0f0; border: 1px solid #444; padding: 8px; border-radius: 4px; font-family: Consolas; }
            QLineEdit:focus { border: 1px solid #05B8CC; }
        """)
        
        self.form_layout.addRow(lbl, inp)
        self.inputs[key] = inp

    def load_config(self):
        try:
            resp = requests.get(CONFIG_API, timeout=2)
            if resp.status_code == 200:
                data = resp.json()
                network = data.get('network', {})
                
                # Clear existing rows if reload (simple reset)
                # For now just assumes init once
                
                for key, val in network.items():
                    self.add_field(key, val)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load config: {str(e)}")

    def save_config(self):
        updates = {}
        for key, inp in self.inputs.items():
            updates[key] = inp.text()
            
        payload = {"network": updates}
        
        try:
            resp = requests.post(CONFIG_API, json=payload, timeout=2)
            if resp.status_code == 200:
                QMessageBox.information(self, "Success", "Network configuration updated successfully!")
            else:
                QMessageBox.warning(self, "Failed", "Could not save configuration.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
