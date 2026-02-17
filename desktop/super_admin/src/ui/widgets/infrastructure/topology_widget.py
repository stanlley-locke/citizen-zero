from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QGraphicsView, QGraphicsScene, QGraphicsRectItem, 
                             QGraphicsTextItem, QGraphicsItem, QPushButton, QGraphicsPathItem, QMenu, QGraphicsLineItem,
                             QScrollArea, QFrame, QTextEdit, QSplitter)
from PyQt6.QtCore import Qt, QTimer, QRectF, QPointF, pyqtSignal, QPropertyAnimation, QObject, QLineF
from PyQt6.QtGui import QBrush, QPen, QColor, QFont, QPainter, QRadialGradient, QLinearGradient
import requests
import random
import datetime

# --- Config ---
MONITOR_API = "http://127.0.0.1:8006/api/v1/monitor/dashboard/"

# --- Graphics Items ---

class ConnectionCable(QGraphicsLineItem):
    """Visual connection between nodes"""
    def __init__(self, start_item, end_item, dashed=False):
        super().__init__()
        self.start_item = start_item
        self.end_item = end_item
        self.dashed = dashed
        
        pen = QPen(QColor("#444"), 2)
        if dashed:
            pen.setStyle(Qt.PenStyle.DashLine)
        self.setPen(pen)
        self.setZValue(-1)
        self.update_position()

    def update_position(self):
        start = self.start_item.sceneBoundingRect().center()
        end = self.end_item.sceneBoundingRect().center()
        self.setLine(QLineF(start, end))

class MonitorNodeItem(QGraphicsRectItem):
    """The Central Monitor Service Node"""
    def __init__(self, x, y):
        super().__init__(0, 0, 140, 140)
        self.setPos(x, y)
        self.setBrush(QBrush(QColor("#004488"))) # Blue Hub
        self.setPen(QPen(QColor("#0088ff"), 2))
        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsMovable | QGraphicsItem.GraphicsItemFlag.ItemIsSelectable | QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        
        # Label
        self.text = QGraphicsTextItem("OBSERVABILITY\nHUB", self)
        self.text.setDefaultTextColor(Qt.GlobalColor.white)
        self.text.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.text.setPos(15, 50)
        
        self.pulse = 0
        
    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            if self.scene():
                self.scene().update_cables()
        return super().itemChange(change, value)
        
    def paint(self, painter, option, widget):
        painter.setBrush(self.brush())
        painter.setPen(self.pen())
        painter.drawEllipse(self.rect()) # Draw as Circle
        
        if self.pulse > 0:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(0, 136, 255, 150), 3))
            painter.drawEllipse(self.rect().adjusted(-self.pulse, -self.pulse, self.pulse, self.pulse))
            self.pulse -= 2
            if self.pulse < 0: self.pulse = 0

    def trigger_pulse(self):
        self.pulse = 30
        self.update()

class ServiceCardItem(QGraphicsRectItem):
    """Microservice Display Card"""
    def __init__(self, name, x, y, widget_ref):
        super().__init__(0, 0, 220, 100)
        self.name = name
        self.widget_ref = widget_ref
        self.setPos(x, y)
        
        # Background
        grad = QLinearGradient(0, 0, 220, 100)
        grad.setColorAt(0, QColor("#222"))
        grad.setColorAt(1, QColor("#111"))
        self.setBrush(QBrush(grad))
        self.setPen(QPen(QColor("#555"), 2))
        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsMovable | QGraphicsItem.GraphicsItemFlag.ItemIsSelectable | QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        
        # Name
        self.name_text = QGraphicsTextItem(name, self)
        self.name_text.setDefaultTextColor(Qt.GlobalColor.white)
        self.name_text.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.name_text.setPos(10, 10)
        
        # Status
        self.status_text = QGraphicsTextItem("Connecting...", self)
        self.status_text.setDefaultTextColor(QColor("#888"))
        self.status_text.setPos(10, 40)
        
        # Latency
        self.lat_text = QGraphicsTextItem("-- ms", self)
        self.lat_text.setDefaultTextColor(QColor("#05B8CC"))
        self.lat_text.setPos(150, 10)
        
        # Traffic Dot
        self.dot_color = QColor("#333")
        
        # Data Cache
        self.latest_logs = []

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
             if self.scene():
                self.scene().update_cables()
        return super().itemChange(change, value)

    def mousePressEvent(self, event):
        self.widget_ref.select_node(self)
        super().mousePressEvent(event)

    def update_data(self, data):
        status = data.get('status', 'offline')
        latency = data.get('latency', 0)
        metrics = data.get('metrics', {})
        self.latest_logs = metrics.get('recent_traffic', [])
        
        # Color
        if status == 'online':
            self.setPen(QPen(QColor("#00ff00"), 2))
            self.status_text.setPlainText(f"ONLINE | {metrics.get('total_requests', 0)} reqs")
            self.status_text.setDefaultTextColor(QColor("#00ff00"))
            self.dot_color = QColor("#00ff00")
        else:
            self.setPen(QPen(QColor("#ff0000"), 2))
            self.status_text.setPlainText(f"OFFLINE")
            self.status_text.setDefaultTextColor(QColor("#ff0000"))
            self.dot_color = QColor("#ff0000")
            
        self.lat_text.setPlainText(f"{latency} ms")
        self.update()

