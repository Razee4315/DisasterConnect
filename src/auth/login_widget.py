from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import pyqtSignal
from ..utils.mongodb_client import mongodb_client
import hashlib
import logging

logger = logging.getLogger(__name__)

class LoginWidget(QWidget):
    login_success = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """Initialize the login UI"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("DisasterConnect Login")
        title.setStyleSheet("font-size: 24px; margin-bottom: 20px;")
        layout.addWidget(title)
        
        # Username input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)
        
        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)
        
        # Login button
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.handle_login)
        layout.addWidget(login_button)
        
        # Center the login form
        layout.addStretch(1)
        self.setLayout(layout)
        layout.addStretch(1)
        
    def handle_login(self):
        """Handle login attempt"""
        try:
            username = self.username_input.text().strip()
            password = self.password_input.text().strip()
            
            logger.info(f"Attempting login for user: {username}")
            
            if not username or not password:
                QMessageBox.warning(self, "Error", "Please enter both username and password")
                return
            
            # Hash password (SHA-256)
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            # Check credentials
            db = mongodb_client.get_database()
            user = db.users.find_one({
                "username": username,
                "password": hashed_password
            })
            
            if user:
                logger.info(f"Login successful for user: {username}")
                # Convert ObjectId to string for JSON serialization
                user['_id'] = str(user['_id'])
                # Remove password from user data
                user.pop("password", None)
                self.login_success.emit(user)
            else:
                logger.warning(f"Login failed for user: {username}")
                QMessageBox.warning(self, "Error", "Invalid username or password")
                
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            QMessageBox.critical(self, "Error", f"Login failed: {str(e)}")
