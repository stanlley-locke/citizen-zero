from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout, QScrollArea)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor
import requests

MONITOR_API = "http://127.0.0.1:8006/api/v1/monitor/dashboard/"

class SmartServiceCard(QFrame):
    def __init__(self, name):
        super().__init__()
        self.setStyleSheet("""
            QFrame { background-color: #202020; border-radius: 10px; border: 1px solid #333; }
            QFrame:hover { border: 1px solid #05B8CC; }
        """)
        self.setFixedSize(260, 160)
        
        layout = QVBoxLayout(self)
        
        # Header
        top = QHBoxLayout()
        lbl = QLabel(name)
        lbl.setStyleSheet("color: white; font-weight: bold; font-size: 14px; border: none;")
        top.addWidget(lbl)
        
        self.status_dot = QLabel("●")
        self.status_dot.setStyleSheet("color: #444; font-size: 16px; border: none;")
        top.addStretch()
        top.addWidget(self.status_dot)
        layout.addLayout(top)
        
        layout.addSpacing(10)
        
        # Metrics
        self.lat_lbl = QLabel("Latency: -- ms", styleSheet="color: #ccc; border: none;")
        layout.addWidget(self.lat_lbl)
        
        self.req_lbl = QLabel("Traffic: 0 reqs", styleSheet="color: #ccc; border: none;")
        layout.addWidget(self.req_lbl)
        
        self.err_lbl = QLabel("Health: Unknown", styleSheet="color: #666; font-style: italic; border: none;")
        layout.addWidget(self.err_lbl)
        
        layout.addStretch()

    def update_data(self, node):
        status = node.get('status', 'offline')
        color = "#00ff00" if status == 'online' else "#ff0000"
        self.status_dot.setStyleSheet(f"color: {color}; font-size: 16px; border: none;")
        
        self.lat_lbl.setText(f"Latency: {node.get('latency', 0)} ms")
        
        metrics = node.get('metrics', {})
        self.req_lbl.setText(f"Traffic: {metrics.get('total_requests', 0)} reqs")
        
        errs = metrics.get('error_count', 0)
        if status == 'online':
            self.err_lbl.setText("Health: Excellent" if errs == 0 else "Health: Degraded")
            self.err_lbl.setStyleSheet("color: #0f0; border: none;" if errs == 0 else "color: #ffbb33; border: none;")
        else:
            self.err_lbl.setText("Health: Critical")
            self.err_lbl.setStyleSheet("color: #f00; border: none;")

class MicroservicesWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.cards = {}
        self.init_ui()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(1500)

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Services Registry", styleSheet="font-size: 22px; font-weight: bold; color: white; margin-bottom: 15px;"))
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")
        
        content = QWidget()
        self.grid = QGridLayout(content)
        self.grid.setSpacing(15)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        scroll.setWidget(content)
        layout.addWidget(scroll)

    def refresh(self):
        try:
            resp = requests.get(MONITOR_API, timeout=1)
            if resp.status_code == 200:
                nodes = resp.json().get('nodes', [])
                
                for i, node in enumerate(nodes):
                    name = node['id']
                    if name not in self.cards:
                        card = SmartServiceCard(name)
                        self.cards[name] = card
                        row = i // 3
                        col = i % 3
                        self.grid.addWidget(card, row, col)
                    
                    self.cards[name].update_data(node)
        except:
            pass
