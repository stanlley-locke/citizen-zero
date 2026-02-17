from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QTableWidget, QTableWidgetItem, QHeaderView, 
                             QPushButton, QDialog, QLineEdit, QFormLayout, QMessageBox, QFrame,
                             QMenu, QInputDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
import requests
import qtawesome as qta
from app_config import Endpoints

class CreateAdminDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Admin")
        self.setFixedSize(400, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.username = QLineEdit()
        self.email = QLineEdit()
        self.first_name = QLineEdit()
        self.last_name = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        
        form_layout.addRow("Username:", self.username)
        form_layout.addRow("Email:", self.email)
        form_layout.addRow("First Name:", self.first_name)
        form_layout.addRow("Last Name:", self.last_name)
        form_layout.addRow("Password:", self.password)
        
        layout.addLayout(form_layout)
        
        btn_layout = QHBoxLayout()
        submit_btn = QPushButton("Create Admin")
        submit_btn.clicked.connect(self.submit)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(submit_btn)
        layout.addLayout(btn_layout)

    def submit(self):
        data = {
            "username": self.username.text(),
            "email": self.email.text(),
            "password": self.password.text(),
            "first_name": self.first_name.text(),
            "last_name": self.last_name.text(),
        }
        
        if not data['username'] or not data['password']:
            QMessageBox.warning(self, "Error", "Username and Password are required.")
            return

        try:
            response = requests.post(Endpoints.AUTH_ADMIN_USERS, json=data)
            if response.status_code == 201:
                QMessageBox.information(self, "Success", "Admin created successfully.")
                self.accept()
            else:
                QMessageBox.warning(self, "Error", f"Failed: {response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

class AdminManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_admins()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Header with Add Button
        header = QHBoxLayout()
        title = QLabel("System Administrators")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        add_btn = QPushButton("Add New Admin")
        add_btn.setIcon(qta.icon('fa5s.user-plus', color='white'))
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #2da44e; 
                color: white; 
                padding: 6px 12px;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #2c974b; }
        """)
        add_btn.clicked.connect(self.open_create_dialog)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setIcon(qta.icon('fa5s.sync', color='black'))
        refresh_btn.clicked.connect(self.load_admins)
        
        header.addWidget(title)
        header.addStretch()
        header.addWidget(refresh_btn)
        header.addWidget(add_btn)
        
        layout.addLayout(header)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Username", "Email", "Active", "Last Login"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        layout.addWidget(self.table)
        
        # Context Menu
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.open_context_menu)

    def open_create_dialog(self):
        dialog = CreateAdminDialog(self)
        if dialog.exec():
            self.load_admins()

    def open_context_menu(self, position):
        menu = QMenu()
        
        toggle_action = menu.addAction("Toggle Active Status")
        reset_action = menu.addAction("Reset Password")
        edit_action = menu.addAction("Edit Details")
        activity_action = menu.addAction("View Activity Log")
        menu.addSeparator()
        delete_action = menu.addAction("Delete Admin")
        delete_action.setIcon(qta.icon('fa5s.trash-alt', color='red'))
        
        action = menu.exec(self.table.viewport().mapToGlobal(position))
        
        if action == toggle_action:
            self.toggle_status()
        elif action == reset_action:
            self.reset_password()
        elif action == edit_action:
            self.edit_admin()
        elif action == activity_action:
            self.view_activity()
        elif action == delete_action:
            self.delete_admin()

    def delete_admin(self):
        row = self.table.currentRow()
        if row < 0: return
        user_id = self.table.item(row, 0).text()
        username = self.table.item(row, 1).text()
        
        reply = QMessageBox.question(self, 'Confirm Delete', 
                                     f'Are you sure you want to permanently delete admin "{username}"?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                     QMessageBox.StandardButton.No)
                                     
        if reply == QMessageBox.StandardButton.Yes:
            try:
                url = f"{Endpoints.AUTH_ADMIN_USERS}{user_id}/"
                response = requests.delete(url, timeout=5)
                if response.status_code == 204:
                    QMessageBox.information(self, "Success", "Admin deleted.")
                    self.load_admins()
                else:
                    QMessageBox.warning(self, "Error", f"Failed: {response.text}")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def edit_admin(self):
        row = self.table.currentRow()
        if row < 0: return
        user_id = self.table.item(row, 0).text()
        
        # Fetch full details first or just pass what we have? 
        # We only have username/email in table. Better to fetch or pass those.
        # For efficiency, let's just use what we have and assume we can edit those.
        current_data = {
            'username': self.table.item(row, 1).text(),
            'email': self.table.item(row, 2).text(),
            'id': user_id
        }
        
        dialog = EditAdminDialog(current_data, self)
        if dialog.exec():
            self.load_admins()

    def view_activity(self):
        row = self.table.currentRow()
        if row < 0: return
        user_id = self.table.item(row, 0).text()
        username = self.table.item(row, 1).text()
        
        dialog = AdminActivityDialog(user_id, username, self)
        dialog.exec()

    def toggle_status(self):
        row = self.table.currentRow()
        if row < 0: return
        
        user_id = self.table.item(row, 0).text()
        current_status = self.table.item(row, 3).text()
        new_status = False if current_status == "True" else True
        
        try:
            url = f"{Endpoints.AUTH_ADMIN_USERS}{user_id}/"
            response = requests.patch(url, json={'is_active': new_status})
            if response.status_code == 200:
                self.load_admins()
            else:
                QMessageBox.warning(self, "Error", f"Failed: {response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def reset_password(self):
        row = self.table.currentRow()
        if row < 0: return
        user_id = self.table.item(row, 0).text()
        username = self.table.item(row, 1).text()
        
        password, ok = QInputDialog.getText(self, "Reset Password", f"Enter new password for {username}:", QLineEdit.EchoMode.Password)
        if ok and password:
            try:
                url = f"{Endpoints.AUTH_ADMIN_USERS}{user_id}/"
                response = requests.patch(url, json={'password': password})
                if response.status_code == 200:
                    QMessageBox.information(self, "Success", "Password updated.")
                else:
                     QMessageBox.warning(self, "Error", f"Failed: {response.text}")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def load_admins(self):
        try:
            # We implemented AdminUserViewSet at /admin/users/
            response = requests.get(Endpoints.AUTH_ADMIN_USERS, timeout=5)
            if response.status_code == 200:
                self.update_table(response.json())
            else:
                print(f"Failed to load admins: {response.text}")
        except Exception as e:
            print(f"Connection error: {e}")

    def update_table(self, admins):
        self.table.setRowCount(0)
        self.table.setRowCount(len(admins))
        
        for i, admin in enumerate(admins):
            self.table.setItem(i, 0, QTableWidgetItem(str(admin.get('id', ''))))
            self.table.setItem(i, 1, QTableWidgetItem(admin.get('username', '')))
            self.table.setItem(i, 2, QTableWidgetItem(admin.get('email', '')))
            
            active = str(admin.get('is_active', ''))
            status_item = QTableWidgetItem(active)
            if active == "True":
                status_item.setForeground(QColor('green'))
            else:
                status_item.setForeground(QColor('red'))
            self.table.setItem(i, 3, status_item)
            
            self.table.setItem(i, 4, QTableWidgetItem(str(admin.get('last_login', ''))))

class EditAdminDialog(QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.setWindowTitle(f"Edit Admin: {data['username']}")
        self.setFixedSize(400, 200)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()
        
        self.email = QLineEdit(self.data['email'])
        self.first_name = QLineEdit() # We don't have this in table yet, leave empty
        self.last_name = QLineEdit()
        
        form.addRow("Email:", self.email)
        form.addRow("First Name:", self.first_name)
        form.addRow("Last Name:", self.last_name)
        
        layout.addLayout(form)
        
        btns = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        btns.addWidget(cancel_btn)
        btns.addWidget(save_btn)
        layout.addLayout(btns)

    def save(self):
        try:
            url = f"{Endpoints.AUTH_ADMIN_USERS}{self.data['id']}/"
            payload = {'email': self.email.text()}
            if self.first_name.text(): payload['first_name'] = self.first_name.text()
            if self.last_name.text(): payload['last_name'] = self.last_name.text()
            
            response = requests.patch(url, json=payload)
            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Admin updated.")
                self.accept()
            else:
                QMessageBox.warning(self, "Error", f"Failed: {response.text}")
        except Exception as e:
             QMessageBox.critical(self, "Error", str(e))

class AdminActivityDialog(QDialog):
    def __init__(self, user_id, username, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.username = username
        self.setWindowTitle(f"Activity Log: {username}")
        self.resize(800, 500)
        self.init_ui()
        self.load_logs()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Time", "Action", "Severity", "Details"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

    def load_logs(self):
        try:
            # Filter audit logs by username if possible, or user_id?
            # Our AuditLog has user_id, which for admins is their username or ID?
            # In AdminUserViewSet.perform_create, we used 'actor' which was username.
            # In AdminLoginView, user_id = username.
            # So filtering by user_id = username (not ID) might be better?
            # Let's try filtering by username field first since we added it.
            
            # Since we just added 'username' field to AuditLog model, we can filter by that.
            # ViewSet supports user_id filter (icontains). 
            # We assume user_id in AuditLog IS the username for Admins based on our previous edits.
            
            # Wait, `user_id` in `AdminUserViewSet` logs was set to `actor` (username).
            # So searching for user_id=username should work.
            url = Endpoints.AUDIT_LOGS
            # We use username from the table (col 1)
            # user_id passing into this dialog is the DB ID (col 0).
            # We want to filter by the username string.
            # But wait, self.user_id passed in init is actually the ID from col 0. 
            # We need the username string. Let's assume the caller passes username correctly?
            # Caller: `dialog = AdminActivityDialog(user_id, username, self)` -> yes username is arg 2.
            
            # But filtering by user_id in AuditLogViewSet does `user_id__icontains`.
            # If we filter by `username` (the new model field), we need to update ViewSet to support it?
            # AuditLogViewSet filters: user_id, severity, action...
            # It does NOT filter by `username` field yet explicitly.
            # But consistent with `user_id` field being used for username in our logging logic.
            
            params = {'user_id': self.username} # Use self.username which we need to store
            response = requests.get(url, params=params)
             
            if response.status_code == 200:
                self.update_table(response.json())
        except Exception as e:
            print(e)
            
    def update_table(self, logs):
        self.table.setRowCount(len(logs))
        for i, log in enumerate(logs):
            self.table.setItem(i, 0, QTableWidgetItem(log.get('timestamp', '')[:19]))
            self.table.setItem(i, 1, QTableWidgetItem(log.get('action', '')))
            self.table.setItem(i, 2, QTableWidgetItem(log.get('severity', '')))
            self.table.setItem(i, 3, QTableWidgetItem(log.get('details', '')))
