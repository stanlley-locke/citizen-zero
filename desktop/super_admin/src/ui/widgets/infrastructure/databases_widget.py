from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame, QGridLayout, QProgressBar)
from PyQt6.QtCore import Qt, QTimer
import requests

MONITOR_API = "http://127.0.0.1:8006/api/v1/monitor/dashboard/"

class DBStatusCard(QFrame):
    def __init__(self, name):
        super().__init__()
        self.setStyleSheet("background-color: #1a1a1a; border: 1px solid #333; border-radius: 8px;")
        self.setFixedSize(300, 150)
        
        layout = QVBoxLayout(self)
        
        # Header
        top = QLabel(f"DB: {name}")
        top.setStyleSheet("color: #05B8CC; font-weight: bold; font-size: 14px; border: none;")
        layout.addWidget(top)
        
        self.status_lbl = QLabel("Status: Checking...")
        self.status_lbl.setStyleSheet("color: #888; border: none;")
        layout.addWidget(self.status_lbl)
        
        self.size_lbl = QLabel("Size on Disk: --")
        self.size_lbl.setStyleSheet("color: white; font-weight: bold; font-size: 12px; border: none;")
        layout.addWidget(self.size_lbl)
        
        self.engine_lbl = QLabel("Engine: --")
        self.engine_lbl.setStyleSheet("color: #666; border: none;")
        layout.addWidget(self.engine_lbl)
        
        layout.addStretch()

    def update(self, db_data):
        st = db_data.get('status', 'Unknown')
        color = "#0f0" if st == "Healthy" else "#f00"
        self.status_lbl.setText(f"Connection: {st}")
        self.status_lbl.setStyleSheet(f"color: {color}; border: none;")
        
        self.size_lbl.setText(f"Size on Disk: {db_data.get('size', 'N/A')}")
        self.engine_lbl.setText(f"Engine: {db_data.get('engine', 'Unknown')}")

class DatabasesWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.cards = {}
        self.init_ui()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(2000)

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Database Persistence Layer", styleSheet="font-size: 22px; font-weight: bold; color: white; margin-bottom: 20px;"))
        
        self.content = QWidget()
        self.grid = QGridLayout(self.content)
        self.grid.setSpacing(20)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        layout.addWidget(self.content)
        layout.addStretch()

    def refresh(self):
        try:
            resp = requests.get(MONITOR_API, timeout=1)
            if resp.status_code == 200:
                nodes = resp.json().get('nodes', [])
                
                for i, node in enumerate(nodes):
                    name = node['id']
                    db_data = node.get('database')
                    if name not in self.cards:
                        card = DBStatusCard(name)
                        self.cards[name] = card
                        row = i // 2
                        col = i % 2
                        self.grid.addWidget(card, row, col)
                    
                    if db_data:
                        self.cards[name].update(db_data)
        except:
            pass
