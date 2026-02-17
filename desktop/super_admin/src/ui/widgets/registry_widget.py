from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QFrame)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QIcon
import requests
from app_config import Endpoints
import qtawesome as qta

from ui.dialogs.citizen_detail_dialog import CitizenDetailDialog
from ui.dialogs.citizen_registration_dialog import CitizenRegistrationDialog

class RegistryWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Citizen Registry")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # Register Button
        self.register_btn = QPushButton("Register Citizen")
        self.register_btn.setIcon(qta.icon('fa5s.plus', color='white'))
        self.register_btn.setStyleSheet("""
            QPushButton {
                background-color: #0088cc;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                border: none;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0099dd;
            }
        """)
        self.register_btn.clicked.connect(self.open_registration_dialog)
        header_layout.addWidget(self.register_btn)
        
        # Refresh Button
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setIcon(qta.icon('fa5s.sync-alt', color='white'))
        self.refresh_btn.setStyleSheet("""
             QPushButton {
                background-color: #333;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                border: 1px solid #444;
            }
            QPushButton:hover {
                background-color: #444;
            }
        """)
        self.refresh_btn.clicked.connect(lambda: self.load_data(self.current_url))
        header_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Search Bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by National ID, Name...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                background-color: #252525;
                border: 1px solid #3d3d3d;
                border-radius: 5px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #0088cc;
            }
        """)
        # Debounce search
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.setInterval(500)
        self.search_timer.timeout.connect(self.perform_search)
        
        self.search_input.textChanged.connect(self.on_search_text_changed)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["National ID", "Name", "DOB", "Gender", "County"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #252525;
                gridline-color: #3d3d3d;
                border: 1px solid #3d3d3d;
                color: #ddd;
                alternate-background-color: #2a2a2a;
            }
            QHeaderView::section {
                background-color: #333;
                color: white;
                padding: 8px;
                border: 1px solid #3d3d3d;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #0088cc;
                color: white;
            }
        """)
        layout.addWidget(self.table)
        
        # Pagination controls
        self.pagination_layout = QHBoxLayout()
        self.prev_btn = QPushButton("Previous")
        self.prev_btn.clicked.connect(self.prev_page)
        self.prev_btn.setEnabled(False)
        self.next_btn = QPushButton("Next")
        self.next_btn.clicked.connect(self.next_page)
        self.next_btn.setEnabled(False)
        self.page_label = QLabel("Page 1")
        self.page_label.setStyleSheet("color: #aaa;")
        
        self.pagination_layout.addWidget(self.prev_btn)
        self.pagination_layout.addWidget(self.page_label)
        self.pagination_layout.addWidget(self.next_btn)
        
        self.count_label = QLabel("Showing 0 records")
        self.count_label.setStyleSheet("color: #aaa; margin-left: 20px;")
        self.pagination_layout.addWidget(self.count_label)
        
        self.pagination_layout.addStretch()
        layout.addLayout(self.pagination_layout)
        
        # Connect double click
        self.table.itemDoubleClicked.connect(self.show_citizen_details)
        
        # Data placeholder
        self.all_users = []
        self.base_url = Endpoints.CITIZENS
        self.current_url = f"{self.base_url}?page_size=20"
        self.next_url = None
        self.prev_url = None
        
        # Initial Load
        QTimer.singleShot(500, lambda: self.load_data(self.current_url))

    def load_data(self, url):
        if not url:
            return
            
        self.refresh_btn.setEnabled(False)
        self.refresh_btn.setText("Loading...")
        
        try:
            print(f"Fetching Citizens from: {url}")
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check for DRF pagination
                if isinstance(data, dict) and 'results' in data:
                    self.all_users = data['results']
                    self.next_url = data.get('next')
                    self.prev_url = data.get('previous')
                    self.count_label.setText(f"Total Records: {data.get('count', '?')}")
                    
                elif isinstance(data, list):
                    # Fallback for no pagination
                    self.all_users = data
                    self.next_url = None
                    self.prev_url = None
                    self.count_label.setText(f"Total Records: {len(data)}")
                
                self.update_table(self.all_users)
                self.update_pagination_buttons()
            else:
                print(f"Failed to fetch citizens: {response.status_code}")
                # Optional details
        except Exception as e:
            print(f"Error fetching citizens: {e}")
        finally:
            self.refresh_btn.setEnabled(True)
            self.refresh_btn.setText("Refresh")

    def update_table(self, citizens):
        self.table.setRowCount(len(citizens))
        
        for i, citizen in enumerate(citizens):
            nid = str(citizen.get('national_id', ''))
            f_name = str(citizen.get('first_name', ''))
            l_name = str(citizen.get('last_name', ''))
            dob = str(citizen.get('date_of_birth', ''))
            gender = "Male" if citizen.get('gender') == 'M' else "Female" if citizen.get('gender') == 'F' else str(citizen.get('gender', ''))
            county = str(citizen.get('county_of_birth', ''))
            
            self.table.setItem(i, 0, QTableWidgetItem(nid))
            self.table.setItem(i, 1, QTableWidgetItem(f"{f_name} {l_name}"))
            self.table.setItem(i, 2, QTableWidgetItem(dob))
            self.table.setItem(i, 3, QTableWidgetItem(gender))
            self.table.setItem(i, 4, QTableWidgetItem(county))
            
    def update_pagination_buttons(self):
        self.next_btn.setEnabled(bool(self.next_url))
        self.prev_btn.setEnabled(bool(self.prev_url))

    def next_page(self):
        if self.next_url:
            self.load_data(self.next_url)

    def prev_page(self):
        if self.prev_url:
            self.load_data(self.prev_url)

    def on_search_text_changed(self, text):
        self.search_timer.start()

    def perform_search(self):
        text = self.search_input.text().strip()
        if text:
            # Append search query to base url
            # Note: ?page_size=20 should be preserved.
            # DRF uses ?search=... if SearchFilter is enabled.
            url = f"{self.base_url}?page_size=20&search={text}"
        else:
            url = f"{self.base_url}?page_size=20"
        
        self.current_url = url
        self.load_data(url)

    def show_citizen_details(self, item):
        row = item.row()
        nid = self.table.item(row, 0).text()
        
        # Find citizen in current list
        citizen = next((c for c in self.all_users if str(c.get('national_id')) == nid), None)
        
        if citizen:
            dialog = CitizenDetailDialog(citizen, self)
            dialog.exec()
            
    def open_registration_dialog(self):
        dialog = CitizenRegistrationDialog(self)
        if dialog.exec():
             # Refresh data if registration was successful
             self.load_data(self.current_url)
