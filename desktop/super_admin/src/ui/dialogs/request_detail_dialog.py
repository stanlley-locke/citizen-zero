from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QGridLayout, QScrollArea, QWidget)
from PyQt6.QtCore import Qt
import qtawesome as qta
import requests
from app_config import Endpoints

class RequestDetailDialog(QDialog):
    def __init__(self, request_data, parent=None):
        super().__init__(parent)
        self.request = request_data
        self.setWindowTitle(f"Request Details - {self.request.get('doc_type', 'Unknown')}")
        self.resize(500, 450)
        self.setStyleSheet("""
            QDialog { background-color: #252525; color: white; }
            QLabel { color: #ddd; font-size: 14px; }
            QLabel#ValueLabel { color: white; font-weight: bold; font-size: 15px; }
            QLabel#SectionHeader { color: #0088cc; font-weight: bold; font-size: 16px; margin-top: 15px; margin-bottom: 5px; }
            QPushButton { 
                background-color: #0088cc; color: white; border: none; padding: 8px 16px; border-radius: 4px; font-weight: bold;
            }
            QPushButton:hover { background-color: #0099dd; }
        """)
        
        layout = QVBoxLayout(self)
        
        # Header
        header = QFrame()
        header.setStyleSheet("background-color: #1a1a1a; border-bottom: 1px solid #333;")
        header_layout = QHBoxLayout(header)
        
        icon_label = QLabel()
        icon_label.setPixmap(qta.icon('fa5s.file-alt', color='white').pixmap(32, 32))
        header_layout.addWidget(icon_label)
        
        doc_type = self.request.get('doc_type', '').replace('_', ' ').title()
        title_label = QLabel(f"{doc_type} Request")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        layout.addWidget(header)

        # Content
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 10)
        
        # Request Info
        self.add_section_header(content_layout, "Request Information", "fa5s.info-circle")
        
        req_grid = QGridLayout()
        self.add_field(req_grid, 0, 0, "Citizen ID", self.request.get('citizen_id'))
        self.add_field(req_grid, 0, 1, "Date", str(self.request.get('request_date'))[:10])
        self.add_field(req_grid, 1, 0, "Status", self.request.get('status'))
        self.add_field(req_grid, 1, 1, "Notes", self.request.get('notes') or "N/A")
        content_layout.addLayout(req_grid)
        
        # Issued Document Info (if approved)
        if self.request.get('status') == 'APPROVED':
            self.load_issued_document(content_layout)
        
        content_layout.addStretch()
        layout.addLayout(content_layout)
        
        # Footer
        footer_layout = QHBoxLayout()
        footer_layout.addStretch()
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        footer_layout.addWidget(close_btn)
        layout.addLayout(footer_layout)

    def load_issued_document(self, layout):
        self.add_section_header(layout, "Issued Document Details", "fa5s.id-card")
        
        # Fetch details from backend
        try:
            cid = self.request.get('citizen_id')
            dtype = self.request.get('doc_type')
            # Filter strictly by citizen_id and type
            url = f"{Endpoints.DIGITAL_IDS}?citizen_id={cid}&type={dtype}"
            print(f"Fetching Issued Doc: {url}")
            
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                results = response.json()
                if isinstance(results, dict): results = results.get('results', []) # handle pagination if present
                
                doc = results[0] if results else None
                
                if doc:
                    doc_grid = QGridLayout()
                    self.add_field(doc_grid, 0, 0, "Document Number", doc.get('national_id')) # using national_id field for doc number
                    self.add_field(doc_grid, 0, 1, "Expiry Date", str(doc.get('expiry_date'))[:10])
                    layout.addLayout(doc_grid)
                else:
                    layout.addWidget(QLabel("Document issued but details not found."))
            else:
                 layout.addWidget(QLabel("Failed to fetch document details."))
        except Exception as e:
            layout.addWidget(QLabel(f"Error: {e}"))

    def add_section_header(self, layout, text, icon_name):
        header_layout = QHBoxLayout()
        label = QLabel(text)
        label.setObjectName("SectionHeader")
        header_layout.addWidget(label)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background-color: #333;")
        line.setFixedHeight(1)
        layout.addWidget(line)

    def add_field(self, grid, row, col, label_text, value_text):
        lbl = QLabel(label_text + ":")
        lbl.setStyleSheet("color: #aaa;")
        val = QLabel(str(value_text))
        val.setObjectName("ValueLabel")
        grid.addWidget(lbl, row, col * 2)
        grid.addWidget(val, row, col * 2 + 1)
