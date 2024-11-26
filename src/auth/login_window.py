from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QLineEdit, QPushButton, 
                           QMessageBox)
from PyQt5.QtCore import pyqtSignal

class LoginWindow(QWidget):
    login_successful = pyqtSignal(dict)
    
    def __init__(self, auth_manager):
        super().__init__()
        self.auth_manager = auth_manager
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the login window UI"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Username field
        username_layout = QHBoxLayout()
        username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        
        # Password field
        password_layout = QHBoxLayout()
        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        
        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.handle_login)
        
        # Register button
        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.show_register)
        
        # Add all widgets to main layout
        layout.addLayout(username_layout)
        layout.addLayout(password_layout)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)
        
    def handle_login(self):
        """Handle login button click"""
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return
            
        user_data = self.auth_manager.login(username, password)
        if user_data:
            self.login_successful.emit(user_data)
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password")
            
    def show_register(self):
        """Show registration window"""
        self.register_window = RegisterWindow(self.auth_manager)
        self.register_window.show()
        
class RegisterWindow(QWidget):
    def __init__(self, auth_manager):
        super().__init__()
        self.auth_manager = auth_manager
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the registration window UI"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Username field
        username_layout = QHBoxLayout()
        username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        
        # Email field
        email_layout = QHBoxLayout()
        email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_input)
        
        # Password fields
        password_layout = QHBoxLayout()
        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        
        confirm_layout = QHBoxLayout()
        confirm_label = QLabel("Confirm Password:")
        self.confirm_input = QLineEdit()
        self.confirm_input.setEchoMode(QLineEdit.Password)
        confirm_layout.addWidget(confirm_label)
        confirm_layout.addWidget(self.confirm_input)
        
        # Register button
        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.handle_register)
        
        # Add all widgets to main layout
        layout.addLayout(username_layout)
        layout.addLayout(email_layout)
        layout.addLayout(password_layout)
        layout.addLayout(confirm_layout)
        layout.addWidget(self.register_button)
        
    def handle_register(self):
        """Handle registration button click"""
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        confirm = self.confirm_input.text()
        
        if not all([username, email, password, confirm]):
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return
            
        if password != confirm:
            QMessageBox.warning(self, "Error", "Passwords do not match")
            return
            
        if self.auth_manager.register_user(username, password, email):
            QMessageBox.information(self, "Success", "Registration successful")
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Username already exists")
