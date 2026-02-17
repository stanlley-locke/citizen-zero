from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTabWidget)
from ui.widgets.security.audit_trail_widget import AuditTrailWidget
from ui.widgets.security.admin_management_widget import AdminManagementWidget
from ui.widgets.security.alerts_widget import AlertsWidget

class SecurityWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #e0e0e0; border-radius: 4px; }
            QTabBar::tab { background: #f6f8fa; padding: 10px 20px; border: 1px solid #e0e0e0; border-bottom: none; }
            QTabBar::tab:selected { background: white; border-bottom: 2px solid #0969da; }
        """)
        
        # Tabs
        self.audit_tab = AuditTrailWidget()
        self.alerts_tab = AlertsWidget()
        self.admin_tab = AdminManagementWidget()
        
        self.tabs.addTab(self.alerts_tab, "Alerts")
        self.tabs.addTab(self.audit_tab, "Audit Trail")
        self.tabs.addTab(self.admin_tab, "Admin Management")
        
        layout.addWidget(self.tabs)
