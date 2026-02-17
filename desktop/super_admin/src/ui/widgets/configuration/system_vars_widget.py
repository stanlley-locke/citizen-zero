from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QPushButton, QHBoxLayout, QMessageBox, QInputDialog)
from PyQt6.QtCore import Qt
import requests

CONFIG_API = "http://127.0.0.1:8006/api/v1/config/"

class SystemVarsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_config()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        header_layout = QHBoxLayout()
        title = QLabel("System Variables & Environment")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: white;")
        header_layout.addWidget(title)
        
        btn_add = QPushButton("+ Add Variable")
        btn_add.setStyleSheet("""
            QPushButton { background-color: #333; color: white; padding: 6px 12px; border-radius: 4px; border: 1px solid #555; }
            QPushButton:hover { background-color: #444; }
        """)
        btn_add.clicked.connect(self.add_variable)
        header_layout.addWidget(btn_add)
        
        layout.addLayout(header_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Variable Key", "Value"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setStyleSheet("""
            QTableWidget { background-color: #1a1a1a; color: white; border: 1px solid #333; gridline-color: #333; }
            QHeaderView::section { background-color: #333; color: white; padding: 8px; border: none; font-weight: bold; }
            QTableWidget::item { padding: 5px; }
        """)
        layout.addWidget(self.table)
        
        # Save
        btn_save = QPushButton("Apply System Changes")
        btn_save.setStyleSheet("""
            QPushButton { background-color: #bb86fc; color: black; font-weight: bold; padding: 12px; border-radius: 6px; }
            QPushButton:hover { background-color: #a370f7; }
        """)
        btn_save.clicked.connect(self.save_config)
        layout.addWidget(btn_save)

    def load_config(self):
        try:
            resp = requests.get(CONFIG_API, timeout=2)
            if resp.status_code == 200:
                data = resp.json()
                system = data.get('system', {})
                
                self.table.setRowCount(len(system))
                for i, (k, v) in enumerate(system.items()):
                    self.table.setItem(i, 0, QTableWidgetItem(str(k)))
                    self.table.setItem(i, 1, QTableWidgetItem(str(v)))
        except:
            pass

    def add_variable(self):
        key, ok1 = QInputDialog.getText(self, "New Variable", "Enter Variable Name:")
        if ok1 and key:
            val, ok2 = QInputDialog.getText(self, "New Variable", f"Enter Value for '{key}':")
            if ok2:
                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(key))
                self.table.setItem(row, 1, QTableWidgetItem(val))

    def save_config(self):
        updates = {}
        for i in range(self.table.rowCount()):
            key_item = self.table.item(i, 0)
            val_item = self.table.item(i, 1)
            
            if key_item and val_item:
                updates[key_item.text()] = val_item.text()
                
        payload = {"system": updates}
        
        try:
            resp = requests.post(CONFIG_API, json=payload, timeout=2)
            if resp.status_code == 200:
                QMessageBox.information(self, "Success", "System configuration saved.")
            else:
                QMessageBox.warning(self, "Failed", "Could not save configuration.")
        except Exception as e:
             QMessageBox.critical(self, "Error", str(e))