# --- Main Widget ---

class TopologyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.nodes = {}
        self.cables = []
        self.selected_node = None
        self.init_ui()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.fetch_data)
        self.timer.start(1000) # 1 sec refresh
        
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self.scene.advance)
        self.anim_timer.start(50)

    def init_ui(self):
        layout = QHBoxLayout(self) # Changed to HBox for splitter
        
        # Right: Details Panel
        self.create_details_panel()
        
        self.scene = TopologyScene(self)
        self.scene.setBackgroundBrush(QBrush(QColor("#101010")))
        
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.view)
        splitter.addWidget(self.details_container)
        splitter.setSizes([800, 300]) # 800px graph, 300px logs
        
        layout.addWidget(splitter)
        
        self.setup_layout()

    def create_details_panel(self):
        self.details_container = QFrame()
        self.details_container.setStyleSheet("background-color: #1a1a1a; border-left: 1px solid #333;")
        vbox = QVBoxLayout(self.details_container)
        
        lbl = QLabel("Live Request Logs")
        lbl.setStyleSheet("color: white; font-weight: bold; font-size: 14px; margin-bottom: 10px;")
        vbox.addWidget(lbl)
        
        self.node_title = QLabel("Select a Service...")
        self.node_title.setStyleSheet("color: #05B8CC; font-weight: bold;")
        vbox.addWidget(self.node_title)
        
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setStyleSheet("""
            QTextEdit { background-color: #000; color: #0f0; font-family: Consolas; font-size: 11px; border: 1px solid #333; }
        """)
        vbox.addWidget(self.log_view)

    def setup_layout(self):
        # Draw Central Monitor Hub
        cx, cy = 400, 300
        self.hub = MonitorNodeItem(cx - 70, cy - 70)
        self.scene.addItem(self.hub)
        
        # Defined Services (Positions around Hub)
        positions = [
            ("Auth Service", 400, 100),
            ("ID Service", 700, 300),
            ("Verify Service", 400, 500),
            ("Audit Service", 100, 300),
            ("IPRS Mock", 100, 100),
        ]
        
        for name, x, y in positions:
            # Card
            node = ServiceCardItem(name, x, y, self)
            self.scene.addItem(node)
            self.nodes[name] = node
            
            # Cable to Hub
            line = ConnectionCable(self.hub, node, dashed=True)
            self.scene.addItem(line)
            self.cables.append(line)

    def fetch_data(self):
        try:
            self.hub.trigger_pulse() # Visual heartbeat
            resp = requests.get(MONITOR_API, timeout=1)
            if resp.status_code == 200:
                data = resp.json()
                
                # Update Nodes
                for node_data in data.get('nodes', []):
                    name = node_data['id']
                    if name in self.nodes:
                        self.nodes[name].update_data(node_data)
                
                # Refresh logs if node selected
                if self.selected_node:
                    self.update_log_panel()
                        
        except Exception as e:
            pass

    def select_node(self, node_item):
        self.selected_node = node_item
        self.node_title.setText(f"Logs: {node_item.name}")
        self.update_log_panel()

    def update_log_panel(self):
        if not self.selected_node: return
        
        logs = self.selected_node.latest_logs
        if not logs:
            self.log_view.setHtml("<i style='color:#555'>No recent traffic...</i>")
            return
            
        html = ""
        for log in reversed(logs): # Newest first
            ts = datetime.datetime.fromtimestamp(log['timestamp']).strftime('%H:%M:%S')
            method = log['method']
            path = log['path']
            status = log['status']
            color = "#00ff00" if status < 400 else "#ff0000"
            
            html += f"<div style='margin-bottom:2px;'><span style='color:#555'>[{ts}]</span> <b style='color:#fff'>{method}</b> {path} <span style='color:{color}'>{status}</span></div>"
            
        self.log_view.setHtml(html)

class TopologyScene(QGraphicsScene):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        
    def update_cables(self):
        for cable in self.widget.cables:
            cable.update_position()
