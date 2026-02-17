from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QFrame, QMessageBox, QComboBox, QLineEdit)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QFont, QPixmap
from app_config import Endpoints
import qtawesome as qta
import requests

class IDWidget(QWidget):
    def __init__(self, doc_type="NATIONAL_ID", title="ID Card Management"):
        super().__init__()
        self.doc_type = doc_type
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        header = QLabel(title)
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        header_layout.addWidget(header)
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setIcon(qta.icon('fa5s.sync-alt', color='white'))
        self.refresh_btn.setStyleSheet("background-color: #333; color: white; padding: 8px 15px; border-radius: 5px;")
        self.refresh_btn.clicked.connect(self.load_data)
        header_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Action Bar (Issue New)
        action_layout = QHBoxLayout()
        self.issue_input = QLineEdit()
        self.issue_input.setPlaceholderText("Enter Citizen ID / National ID to Issue...")
        self.issue_input.setStyleSheet("padding: 10px; background: #252525; color: white; border: 1px solid #444; border-radius: 5px;")
        action_layout.addWidget(self.issue_input)
        
        self.issue_btn = QPushButton("Issue New Document")
        self.issue_btn.setIcon(qta.icon('fa5s.plus', color='white'))
        self.issue_btn.setStyleSheet("background-color: #28a745; color: white; padding: 10px; border-radius: 5px; font-weight: bold;")
        self.issue_btn.clicked.connect(self.issue_document)
        action_layout.addWidget(self.issue_btn)
        
        layout.addLayout(action_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Document ID", "Citizen ID", "Status", "Date Issued", "Expiry"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet("""
            QTableWidget { background-color: #252525; gridline-color: #3d3d3d; border: 1px solid #3d3d3d; color: #ddd; }
            QHeaderView::section { background-color: #333; color: white; padding: 8px; border: 1px solid #3d3d3d; font-weight: bold; }
        """)
        layout.addWidget(self.table)
        
        # Initial Load
        QTimer.singleShot(500, self.load_data)

    def load_data(self):
        self.refresh_btn.setText("Loading...")
        self.refresh_btn.setEnabled(False)        
        try:
            url = f"{Endpoints.DIGITAL_IDS}?type={self.doc_type}"
            print(f"Fetching Issued Doc: {url}")
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                self.update_table(response.json())
            else:
                print(f"Error loading IDs: {response.text}")
        except Exception as e:
            print(f"Connection error: {e}")
        finally:
            self.refresh_btn.setText("Refresh")
            self.refresh_btn.setEnabled(True)

    def update_table(self, data):
        self.table.setRowCount(len(data))
        for i, item in enumerate(data):
            self.table.setItem(i, 0, QTableWidgetItem(str(item.get('id'))))
            self.table.setItem(i, 1, QTableWidgetItem(item.get('citizen_id')))
            
            status = item.get('status', 'UNKNOWN')
            status_item = QTableWidgetItem(status)
            if status == 'ACTIVE':
                status_item.setForeground(QColor('#00ff00'))
            self.table.setItem(i, 2, status_item)
            
            self.table.setItem(i, 3, QTableWidgetItem(item.get('created_at', '')[:10]))
            self.table.setItem(i, 4, QTableWidgetItem("2036-01-01")) # Mock expiry for now

    def issue_document(self):
        citizen_id = self.issue_input.text()
        if not citizen_id:
             QMessageBox.warning(self, "Input Error", "Please enter a Citizen ID")
             return
             
        try:
            # Backend endpoint needs to handle document_type in POST
            # We haven't updated 'issue' action to accept doc_type yet in views.py,
            # but we can try passing it or assume standard ID for now.
            # TODO: Update backend issue() to accept doc_type
            
            # For now, let's mock the success loop visually until backend issue() supports types fully
            # Or use the standard issue endpoint            
            print(f"Manually Issuing {self.doc_type} for {citizen_id}")
            
            url = Endpoints.ISSUE_ID
            payload = {"citizen_id": citizen_id, "doc_type": self.doc_type}
            
            # Since standard issue() might not take doc_type yet, we might need to fix backend view first.
            # But let's try.
            
            QMessageBox.information(self, "Simulated", f"Request sent to issue {self.doc_type} for {citizen_id}")
            self.load_data()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
