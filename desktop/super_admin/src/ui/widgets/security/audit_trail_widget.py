from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QTableWidget, QTableWidgetItem, QHeaderView, 
                             QComboBox, QLineEdit, QPushButton, QDateEdit, QFrame,
                             QFileDialog, QMessageBox) # Added missing imports
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor, QIcon
import requests
import qtawesome as qta
import csv
from app_config import Endpoints

class AuditTrailWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_logs()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # --- Filter Bar ---
        filter_frame = QFrame()
        filter_frame.setObjectName("Card")
        filter_layout = QHBoxLayout(filter_frame)
        
        self.severity_combo = QComboBox()
        self.severity_combo.addItems(["All Severities", "INFO", "WARNING", "CRITICAL"])
        
        self.action_input = QLineEdit()
        self.action_input.setPlaceholderText("Filter by Action (e.g. LOGIN)")
        
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Filter by User ID")
        
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate().addDays(-7)) # Default last 7 days
        
        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())
        
        search_btn = QPushButton("Filter")
        search_btn.setIcon(qta.icon('fa5s.search', color='white'))
        search_btn.clicked.connect(self.load_logs)
        
        export_btn = QPushButton("Export CSV")
        export_btn.setIcon(qta.icon('fa5s.file-csv', color='white'))
        export_btn.clicked.connect(self.export_csv)
        
        filter_layout.addWidget(QLabel("Severity:"))
        filter_layout.addWidget(self.severity_combo)
        filter_layout.addWidget(self.action_input)
        filter_layout.addWidget(self.user_input)
        filter_layout.addWidget(QLabel("From:"))
        filter_layout.addWidget(self.start_date)
        filter_layout.addWidget(QLabel("To:"))
        filter_layout.addWidget(self.end_date)
        filter_layout.addWidget(search_btn)
        filter_layout.addWidget(export_btn)
        
        layout.addWidget(filter_frame)

        # --- Table ---
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["Timestamp", "Severity", "Actor Type", "Username", "Action", "User ID", "Details", "IP"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)
        
        layout.addWidget(self.table)

    def export_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "audit_logs.csv", "CSV Files (*.csv)")
        if not path:
            return
            
        try:
            with open(path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                headers = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
                writer.writerow(headers)
                
                for row in range(self.table.rowCount()):
                    row_data = []
                    for col in range(self.table.columnCount()):
                        item = self.table.item(row, col)
                        row_data.append(item.text() if item else "")
                    writer.writerow(row_data)
                    
            QMessageBox.information(self, "Success", "Export successful!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save file: {e}")

    def load_logs(self):
        try:
            url = Endpoints.AUDIT_LOGS
            params = {}
            
            # Severity
            severity = self.severity_combo.currentText()
            if severity != "All Severities":
                params['severity'] = severity
            
            # Action
            action = self.action_input.text().strip()
            if action:
                params['action'] = action
                
            # User
            user = self.user_input.text().strip()
            if user:
                params['user_id'] = user
                
            # Dates (Format YYYY-MM-DD)
            params['start_date'] = self.start_date.date().toString("yyyy-MM-dd")
            params['end_date'] = self.end_date.date().toString("yyyy-MM-dd")

            print(f"Fetching Audit Logs with params: {params}")
            response = requests.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                logs = response.json()
                self.update_table(logs)
            else:
                print(f"Failed to fetch logs: {response.text}")
                
        except Exception as e:
            print(f"Error loading logs: {e}")

    def update_table(self, logs):
        self.table.setRowCount(0)
        self.table.setRowCount(len(logs))
        
        for i, log in enumerate(logs):
            # Timestamp
            self.table.setItem(i, 0, QTableWidgetItem(str(log.get('timestamp', '')[:19])))
            
            # Severity (Color Coded)
            severity = log.get('severity', 'INFO')
            sev_item = QTableWidgetItem(severity)
            if severity == 'CRITICAL':
                sev_item.setForeground(QColor('red'))
                sev_item.setFont(qta.font('fa5s', 10))
            elif severity == 'WARNING':
                sev_item.setForeground(QColor('orange'))
            self.table.setItem(i, 1, sev_item)
            
            self.table.setItem(i, 2, QTableWidgetItem(log.get('actor_type', 'SYSTEM')))
            self.table.setItem(i, 3, QTableWidgetItem(log.get('username', '') or ''))
            self.table.setItem(i, 4, QTableWidgetItem(log.get('action', '')))
            self.table.setItem(i, 5, QTableWidgetItem(log.get('user_id', '')))
            self.table.setItem(i, 6, QTableWidgetItem(log.get('details', '')))
            self.table.setItem(i, 7, QTableWidgetItem(log.get('ip_address', '')))
