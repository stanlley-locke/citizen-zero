from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QIcon
import qtawesome as qta
import requests
from app_config import Endpoints
from ui.dialogs.request_detail_dialog import RequestDetailDialog

class RequestsWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Credential Requests")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # Refresh Button
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setIcon(qta.icon('fa5s.sync-alt', color='white'))
        self.refresh_btn.setStyleSheet("""
            QPushButton { background-color: #333; color: white; padding: 8px 15px; border-radius: 5px; border: 1px solid #444; }
            QPushButton:hover { background-color: #444; }
        """)
        self.refresh_btn.clicked.connect(self.load_requests)
        header_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Date", "Citizen ID", "Document Type", "Status", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setStyleSheet("""
            QTableWidget { background-color: #252525; border: 1px solid #3d3d3d; color: #ddd; }
            QHeaderView::section { background-color: #333; color: white; padding: 8px; border: 1px solid #3d3d3d; font-weight: bold; }
        """)
        layout.addWidget(self.table)
        
        # Connect Double Click
        self.table.itemDoubleClicked.connect(self.show_request_details)
        
        self.requests = []
        
        # Initial Load
        QTimer.singleShot(500, self.load_requests)

    def load_requests(self):
        self.refresh_btn.setEnabled(False)
        try:
            url = Endpoints.REQUESTS
            print(f"Fetching requests from {url}")
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and 'results' in data:
                    self.requests = data['results']
                elif isinstance(data, list):
                    self.requests = data
                else:
                    self.requests = []
                    
                self.update_table(self.requests)
            else:
                print(f"Failed to fetch requests: {response.status_code}")
        except Exception as e:
            print(f"Error fetching requests: {e}")
        finally:
            self.refresh_btn.setEnabled(True)

    def update_table(self, requests_data):
        self.table.setRowCount(0) # Clear
        
        # Sort pending first
        requests_data.sort(key=lambda x: 0 if x.get('status') == 'PENDING' else 1)
        
        self.table.setRowCount(len(requests_data))
        
        for i, req in enumerate(requests_data):
            date = str(req.get('request_date', ''))[:10]
            cid = str(req.get('citizen_id', ''))
            dtype = str(req.get('doc_type', '')).replace('_', ' ').title()
            status = str(req.get('status', 'PENDING'))
            req_id = req.get('id')
            
            # STORE ID IN FIRST COLUMN ITEM
            item_date = QTableWidgetItem(date)
            item_date.setData(Qt.ItemDataRole.UserRole, req_id)
            self.table.setItem(i, 0, item_date)
            
            self.table.setItem(i, 1, QTableWidgetItem(cid))
            self.table.setItem(i, 2, QTableWidgetItem(dtype))
            
            status_item = QTableWidgetItem(status)
            if status == 'PENDING':
                status_item.setForeground(QColor("#ffcc00"))
            elif status == 'APPROVED':
                status_item.setForeground(QColor("#00ff00"))
            elif status == 'REJECTED':
                status_item.setForeground(QColor("#ff0000"))
            self.table.setItem(i, 3, status_item)
            
            # Action Buttons
            if status == 'PENDING':
                widget = QWidget()
                h_layout = QHBoxLayout(widget)
                h_layout.setContentsMargins(0, 0, 0, 0)
                h_layout.setSpacing(5)
                
                btn_approve = QPushButton("Approve")
                btn_approve.setStyleSheet("background-color: #0088cc; color: white; border-radius: 3px; padding: 4px;")
                btn_approve.clicked.connect(lambda checked, rid=req_id, cid=cid, dt=dtype: self.approve_request(rid, cid, dt))
                
                btn_reject = QPushButton("Reject")
                btn_reject.setStyleSheet("background-color: #cc0000; color: white; border-radius: 3px; padding: 4px;")
                btn_reject.clicked.connect(lambda checked, rid=req_id: self.reject_request(rid))
                
                h_layout.addWidget(btn_approve)
                h_layout.addWidget(btn_reject)
                self.table.setCellWidget(i, 4, widget)
            else:
                self.table.setItem(i, 4, QTableWidgetItem("-"))

    def show_request_details(self, item):
        row = item.row()
        req_id = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        request = next((r for r in self.requests if r.get('id') == req_id), None)
        
        if request:
            dialog = RequestDetailDialog(request, self)
            dialog.exec()

    def approve_request(self, req_id, citizen_id, doc_type):
        reply = QMessageBox.question(self, "Approve Request", 
                                     f"Are you sure you want to approve the {doc_type} for Citizen {citizen_id}?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.process_approval(req_id, citizen_id)

    def process_approval(self, req_id, citizen_id):
        try:
            # Use the dedicated approve endpoint which handles status update and issuance
            url = f"{Endpoints.REQUESTS}{req_id}/approve/"
            response = requests.post(url, timeout=5)
            
            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Request approved and document issued.")
                self.load_requests()
            else:
                 QMessageBox.warning(self, "Error", f"Failed to approve: {response.text}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Connection error: {str(e)}")

    def reject_request(self, req_id):
        reply = QMessageBox.question(self, "Reject Request", 
                                     "Are you sure you want to reject this request?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                url = f"{Endpoints.REQUESTS}{req_id}/reject/"
                response = requests.post(url, json={'reason': 'Rejected by Admin'}, timeout=5)
                
                if response.status_code == 200:
                    QMessageBox.information(self, "Success", "Request rejected.")
                    self.load_requests()
                else:
                    QMessageBox.warning(self, "Error", f"Failed to reject: {response.text}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Connection error: {str(e)}")
