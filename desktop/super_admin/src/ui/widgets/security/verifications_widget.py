from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QTableWidget, QTableWidgetItem, QHeaderView, 
                             QPushButton, QLineEdit, QDateEdit, QFrame)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor
import requests
import qtawesome as qta
from app_config import Endpoints

class VerificationsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Identity Verification Logs")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setIcon(qta.icon('fa5s.sync-alt', color='black'))
        refresh_btn.clicked.connect(self.load_data)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(refresh_btn)
        layout.addLayout(header_layout)

        # Filters
        filter_frame = QFrame()
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(0, 5, 0, 5)
        
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Filter by Citizen ID")
        
        filter_btn = QPushButton("Search")
        filter_btn.clicked.connect(self.load_data)
        
        filter_layout.addWidget(self.user_input)
        filter_layout.addWidget(filter_btn)
        layout.addWidget(filter_frame)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Timestamp", "Verifier", "Citizen ID", "Method", "Result"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.doubleClicked.connect(self.show_details)
        
        layout.addWidget(self.table)

    def show_details(self):
        row = self.table.currentRow()
        if row < 0: return
        
        # We need the full log object. 
        # For simplicity, we stored it? No.
        # Ideally, we should store the data list in self.logs.
        pass

    def load_data(self):
        try:
            url = Endpoints.AUDIT_LOGS
            params = {'action': 'VERIFY_ID'}
            
            if self.user_input.text():
                params['user_id'] = self.user_input.text()
                
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                self.logs = response.json() # Store logs
                self.update_table(self.logs)
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Connection error: {e}")

    def update_table(self, logs):
        self.table.setRowCount(0)
        self.table.setRowCount(len(logs))
        
        for i, log in enumerate(logs):
            self.table.setItem(i, 0, QTableWidgetItem(str(log.get('timestamp', '')[:19])))
            
            details = log.get('details', '')
            verifier = "Unknown"
            method = "Online"
            
            if "Verifier" in str(details):
                verifier = "Verifier App"
            
            self.table.setItem(i, 1, QTableWidgetItem(verifier))
            self.table.setItem(i, 2, QTableWidgetItem(log.get('user_id', '')))
            self.table.setItem(i, 3, QTableWidgetItem(method))
            
            status = log.get('status', 'SUCCESS')
            status_item = QTableWidgetItem(status)
            if status == 'SUCCESS':
                status_item.setForeground(QColor('#00ff00'))
            else:
                status_item.setForeground(QColor('#ff0000'))
            self.table.setItem(i, 4, status_item)

    def show_details(self):
        row = self.table.currentRow()
        if row < 0: return
        
        log = self.logs[row]
        
        from PyQt6.QtWidgets import QDialog, QTextEdit
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Verification Details")
        dialog.resize(500, 400)
        
        layout = QVBoxLayout(dialog)
        
        text = QTextEdit()
        import json
        try:
            # Try to format JSON if detail is JSON string
            detail_obj = log.get('details', '')
            if isinstance(detail_obj, str) and (detail_obj.startswith('{') or detail_obj.startswith('[')):
                detail_obj = json.loads(detail_obj)
            
            pretty_json = json.dumps(log, indent=4, default=str)
            text.setText(pretty_json)
        except:
             text.setText(str(log))
             
        text.setReadOnly(True)
        layout.addWidget(text)
        
        dialog.exec()
