from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QProgressBar, QFrame, QMessageBox, QComboBox, QLineEdit)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QPixmap, QColor
import qtawesome as qta
import requests
from app_config import Endpoints
from ui.dialogs.citizen_detail_dialog import CitizenDetailDialog
class BiometricWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        title = QLabel("Biometric Enrollment & Verification")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        layout.addWidget(title)
        
        # Main Content Area - Split View
        content_layout = QHBoxLayout()
        
        # Left Panel - Enrollment Controls
        left_panel = QFrame()
        left_panel.setStyleSheet("background-color: #252525; border-radius: 10px; border: 1px solid #3d3d3d;")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(20)
        left_layout.setContentsMargins(20, 20, 20, 20)
        
        lbl_instr = QLabel("Select Citizen & Biometric Type to Enroll")
        lbl_instr.setStyleSheet("color: #aaa; font-size: 14px;")
        left_layout.addWidget(lbl_instr)
        
        # Search Citizen
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search Citizen (ID or Name)...")
        self.search_input.setStyleSheet("""
            QLineEdit { padding: 10px; background: #333; color: white; border: 1px solid #444; border-radius: 5px; }
            QLineEdit:focus { border: 1px solid #0088cc; }
        """)
        self.search_input.textChanged.connect(self.on_search_text_changed)
        left_layout.addWidget(self.search_input)
        
        # Debounce timer
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.setInterval(500)
        self.search_timer.timeout.connect(self.perform_search)
        
        # Citizen Selector
        self.citizen_combo = QComboBox()
        self.citizen_combo.addItem("Select Citizen...")
        self.citizen_combo.setStyleSheet("""
            QComboBox { padding: 10px; background: #333; color: white; border: 1px solid #444; border-radius: 5px; }
            QComboBox::drop-down { border: none; }
        """)
        left_layout.addWidget(self.citizen_combo)
        
        # Load citizens for combo (Initial load)
        self.load_citizens()
        
        # Biometric Type
        self.bio_type_combo = QComboBox()
        self.bio_type_combo.addItems(["Fingerprint (Right Thumb)", "Fingerprint (Left Thumb)", "Face Scan", "Iris Scan"])
        self.bio_type_combo.setStyleSheet(self.citizen_combo.styleSheet())
        left_layout.addWidget(self.bio_type_combo)
        
        # Start Button
        self.btn_capture = QPushButton("Start Capture")
        self.btn_capture.setIcon(qta.icon('fa5s.camera', color='white'))
        self.btn_capture.setStyleSheet("""
            QPushButton { background-color: #0088cc; color: white; padding: 15px; border-radius: 5px; font-weight: bold; font-size: 14px; }
            QPushButton:hover { background-color: #0099dd; }
            QPushButton:disabled { background-color: #555; color: #888; }
        """)
        self.btn_capture.clicked.connect(self.start_capture)
        left_layout.addWidget(self.btn_capture)
        
        left_layout.addStretch()
        content_layout.addWidget(left_panel, 1) # Stretch factor 1
        
        # Right Panel - Visualization
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: #1a1a1a; border-radius: 10px; border: 2px dashed #444;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.visual_label = QLabel()
        self.visual_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_default = qta.icon('fa5s.fingerprint', color='#333')
        self.visual_label.setPixmap(self.icon_default.pixmap(128, 128))
        right_layout.addWidget(self.visual_label)
        
        self.status_label = QLabel("Ready for Capture")
        self.status_label.setStyleSheet("color: #666; font-size: 16px; margin-top: 10px;")
        right_layout.addWidget(self.status_label)
        
        self.progress = QProgressBar()
        self.progress.setStyleSheet("""
            QProgressBar { background: #333; border-radius: 5px; text-align: center; color: white; height: 10px; }
            QProgressBar::chunk { background-color: #00ff00; border-radius: 5px; }
        """)
        self.progress.setValue(0)
        self.progress.hide()
        right_layout.addWidget(self.progress)
        
        content_layout.addWidget(right_panel, 2) # Stretch factor 2
        
        layout.addLayout(content_layout)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.capture_step = 0

    def start_capture(self):
        if self.citizen_combo.currentIndex() == 0:
            QMessageBox.warning(self, "Selection Required", "Please select a citizen first.")
            return
            
        self.btn_capture.setEnabled(False)
        self.citizen_combo.setEnabled(False)
        self.search_input.setEnabled(False)
        self.progress.setValue(0)
        self.progress.show()
        self.capture_step = 0
        self.status_label.setText("Initializing Scanner...")
        self.status_label.setStyleSheet("color: #0088cc;")
        
        # Animate Icon
        self.icon_active = qta.icon('fa5s.fingerprint', color='#0088cc')
        self.visual_label.setPixmap(self.icon_active.pixmap(128, 128))
        
        self.timer.start(100) # 100ms interval

    def update_progress(self):
        self.capture_step += 2
        self.progress.setValue(self.capture_step)
        
        if self.capture_step < 30:
            self.status_label.setText("Scanning...")
        elif self.capture_step < 70:
             self.status_label.setText("Processing Biometric Data...")
        elif self.capture_step < 90:
             self.status_label.setText("Encrypting & Uploading...")
             
        if self.capture_step >= 100:
            self.timer.stop()
            self.finish_capture()

    def finish_capture(self):
        self.status_label.setText("Enrollment Successful!")
        self.status_label.setStyleSheet("color: #00ff00; font-weight: bold;")
        self.icon_success = qta.icon('fa5s.check-circle', color='#00ff00')
        self.visual_label.setPixmap(self.icon_success.pixmap(128, 128))
        
        self.btn_capture.setEnabled(True)
        self.citizen_combo.setEnabled(True)
        self.search_input.setEnabled(True)
        self.btn_capture.setText("Capture Another")
        
        # Simulate Backend Call
        # requests.post(..., json={'biometric_data': 'encrypted_blob'})
        print("Mock Biometric Data 'Uploaded' to ID Service")

    def on_search_text_changed(self, text):
        self.search_timer.start()

    def perform_search(self):
        text = self.search_input.text().strip()
        self.load_citizens(search_query=text)

    def load_citizens(self, search_query=None):
        try:
            # Fetch a reasonable number of citizens for the dropdown
            url = f"{Endpoints.CITIZENS}?page_size=20"
            print(f"Fetching Citizens from: {url}")
            if search_query:
                url += f"&search={search_query}"
                
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                citizens = data.get('results', []) if isinstance(data, dict) else data
                
                self.citizen_combo.clear()
                self.citizen_combo.addItem("Select Citizen...")
                
                for citizen in citizens:
                    label = f"{citizen.get('national_id')} - {citizen.get('first_name')} {citizen.get('last_name')}"
                    # Store ID as user data
                    self.citizen_combo.addItem(label, citizen.get('national_id'))
            else:
                print("Failed to load citizens for biometrics.")
        except Exception as e:
            print(f"Error loading citizens: {e}")
