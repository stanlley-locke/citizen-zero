from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QFrame, QGridLayout, QScrollArea)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QFont
import requests

MONITOR_API = "http://127.0.0.1:8006/api/v1/monitor/dashboard/"

class ResourceCard(QFrame):
    def __init__(self, title, subtitle_template, color):
        super().__init__()
        self.subtitle_template = subtitle_template # e.g. "Hosting: Auth\nIP: {ip}"
        self.setStyleSheet(f"""
            QFrame {{ background-color: #151515; border-radius: 8px; border: 1px solid #333; }}
        """) 
        
        layout = QVBoxLayout(self)
        
        # Header Strip
        strip = QFrame()
        strip.setFixedHeight(4)
        strip.setStyleSheet(f"background-color: {color}; border-radius: 2px;")
        layout.addWidget(strip)
        
        # Title
        lbl = QLabel(title)
        lbl.setStyleSheet("color: white; font-weight: bold; font-size: 16px; border: none;")
        layout.addWidget(lbl)
        
        self.sub = QLabel(subtitle_template.format(ip="..."))
        self.sub.setStyleSheet("color: #888; font-size: 12px; border: none;")
        layout.addWidget(self.sub)
        
        layout.addSpacing(10)
        
        # Metrics
        self.cpu_bar = self.add_metric(layout, "CPU Load", color)
        self.ram_bar = self.add_metric(layout, "RAM Usage", color)
        self.disk_bar = self.add_metric(layout, "Disk I/O", color)
        
        layout.addStretch()
        
    def add_metric(self, parent, name, color):
        v = QVBoxLayout()
        h = QHBoxLayout()
        h.addWidget(QLabel(name, styleSheet="color: #ccc; border: none;"))
        val = QLabel("0%", styleSheet="color: white; font-weight: bold; border: none;")
        h.addStretch()
        h.addWidget(val)
        v.addLayout(h)
        
        bar = QProgressBar()
        bar.setFixedHeight(8)
        bar.setTextVisible(False)
        bar.setStyleSheet(f"""
            QProgressBar {{ background: #222; border-radius: 4px; border: none; }}
            QProgressBar::chunk {{ background: {color}; border-radius: 4px; }}
        """)
        v.addWidget(bar)
        parent.addLayout(v)
        parent.addSpacing(8)
        return {'bar': bar, 'val': val}

    def update(self, res):
        # Update IP Label
        real_ip = res.get('ip', 'Unknown')
        self.sub.setText(self.subtitle_template.format(ip=real_ip))

        # Update Bars
        self.cpu_bar['bar'].setValue(int(float(res.get('cpu', 0))))
        self.cpu_bar['val'].setText(f"{res.get('cpu', 0)}%")
        
        self.ram_bar['bar'].setValue(int(float(res.get('ram', 0))))
        self.ram_bar['val'].setText(f"{res.get('ram', 0)}%")
        
        self.disk_bar['bar'].setValue(int(float(res.get('disk', 0))))
        self.disk_bar['val'].setText(f"{res.get('disk', 0)}%")

class NodesWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.cards = {}
        self.init_ui()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(2000)

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        header = QLabel("Cluster Infrastructure Resources")
        header.setStyleSheet("color: white; font-size: 22px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(header)
        
        # Card Container
        grid = QHBoxLayout()
        grid.setSpacing(20)
        
        # 1. Core Master
        self.core = ResourceCard("Core Master Node", "Hosting: Auth, ID Service\nIP: {ip}", "#05B8CC")
        grid.addWidget(self.core)
        
        # 2. Security Cluster
        self.sec = ResourceCard("Security Cluster", "Hosting: Verify, Audit\nIP: {ip}", "#bb86fc")
        grid.addWidget(self.sec)
        
        # 3. Edge Gateway
        self.edge = ResourceCard("Edge Gateway", "Hosting: IPRS Interface\nIP: {ip}", "#ff9800")
        grid.addWidget(self.edge)
        
        layout.addLayout(grid)
        layout.addStretch()

    def refresh(self):
        try:
            resp = requests.get(MONITOR_API, timeout=1)
            if resp.status_code == 200:
                data = resp.json()
                nodes = data.get('nodes', [])
                
                # Fetch Real System Stats from ANY node (since they are all localhost)
                real_res = {'cpu': 0, 'ram': 0, 'disk': 0, 'ip': 'Checking...'}
                if nodes:
                    real_res = nodes[0].get('resources', real_res)

                # Update all cards with the REAL host data
                self.core.update(real_res)
                self.sec.update(real_res)
                self.edge.update(real_res)
        except:
            pass
