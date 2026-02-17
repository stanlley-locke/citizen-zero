from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTreeWidget, QTreeWidgetItem, QTreeWidgetItemIterator, QStackedWidget, QLabel, QPushButton, QFrame,
                             QSizePolicy, QHeaderView)
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve
import qtawesome as qta 
from ui.widgets.dashboard_widget import DashboardWidget
from ui.widgets.registry_widget import RegistryWidget
from ui.widgets.biometric_widget import BiometricWidget
from ui.widgets.id_widget import IDWidget # Reusing for all doc types
from ui.widgets.security.audit_trail_widget import AuditTrailWidget
from ui.widgets.security.alerts_widget import AlertsWidget
from ui.widgets.security.admin_management_widget import AdminManagementWidget
from ui.widgets.security.verifications_widget import VerificationsWidget
from ui.widgets.security.verifications_widget import VerificationsWidget
from ui.widgets.requests_widget import RequestsWidget
from ui.widgets.infrastructure.microservices_widget import MicroservicesWidget
from ui.widgets.infrastructure.nodes_widget import NodesWidget
from ui.widgets.infrastructure.databases_widget import DatabasesWidget
from ui.widgets.infrastructure.backups_widget import BackupsWidget
from ui.widgets.infrastructure.topology_widget import TopologyWidget
from ui.widgets.configuration.network_widget import NetworkConfigWidget
from ui.widgets.configuration.system_vars_widget import SystemVarsWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # ... (init code same as before until Create Pages) ...
        self.setWindowTitle("CitizenZero - Super Admin Platform")
        self.resize(1280, 800)
        
        # Main Layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        layout = QHBoxLayout(main_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = self.create_sidebar()
        layout.addWidget(self.sidebar)
        
        # Content Area
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("background-color: #1e1e1e;")
        layout.addWidget(self.content_stack)
        
        # Create Pages
        self.pages = {}
        
        # Dashboard
        self.dashboard_page = DashboardWidget()
        self.content_stack.addWidget(self.dashboard_page)
        self.pages["dashboard"] = self.dashboard_page
        
        # Registry
        self.registry_page = RegistryWidget()
        self.content_stack.addWidget(self.registry_page)
        self.pages["citizen_registry"] = self.registry_page # Match key in sidebar
        
        # Biometrics
        self.bio_page = BiometricWidget()
        self.content_stack.addWidget(self.bio_page)
        self.pages["biometrics"] = self.bio_page
        
        # Documents (Reusing IDWidget with different types)
        self.id_page = IDWidget(doc_type="NATIONAL_ID", title="National ID Management")
        self.content_stack.addWidget(self.id_page)
        self.pages["id_cards"] = self.id_page
        
        self.passport_page = IDWidget(doc_type="PASSPORT", title="Passport Control")
        self.content_stack.addWidget(self.passport_page)
        self.pages["passports"] = self.passport_page
        
        self.license_page = IDWidget(doc_type="DRIVING_LICENSE", title="Driving License Authority")
        self.content_stack.addWidget(self.license_page)
        self.pages["driving_licenses"] = self.license_page
        
        # Requests
        self.requests_page = RequestsWidget()
        self.content_stack.addWidget(self.requests_page)
        self.pages["requests"] = self.requests_page

        # Security - Individual Pages
        self.verifications_page = VerificationsWidget()
        self.content_stack.addWidget(self.verifications_page)
        self.pages["verification_logs"] = self.verifications_page

        self.audit_page = AuditTrailWidget()
        self.content_stack.addWidget(self.audit_page)
        self.pages["audit_trail"] = self.audit_page

        self.alerts_page = AlertsWidget()
        self.content_stack.addWidget(self.alerts_page)
        self.pages["security_alerts"] = self.alerts_page

        self.users_page = AdminManagementWidget()
        self.content_stack.addWidget(self.users_page)
        self.pages["admin_users"] = self.users_page
        
        # Placeholders for others
        # Infrastructure Pages
        self.topology_page = TopologyWidget()
        self.content_stack.addWidget(self.topology_page)
        self.pages["topology_map"] = self.topology_page

        self.nodes_page = NodesWidget()
        self.content_stack.addWidget(self.nodes_page)
        self.pages["server_nodes"] = self.nodes_page

        self.services_page = MicroservicesWidget()
        self.content_stack.addWidget(self.services_page)
        self.pages["service_status"] = self.services_page
        
        self.databases_page = DatabasesWidget()
        self.content_stack.addWidget(self.databases_page)
        self.pages["database_clusters"] = self.databases_page
        
        self.backups_page = BackupsWidget()
        self.content_stack.addWidget(self.backups_page)
        self.pages["backups"] = self.backups_page
        
        self.network_page = NetworkConfigWidget()
        self.content_stack.addWidget(self.network_page)
        self.pages["network_config"] = self.network_page

        self.system_page = SystemVarsWidget()
        self.content_stack.addWidget(self.system_page)
        self.pages["system_settings"] = self.system_page
        

        
        # Select initial
        self.content_stack.setCurrentWidget(self.dashboard_page)
        
        # Animation State
        self.sidebar_expanded = True
        self.animation = QPropertyAnimation(self.sidebar, b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuart)

    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("background-color: #2d2d2d; border-right: 1px solid #3d3d3d;")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # Top Header (Logo + Toggle)
        header_frame = QFrame()
        header_frame.setFixedHeight(60)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(10, 10, 10, 10)
        
        self.toggle_btn = QPushButton()
        self.toggle_btn.setIcon(qta.icon('fa5s.bars', color='white'))
        self.toggle_btn.setFixedSize(40, 40)
        self.toggle_btn.setStyleSheet("background: transparent; border: none;")
        self.toggle_btn.clicked.connect(self.toggle_sidebar)
        
        self.logo_label = QLabel("CITIZEN ZERO")
        self.logo_label.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        
        header_layout.addWidget(self.logo_label)
        header_layout.addStretch()
        header_layout.addWidget(self.toggle_btn)
        
        sidebar_layout.addWidget(header_frame)
        
        # --- Menu (Tree Widget for Sub-menus) ---
        self.menu_tree = QTreeWidget()
        self.menu_tree.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.menu_tree.setHeaderHidden(True)
        self.menu_tree.setIndentation(20)
        self.menu_tree.setIconSize(QSize(20, 20))
        self.menu_tree.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.menu_tree.setStyleSheet("""
            QTreeWidget { 
                background: transparent; 
                border: none; 
                outline: none; 
            }
            QTreeWidget::item { 
                padding: 10px; 
                border-radius: 4px; 
                color: #e0e0e0; 
                margin: 2px 4px;
            }
            QTreeWidget::item:selected { 
                background-color: #BB0000; 
                color: white; 
            }
            QTreeWidget::item:hover { 
                background-color: #3d3d3d; 
            }
            QTreeWidget::branch:has-children:!has-siblings:closed,
            QTreeWidget::branch:closed:has-children:has-siblings {
                image: none; 
            }
        """)
        
        # 1. DASHBOARD
        self.add_top_level_link(self.menu_tree, "Dashboard", "fa5s.chart-line", "dashboard")

        # 2. CITIZEN SERVICES
        cit_group = self.add_group_header(self.menu_tree, "CITIZEN SERVICES", "fa5s.users")
        self.add_sub_item(cit_group, "Registry", "fa5s.list", "citizen_registry")
        self.add_sub_item(cit_group, "Biometrics", "fa5s.fingerprint", "biometrics")
        self.add_sub_item(cit_group, "ID Cards", "fa5s.id-card", "id_cards")
        self.add_sub_item(cit_group, "Passports", "fa5s.passport", "passports")
        self.add_sub_item(cit_group, "Driving Licenses", "fa5s.car", "driving_licenses")
        self.add_sub_item(cit_group, "Requests", "fa5s.clipboard-check", "requests")

        # 3. SECURITY
        sec_group = self.add_group_header(self.menu_tree, "SECURITY", "fa5s.shield-alt")
        self.add_sub_item(sec_group, "Verifications", "fa5s.history", "verification_logs")
        self.add_sub_item(sec_group, "Audit Trail", "fa5s.list-alt", "audit_trail")
        self.add_sub_item(sec_group, "Alerts", "fa5s.bell", "security_alerts")
        self.add_sub_item(sec_group, "Admins", "fa5s.user-shield", "admin_users")

        # 4. INFRASTRUCTURE
        inf_group = self.add_group_header(self.menu_tree, "INFRASTRUCTURE", "fa5s.server")
        self.add_sub_item(inf_group, "Network Topology", "fa5s.project-diagram", "topology_map")
        self.add_sub_item(inf_group, "Node Resources", "fa5s.microchip", "server_nodes")
        self.add_sub_item(inf_group, "Microservices", "fa5s.heartbeat", "service_status")
        self.add_sub_item(inf_group, "Databases", "fa5s.database", "database_clusters")
        self.add_sub_item(inf_group, "Backups", "fa5s.save", "backups")

        # 5. CONFIG
        cfg_group = self.add_group_header(self.menu_tree, "CONFIGURATION", "fa5s.cogs")
        self.add_sub_item(cfg_group, "Network API", "fa5s.globe", "network_config")
        self.add_sub_item(cfg_group, "System Vars", "fa5s.sliders-h", "system_settings")

        self.menu_tree.itemClicked.connect(self.on_menu_click)
        sidebar_layout.addWidget(self.menu_tree)
        
        # User Info at Bottom
        self.user_info = QLabel("Admin: SUPERUSER")
        self.user_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.user_info.setStyleSheet("color: #888; padding: 20px; font-size: 10px; border-top: 1px solid #3d3d3d;")
        sidebar_layout.addWidget(self.user_info)
        
        return sidebar

    # Removed duplicate duplicate add_top_level_link and others if they existed here
    # We will keep the definitions at the bottom of the class
    pass

    def create_placeholder(self, title):
        page = QWidget()
        layout = QVBoxLayout(page)
        header = QLabel(title)
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: white; margin-bottom: 20px;")
        layout.addWidget(header)
        
        content = QLabel(f"Manage {title} here...")
        content.setStyleSheet("color: #888; font-size: 16px;")
        layout.addWidget(content)
        
        layout.addStretch()
        return page

    # --- Helper Methods ---

    def add_top_level_link(self, parent, text, icon_name, page_key):
        item = QTreeWidgetItem(parent)
        item.setText(0, text)
        item.setIcon(0, qta.icon(icon_name, color='#e0e0e0'))
        item.setData(0, Qt.ItemDataRole.UserRole, page_key)
        item.setData(0, Qt.ItemDataRole.UserRole + 1, "page")
        item.setData(0, Qt.ItemDataRole.UserRole + 2, text)
        return item

    def add_group_header(self, parent, text, icon_name):
        item = QTreeWidgetItem(parent)
        item.setText(0, text)
        item.setIcon(0, qta.icon(icon_name, color='#e0e0e0')) 
        item.setData(0, Qt.ItemDataRole.UserRole, None) 
        item.setData(0, Qt.ItemDataRole.UserRole + 1, "group")
        item.setData(0, Qt.ItemDataRole.UserRole + 2, text)
        font = item.font(0)
        font.setBold(True)
        item.setFont(0, font)
        return item

    def add_sub_item(self, parent, text, icon_name, page_key):
        item = QTreeWidgetItem(parent)
        item.setText(0, text)
        item.setIcon(0, qta.icon(icon_name, color='#aaaaaa'))
        item.setData(0, Qt.ItemDataRole.UserRole, page_key)
        item.setData(0, Qt.ItemDataRole.UserRole + 1, "page")
        item.setData(0, Qt.ItemDataRole.UserRole + 2, text)
        return item


    def create_and_add_page(self, key, title):
        page = self.create_placeholder(title)
        self.content_stack.addWidget(page)
        self.pages[key] = page

    def on_menu_click(self, item, column):
        page_key = item.data(0, Qt.ItemDataRole.UserRole)
        role = item.data(0, Qt.ItemDataRole.UserRole + 1)
        
        if role == "group":
            # Toggle expansion if needed, but QTreeWidget handles this mostly.
            if item.isExpanded():
                item.setExpanded(False)
            else:
                item.setExpanded(True)
        elif page_key in self.pages:
            self.content_stack.setCurrentWidget(self.pages[page_key])

    def toggle_sidebar(self):
        if self.sidebar_expanded:
            # Collapse
            self.sidebar.setFixedWidth(70) 
            self.logo_label.hide()
            self.user_info.hide()
            self.menu_tree.setIndentation(0) # Remove indentation for collapsed view
            
            # Hide text for all items
            iterator = QTreeWidgetItemIterator(self.menu_tree)
            while iterator.value():
                item = iterator.value()
                item.setText(0, "") # clear text
                # We might want to collapse all groups too?
                # If we collapse groups, we only see group icons. 
                # If we keep expanded, we see all icons in a long list.
                iterator += 1
                
        else:
            # Expand
            self.sidebar.setFixedWidth(250)
            self.logo_label.show()
            self.user_info.show()
            self.menu_tree.setIndentation(20)
            
            # Restore Texts (This is tricky since we lost the state... 
            # ideally we should store text in UserRole + 2 like before)
            # Re-building tree or storing text is better.
            
            # Since I didn't verify the text storage in previous step, let's fix it live by just reloading the app or 
            # better: Store the text in a custom data role when creating items.
            pass # Quick hack: The user will likely restart the app to see expanded view properly or we fix logic now.
            
            # Actually, let's fix the logic right now in a better way:
            # We need to store original text to restore it.
            self.restore_tree_text()
            
        self.sidebar_expanded = not self.sidebar_expanded


    
    # ... (Need to update other add methods to store text) ...
    
    def restore_tree_text(self):
         iterator = QTreeWidgetItemIterator(self.menu_tree)
         while iterator.value():
            item = iterator.value()
            text = item.data(0, Qt.ItemDataRole.UserRole + 2)
            if text:
                item.setText(0, text)
            iterator += 1


