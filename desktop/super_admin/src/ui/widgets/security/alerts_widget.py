from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QScrollArea, QFrame, QPushButton, QGridLayout)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor
import requests
import qtawesome as qta
from app_config import Endpoints

class AlertsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_alerts()
        
        # Poll every 30 seconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.load_alerts)
        self.timer.start(30000)

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        header = QHBoxLayout()
        title = QLabel("Security Alerts")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setIcon(qta.icon('fa5s.sync-alt', color='black'))
        refresh_btn.clicked.connect(self.load_alerts)
        
        header.addWidget(title)
        header.addStretch()
        header.addWidget(refresh_btn)
        layout.addLayout(header)

        # Alerts Area (Scrollable)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        self.alerts_container = QWidget()
        self.alerts_layout = QVBoxLayout(self.alerts_container)
        self.alerts_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        scroll.setWidget(self.alerts_container)
        layout.addWidget(scroll)

    def load_alerts(self):
        try:
            # We created the /alerts/ action on the AuditLogViewSet
            # URL should be .../audit/logs/alerts/
            # But Endpoints.AUDIT_LOGS is .../audit/logs/
            url = f"{Endpoints.AUDIT_LOGS}alerts/"
            
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                self.display_alerts(response.json())
            else:
                print(f"Failed to fetch alerts: {response.text}")
        except Exception as e:
            print(f"Error loading alerts: {e}")

    def display_alerts(self, alerts):
        # Clear existing
        for i in reversed(range(self.alerts_layout.count())): 
            self.alerts_layout.itemAt(i).widget().setParent(None)

        if not alerts:
            lbl = QLabel("No active security alerts in the last 24 hours.")
            lbl.setStyleSheet("color: #888; font-size: 14px; margin-top: 20px;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.alerts_layout.addWidget(lbl)
            return

        for alert in alerts:
            card = self.create_alert_card(alert)
            self.alerts_layout.addWidget(card)

    def create_alert_card(self, alert):
        frame = QFrame()
        frame.setObjectName("AlertCard")
        # Style depending on severity
        severity = alert.get('severity', 'WARNING')
        border_color = "#ff4444" if severity == 'CRITICAL' else "#ffbb33"
        bg_color = "#3a1c1c" if severity == 'CRITICAL' else "#3a2e1c"
        
        frame.setStyleSheet(f"""
            QFrame#AlertCard {{
                background-color: {bg_color};
                border-left: 5px solid {border_color};
                border-radius: 4px;
                padding: 10px;
                margin-bottom: 10px;
            }}
            QLabel {{ color: #ddd; }}
        """)
        
        layout = QGridLayout(frame)
        
        # Icon
        icon_name = 'fa5s.exclamation-circle' if severity == 'CRITICAL' else 'fa5s.exclamation-triangle'
        icon_lbl = QLabel()
        icon_lbl.setPixmap(qta.icon(icon_name, color=border_color).pixmap(32, 32))
        layout.addWidget(icon_lbl, 0, 0, 2, 1)
        
        # Title (Action)
        action_lbl = QLabel(alert.get('action', 'UNKNOWN'))
        action_lbl.setStyleSheet("font-weight: bold; font-size: 16px; color: white;")
        layout.addWidget(action_lbl, 0, 1)
        
        # Timestamp
        time_lbl = QLabel(str(alert.get('timestamp', '')[:19]))
        time_lbl.setStyleSheet("color: #aaa;")
        layout.addWidget(time_lbl, 0, 2, alignment=Qt.AlignmentFlag.AlignRight)
        
        # Details
        details_lbl = QLabel(alert.get('details', 'No details provided.'))
        details_lbl.setWordWrap(True)
        layout.addWidget(details_lbl, 1, 1, 1, 2)
        
        # Footer (Actor)
        username = alert.get('username') or alert.get('user_id')
        actor_lbl = QLabel(f"Actor: {username} ({alert.get('actor_type', 'SYSTEM')})")
        actor_lbl.setStyleSheet("font-style: italic; color: #888; margin-top: 5px;")
        layout.addWidget(actor_lbl, 2, 1, 1, 2)
        
        return frame
