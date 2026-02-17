from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QGridLayout, QScrollArea, QWidget)
from PyQt6.QtCore import Qt
import qtawesome as qta

class CitizenDetailDialog(QDialog):
    def __init__(self, citizen_data, parent=None):
        super().__init__(parent)
        self.citizen = citizen_data
        self.setWindowTitle(f"Citizen Details - {self.citizen.get('national_id', 'Unknown')}")
        self.resize(600, 500)
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
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header = QFrame()
        header.setStyleSheet("background-color: #1a1a1a; border-bottom: 1px solid #333;")
        header_layout = QHBoxLayout(header)
        
        icon_label = QLabel()
        icon_label.setPixmap(qta.icon('fa5s.user-circle', color='white').pixmap(32, 32))
        header_layout.addWidget(icon_label)
        
        name_label = QLabel(f"{self.citizen.get('first_name', '')} {self.citizen.get('last_name', '')}".upper())
        name_label.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        header_layout.addWidget(name_label)
        
        header_layout.addStretch()
        layout.addWidget(header)
        
        # Content Scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)
        
        # Personal Info Section
        self.add_section_header(content_layout, "Personal Information", "fa5s.id-card")
        
        info_grid = QGridLayout()
        info_grid.setColumnStretch(1, 1)
        info_grid.setColumnStretch(3, 1)
        
        self.add_field(info_grid, 0, 0, "National ID", self.citizen.get('national_id'))
        self.add_field(info_grid, 0, 2, "Date of Birth", self.citizen.get('date_of_birth'))
        self.add_field(info_grid, 1, 0, "Gender", self.get_gender_str(self.citizen.get('gender')))
        self.add_field(info_grid, 1, 2, "Place of Birth", self.citizen.get('place_of_birth'))
        self.add_field(info_grid, 2, 0, "County", self.citizen.get('county_of_birth'))
        self.add_field(info_grid, 2, 2, "Nationality", "Kenyan") # Mock
        
        content_layout.addLayout(info_grid)
        
        # Contact Info
        self.add_section_header(content_layout, "Contact Information", "fa5s.address-book")
        contact_grid = QGridLayout()
        self.add_field(contact_grid, 0, 0, "Phone Number", self.citizen.get('phone_number') or "N/A")
        self.add_field(contact_grid, 0, 2, "Email", self.citizen.get('email') or "N/A") # Assuming email might exist
        content_layout.addLayout(contact_grid)
        
        # Metadata
        self.add_section_header(content_layout, "System Metadata", "fa5s.database")
        meta_grid = QGridLayout()
        self.add_field(meta_grid, 0, 0, "Created At", str(self.citizen.get('created_at'))[:10])
        self.add_field(meta_grid, 0, 2, "Last Updated", str(self.citizen.get('updated_at'))[:10])
        content_layout.addLayout(meta_grid)
        
        content_layout.addStretch()
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
        
        # Footer
        footer = QFrame()
        footer.setStyleSheet("background-color: #1a1a1a; border-top: 1px solid #333;")
        footer_layout = QHBoxLayout(footer)
        footer_layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.setFixedWidth(100)
        close_btn.clicked.connect(self.accept)
        footer_layout.addWidget(close_btn)
        
        layout.addWidget(footer)

    def add_section_header(self, layout, text, icon_name):
        header_layout = QHBoxLayout()
        icon = QLabel()
        icon.setPixmap(qta.icon(icon_name, color='#0088cc').pixmap(16, 16))
        
        label = QLabel(text)
        label.setObjectName("SectionHeader")
        
        header_layout.addWidget(icon)
        header_layout.addWidget(label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet("background-color: #333;")
        line.setFixedHeight(1)
        layout.addWidget(line)

    def add_field(self, grid, row, col, label_text, value_text):
        lbl = QLabel(label_text + ":")
        lbl.setStyleSheet("color: #aaa;")
        
        val = QLabel(str(value_text) if value_text else "N/A")
        val.setObjectName("ValueLabel")
        val.setWordWrap(True)
        
        grid.addWidget(lbl, row, col)
        grid.addWidget(val, row, col + 1)

    def get_gender_str(self, code):
        if code == 'M': return "Male"
        if code == 'F': return "Female"
        return str(code)
