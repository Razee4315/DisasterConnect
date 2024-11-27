from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
from ..utils.mongodb_client import mongodb_client
import hashlib
import logging
import os

logger = logging.getLogger(__name__)

class LoginWidget(QWidget):
    login_success = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """Initialize the login UI"""
        layout = QVBoxLayout()
        layout.setSpacing(15)  # Add space between elements
        layout.setContentsMargins(30, 30, 30, 30)  # Add margins around the form
        
        # Add logo
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                               'resources', 'images', 'logo_new.svg')
        if os.path.exists(logo_path):
            logo_label = QLabel()
            logo_pixmap = QPixmap(logo_path)
            scaled_pixmap = logo_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(logo_label)
        
        # Add logo or title
        title_label = QLabel("DisasterConnect")
        title_label.setStyleSheet("""
            QLabel {
                color: #2C3E50;
                font-size: 24px;
                font-weight: bold;
                qproperty-alignment: AlignCenter;
            }
        """)
        layout.addWidget(title_label)
        
        # Add some spacing
        layout.addSpacing(20)
        
        # Username field
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #BDC3C7;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #3498DB;
            }
        """)
        layout.addWidget(self.username_input)
        
        # Password field
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #BDC3C7;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #3498DB;
            }
        """)
        layout.addWidget(self.password_input)
        
        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #2ECC71;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27AE60;
            }
            QPushButton:pressed {
                background-color: #219A52;
            }
        """)
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)
        
        # Add stretch to push everything to the top
        layout.addStretch()
        
        self.setLayout(layout)
        
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
            
    def clear_fields(self):
        """Clear all input fields"""
        self.username_input.clear()
        self.password_input.clear()
