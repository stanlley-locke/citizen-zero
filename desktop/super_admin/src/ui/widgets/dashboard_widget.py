from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, 
                             QGridLayout, QScrollArea, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont
import requests
from app_config import Endpoints
import qtawesome as qta
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Circle
import random
import requests

class StatCard(QFrame):
    def __init__(self, title, value, icon, color, change="+0%"):
        super().__init__()
        self.setStyleSheet(f"""
            QFrame {{
                background-color: #252525;
                border-radius: 8px;
                border: 1px solid #3d3d3d;
            }}
            QFrame:hover {{
                border: 1px solid {color};
            }}
        """)
        self.setFixedSize(240, 120)
        
        layout = QVBoxLayout(self)
        
        header_layout = QHBoxLayout()
        icon_label = QLabel()
        icon_label.setPixmap(qta.icon(icon, color=color).pixmap(24, 24))
        icon_label.setStyleSheet("border: none; background: transparent;")
        
        title_label = QLabel(title.upper())
        title_label.setStyleSheet("color: #aaa; font-size: 11px; font-weight: bold; border: none; background: transparent;")
        
        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        self.value_label = QLabel(value)
        self.value_label.setStyleSheet("color: white; font-size: 28px; font-weight: bold; border: none; background: transparent;")
        
        change_label = QLabel(f"{change} from last week")
        change_col = "#00ff00" if "+" in change else "#ff0000"
        change_label.setStyleSheet(f"color: {change_col}; font-size: 11px; border: none; background: transparent;")
        
        layout.addLayout(header_layout)
        layout.addWidget(self.value_label)
        layout.addWidget(change_label)

class DashboardWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        # Scroll Area for the whole dashboard
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setContentsMargins(30, 30, 30, 30)
        self.content_layout.setSpacing(20)
        
        # 1. Header
        header = QLabel("Executive Overview")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        self.content_layout.addWidget(header)
        
        # 2. Stats Row
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(15)
        
        self.citizens_card = StatCard("Total Citizens", "12,450", "fa5s.users", "#0088cc", "+12%")
        self.ids_card = StatCard("IDs Issued", "Loading...", "fa5s.id-card", "#006600", "+5%")
        self.pending_card = StatCard("Pending Verifications", "Loading...", "fa5s.hourglass-half", "#ffa500", "-2%")
        self.alerts_card = StatCard("System Alerts", "3", "fa5s.bell", "#BB0000", "+1")
        
        stats_layout.addWidget(self.citizens_card)
        stats_layout.addWidget(self.ids_card)
        stats_layout.addWidget(self.pending_card)
        stats_layout.addWidget(self.alerts_card)
        stats_layout.addStretch()
        
        self.content_layout.addLayout(stats_layout)
        
        # 3. Charts Row
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(20)
        
        # Chart 1: Registration Trend
        chart1_frame = QFrame()
        chart1_frame.setStyleSheet("background-color: #252525; border-radius: 8px; border: 1px solid #3d3d3d;")
        chart1_frame.setMinimumHeight(350)
        chart1_layout = QVBoxLayout(chart1_frame)
        chart1_title = QLabel("Registration Growth (Last 6 Months)")
        chart1_title.setStyleSheet("color: white; font-weight: bold; border: none;")
        chart1_layout.addWidget(chart1_title)
        
        self.trend_canvas = FigureCanvas(Figure(facecolor='#252525'))
        self.plot_growth_chart()
        chart1_layout.addWidget(self.trend_canvas)
        
        charts_layout.addWidget(chart1_frame, 2) # Stretch factor 2
        
        # Chart 2: Demographics (Pie)
        chart2_frame = QFrame()
        chart2_frame.setStyleSheet("background-color: #252525; border-radius: 8px; border: 1px solid #3d3d3d;")
        chart2_frame.setMinimumHeight(350)
        chart2_layout = QVBoxLayout(chart2_frame)
        chart2_title = QLabel("Demographics Breakdown")
        chart2_title.setStyleSheet("color: white; font-weight: bold; border: none;")
        chart2_layout.addWidget(chart2_title)
        
        self.pie_canvas = FigureCanvas(Figure(facecolor='#252525'))
        self.plot_demographics_chart()
        chart2_layout.addWidget(self.pie_canvas)
        
        charts_layout.addWidget(chart2_frame, 1) # Stretch factor 1
        
        self.content_layout.addLayout(charts_layout)
        
        # 4. Recent Activity Table
        activity_label = QLabel("Recent System Activity")
        activity_label.setStyleSheet("font-size: 18px; font-weight: bold; color: white; margin-top: 10px;")
        self.content_layout.addWidget(activity_label)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Timestamp", "User", "Action", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #252525;
                gridline-color: #3d3d3d;
                border: 1px solid #3d3d3d;
                color: #ddd;
            }
            QHeaderView::section {
                background-color: #333;
                color: white;
                padding: 5px;
                border: 1px solid #3d3d3d;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        self.populate_dummy_data()
        self.table.setFixedHeight(250)
        self.content_layout.addWidget(self.table)
        
        self.content_layout.addStretch()
        
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

    def plot_growth_chart(self):
        ax = self.trend_canvas.figure.add_subplot(111)
        ax.set_facecolor('#252525')
        
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        registrations = [1200, 1500, 1400, 1800, 2100, 2450]
        
        ax.plot(months, registrations, color='#0088cc', marker='o', linewidth=2)
        ax.grid(color='#444', linestyle='--', linewidth=0.5)
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.spines['bottom'].set_color('#555')
        ax.spines['top'].set_color('none') 
        ax.spines['left'].set_color('#555')
        ax.spines['right'].set_color('none')

    def plot_demographics_chart(self):
        ax = self.pie_canvas.figure.add_subplot(111)
        ax.set_facecolor('#252525')
        
        sizes = [45, 30, 15, 10]
        labels = ['Nairobi', 'Mombasa', 'Kisumu', 'Others']
        colors = ['#0088cc', '#006600', '#ffa500', '#bb0000']
        
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', 
                                          startangle=90, colors=colors, textprops=dict(color="white"))
        
        # Make it a donut
        centre_circle = Circle((0,0),0.70,fc='#252525')
        self.pie_canvas.figure.gca().add_artist(centre_circle)

    def load_data(self):
        """Fetch real data from backend services"""
        # We can use a thread here, but for now let's just do it directly to prove integration
        # Real apps should use the Worker pattern implemented in utils/workers.py
        
        # 1. Fetch Audit Logs for Activity
        try:
            url = Endpoints.AUDIT_LOGS
            print(f"Fetching Audit Logs from: {url}")
            response = requests.get(url)
            print(f"Audit Logs Response: {response.status_code}")
            if response.status_code == 200:
                logs = response.json()
                print(f"Loaded {len(logs)} audit logs")
                self.update_activity_table(logs)
            else:
                print(f"Failed to fetch logs: {response.text}")
        except Exception as e:
            print(f"Error fetching audit logs: {e}")

        # 2. Fetch Issued IDs Count
        try:
            # ID Service running
            response = requests.get(Endpoints.DIGITAL_IDS)
            if response.status_code == 200:
                ids = response.json()
                self.ids_card.value_label.setText(str(len(ids)))
        except Exception as e:
            print(f"Error fetching IDs: {e}")

        # 3. Fetch Pending Requests
        try:
            # ID Service requests
            response = requests.get(Endpoints.REQUESTS)
            if response.status_code == 200:
                reqs = response.json()
                self.pending_card.value_label.setText(str(len(reqs)))
        except Exception as e:
            print(f"Error fetching requests: {e}")

        # 4. Fetch Total Citizens (IPRS Mock)
        try:
            response = requests.get(Endpoints.CITIZENS)
            if response.status_code == 200:
                citizens = response.json()
                # If pagination is enabled, DRF might return {'count': X, 'results': [...]}. 
                # Checking structure:
                if isinstance(citizens, dict) and 'count' in citizens:
                     count = citizens['count']
                else:
                     count = len(citizens)
                
                self.citizens_card.value_label.setText(f"{count:,}") # Format with commas
        except Exception as e:
            print(f"Error fetching citizens: {e}")

    def update_activity_table(self, logs):
        # Sort logs by timestamp desc if not already
        # logs.sort(key=lambda x: x['timestamp'], reverse=True)
        
        self.table.setRowCount(len(logs))
        for i, log in enumerate(logs):
            # Parse timestamp for display?
            time_str = log.get('timestamp', 'N/A')
            user_str = str(log.get('user', 'System'))
            action_str = log.get('action', 'Unknown')
            details_str = log.get('details', '')
            
            self.table.setItem(i, 0, QTableWidgetItem(time_str))
            self.table.setItem(i, 1, QTableWidgetItem(user_str))
            self.table.setItem(i, 2, QTableWidgetItem(f"{action_str} - {details_str}"))
            
            # Mock status for now as AuditLog might not have it explicitly
            status = "Success" 
            status_item = QTableWidgetItem(status)
            status_item.setForeground(QColor("#00ff00"))
            self.table.setItem(i, 3, status_item)

    def populate_dummy_data(self):
        # Initial dummy data, then load real
        data = [
            ("Loading...", "...", "Connecting to backend...", "...")
        ]
        self.table.setRowCount(len(data))
        for i, (time, user, action, status) in enumerate(data):
            self.table.setItem(i, 0, QTableWidgetItem(time))
            self.table.setItem(i, 1, QTableWidgetItem(user))
            self.table.setItem(i, 2, QTableWidgetItem(action))
            self.table.setItem(i, 3, QTableWidgetItem(status))
            
        # Trigger load
        # Use QTimer to delay slightly so UI shows up first
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(1000, self.load_data)
