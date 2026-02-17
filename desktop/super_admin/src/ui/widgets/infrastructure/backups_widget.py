from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QPushButton, QHBoxLayout, QMessageBox, QFrame, QComboBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QFont
import requests

MONITOR_API = "http://127.0.0.1:8006/api/v1/monitor/dashboard/"
BACKUP_API = "http://127.0.0.1:8006/api/v1/monitor/backup/"

class BackupsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.services = []
        self.init_ui()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(5000)

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # --- Header ---
        header_frame = QFrame()
        header_frame.setStyleSheet("background: #1a1a1a; border-radius: 8px; padding: 10px;")
        header_layout = QHBoxLayout(header_frame)
        
        title = QLabel("Disaster Recovery Console")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: white; border:none;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        self.svc_combo = QComboBox()
        self.svc_combo.setFixedWidth(200)
        self.svc_combo.setStyleSheet("""
            QComboBox { background: #333; color: white; border: 1px solid #555; padding: 5px; border-radius: 4px; }
            QComboBox::drop-down { border: none; }
        """)
        header_layout.addWidget(self.svc_combo)
        
        btn = QPushButton("Create New Snapshot")
        btn.setStyleSheet("""
            QPushButton { background: #05B8CC; color: white; padding: 8px 15px; font-weight: bold; border-radius: 4px; border: none; }
            QPushButton:hover { background: #04abcd; }
        """)
        btn.clicked.connect(self.trigger_backup)
        header_layout.addWidget(btn)
        
        layout.addWidget(header_frame)
        
        # --- Table ---
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Service", "Snapshot File", "Size", "Last Created", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed) # Actions fixed
        self.table.setColumnWidth(4, 120)
        self.table.verticalHeader().setVisible(False)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.table.setStyleSheet("""
            QTableWidget { background-color: #151515; color: white; border: none; gridline-color: #333; }
            QHeaderView::section { background-color: #222; color: #aaa; padding: 8px; border: none; font-weight: bold; text-align: left; }
            QTableWidget::item { padding: 8px; border-bottom: 1px solid #222; }
        """)
        layout.addWidget(self.table)

    def refresh(self):
        try:
            resp = requests.get(MONITOR_API, timeout=1)
            if resp.status_code == 200:
                nodes = resp.json().get('nodes', [])
                self.services = [n['id'] for n in nodes]
                
                # Update Combo
                current = self.svc_combo.currentText()
                if self.svc_combo.count() == 0:
                    self.svc_combo.addItems(self.services)
                
                self.update_table(nodes)
        except:
            pass

    def update_table(self, nodes):
        # Determine valid rows (services with backups)
        rows_data = []
        for node in nodes:
            bk = node.get('backup', {})
            if bk.get('last_snapshot') and bk.get('last_snapshot') != "No backups yet":
                 rows_data.append(node)
        
        self.table.setRowCount(len(rows_data))
        
        for i, node in enumerate(rows_data):
            bk = node.get('backup', {})
            
            # Service
            self.table.setItem(i, 0, QTableWidgetItem(node['id']))
            
            # File
            fname = bk.get('file', 'Unknown')
            self.table.setItem(i, 1, QTableWidgetItem(fname))
            
            # Size
            size_mb = bk.get('size_mb', 0)
            self.table.setItem(i, 2, QTableWidgetItem(f"{size_mb} MB"))
            
            # Time
            time_str = bk.get('last_snapshot', '--')
            item_t = QTableWidgetItem(time_str)
            item_t.setForeground(QColor("#888"))
            self.table.setItem(i, 3, item_t)
            
            # Actions
            btn_restore = QPushButton("Restore")
            btn_restore.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_restore.setStyleSheet("""
                QPushButton { background: #333; color: white; border: 1px solid #444; border-radius: 3px; }
                QPushButton:hover { background: #444; border: 1px solid #666; }
            """)
            btn_restore.clicked.connect(lambda _, n=node['id']: self.restore(n))
            
            # Cell Widget for layout
            w = QWidget()
            h = QHBoxLayout(w)
            h.setContentsMargins(0,0,0,0)
            h.addWidget(btn_restore)
            self.table.setCellWidget(i, 4, w)

    def trigger_backup(self):
        svc = self.svc_combo.currentText()
        if not svc: return
            
        try:
            resp = requests.post(BACKUP_API, json={'service_name': svc}, timeout=5)
            if resp.status_code == 200:
                res = resp.json()
                if res.get('success'):
                    QMessageBox.information(self, "Success", f"Snapshot Created!\n{res.get('message')}")
                    self.refresh()
                else:
                    QMessageBox.warning(self, "Failed", f"Backup failed: {res.get('message')}")
        except Exception as e:
             QMessageBox.critical(self, "Error", str(e))

    def restore(self, service_name):
        QMessageBox.warning(self, "Restore", f"Restore functionality requires stopping the service first.\n(Simulation: Overwrite {service_name} DB).")
