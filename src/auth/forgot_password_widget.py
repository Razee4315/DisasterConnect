"""Forgot password window for DisasterConnect."""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QLabel, QLineEdit, QPushButton, QFrame, QMessageBox,
                           QStackedWidget)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon
import os
import re
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from ..utils.mongodb_client import mongodb_client
import bcrypt

class ForgotPasswordWindow(QMainWindow):
    switch_to_login = pyqtSignal()
    
    def __init__(self, auth_manager=None):
        super().__init__()
        self.auth_manager = auth_manager
        self.setWindowTitle("DisasterConnect - Reset Password")
        self.setFixedSize(800, 500)
        self.reset_code = None
        self.reset_email = None
        self.code_expiry = None
        
        # Set window icon
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                'resources', 'images', 'logo_icon.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Create left panel (logo and message)
        left_panel = QFrame()
        left_panel.setObjectName("auth-panel")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignCenter)
        
        # Add logo
        logo_label = QLabel()
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                'resources', 'images', 'logo_large.png')
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            logo_label.setPixmap(pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
            logo_label.setStyleSheet("margin-bottom: 20px;")
        
        # Add message
        title_label = QLabel("Reset Password")
        title_label.setObjectName("welcome-text")
        title_label.setAlignment(Qt.AlignCenter)
        
        description_label = QLabel("Don't worry! It happens. Please follow the steps "
                                 "to securely reset your password.")
        description_label.setObjectName("description-text")
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setWordWrap(True)
        
        left_layout.addWidget(logo_label)
        left_layout.addWidget(title_label)
        left_layout.addWidget(description_label)
        
        # Create right panel with stacked widgets
        right_panel = QFrame()
        right_panel.setObjectName("auth-panel")
        right_layout = QVBoxLayout(right_panel)
        
        self.stacked_widget = QStackedWidget()
        self.email_page = self._create_email_page()
        self.code_verification_page = self._create_verification_page()
        self.new_password_page = self._create_new_password_page()
        
        self.stacked_widget.addWidget(self.email_page)
        self.stacked_widget.addWidget(self.code_verification_page)
        self.stacked_widget.addWidget(self.new_password_page)
        
        right_layout.addWidget(self.stacked_widget)
        
        # Add panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)
        
        # Set stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5;
            }
            #auth-panel {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
                margin: 10px;
                min-width: 350px;
            }
            #welcome-text {
                font-size: 28px;
                font-weight: bold;
                color: #1a73e8;
                margin: 20px 0;
            }
            #description-text {
                font-size: 16px;
                color: #5f6368;
                margin-bottom: 20px;
                max-width: 300px;
            }
            #form-title {
                font-size: 24px;
                font-weight: bold;
                color: #202124;
                margin-bottom: 20px;
            }
            #auth-input {
                padding: 12px;
                margin: 8px 0;
                border: 1px solid #dadce0;
                border-radius: 5px;
                font-size: 14px;
                background-color: #f8f9fa;
            }
            #auth-input:focus {
                border-color: #1a73e8;
                background-color: white;
                outline: none;
            }
            #hint-text {
                font-size: 14px;
                color: #5f6368;
                margin: 4px 0 20px 0;
            }
            #primary-button {
                background-color: #1a73e8;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 5px;
                margin: 20px 0;
                font-size: 16px;
                font-weight: 500;
            }
            #primary-button:hover {
                background-color: #1557b0;
            }
            #text-button {
                background: none;
                border: none;
                color: #1a73e8;
                text-decoration: none;
                font-size: 14px;
                font-weight: 500;
                padding: 0 5px;
            }
            #text-button:hover {
                text-decoration: underline;
            }
        """)
    
    def _create_email_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)
        
        form_label = QLabel("Enter your email")
        form_label.setObjectName("form-title")
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email Address")
        self.email_input.setObjectName("auth-input")
        
        hint_label = QLabel("We'll send you a verification code")
        hint_label.setObjectName("hint-text")
        hint_label.setWordWrap(True)
        
        send_button = QPushButton("Send Verification Code")
        send_button.setObjectName("primary-button")
        send_button.clicked.connect(self._handle_email_submit)
        
        back_button = QPushButton("Back to Login")
        back_button.setObjectName("text-button")
        back_button.clicked.connect(self.switch_to_login.emit)
        
        layout.addWidget(form_label)
        layout.addWidget(self.email_input)
        layout.addWidget(hint_label)
        layout.addWidget(send_button)
        layout.addWidget(back_button)
        
        return page
    
    def _create_verification_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)
        
        title = QLabel("Enter Verification Code")
        title.setObjectName("form-title")
        
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Enter 6-digit code")
        self.code_input.setObjectName("auth-input")
        self.code_input.setMaxLength(6)
        
        hint_label = QLabel("Please enter the verification code sent to your email")
        hint_label.setObjectName("hint-text")
        hint_label.setWordWrap(True)
        
        verify_button = QPushButton("Verify Code")
        verify_button.setObjectName("primary-button")
        verify_button.clicked.connect(self._verify_code)
        
        resend_button = QPushButton("Resend Code")
        resend_button.setObjectName("text-button")
        resend_button.clicked.connect(self._resend_code)
        
        layout.addWidget(title)
        layout.addWidget(self.code_input)
        layout.addWidget(hint_label)
        layout.addWidget(verify_button)
        layout.addWidget(resend_button)
        
        return page
    
    def _create_new_password_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)
        
        title = QLabel("Create New Password")
        title.setObjectName("form-title")
        
        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("New Password")
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input.setObjectName("auth-input")
        
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm New Password")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setObjectName("auth-input")
        
        hint_label = QLabel("Password must be at least 8 characters long and contain letters and numbers")
        hint_label.setObjectName("hint-text")
        hint_label.setWordWrap(True)
        
        reset_button = QPushButton("Reset Password")
        reset_button.setObjectName("primary-button")
        reset_button.clicked.connect(self._reset_password)
        
        layout.addWidget(title)
        layout.addWidget(self.new_password_input)
        layout.addWidget(self.confirm_password_input)
        layout.addWidget(hint_label)
        layout.addWidget(reset_button)
        
        return page
    
    def _handle_email_submit(self):
        email = self.email_input.text().strip()
        if not self._validate_email(email):
            QMessageBox.warning(self, "Invalid Email", "Please enter a valid email address.")
            return
            
        # Check if email exists in database
        user = mongodb_client.users.find_one({"email": email})
        if not user:
            QMessageBox.warning(self, "Account Not Found", 
                              "No account found with this email address.")
            return
            
        self.reset_email = email
        self.reset_code = ''.join(secrets.choice('0123456789') for _ in range(6))
        self.code_expiry = datetime.now() + timedelta(minutes=15)
        
        # Store reset code in database
        mongodb_client.users.update_one(
            {"email": email},
            {"$set": {
                "reset_code": self.reset_code,
                "reset_code_expiry": self.code_expiry
            }}
        )
        
        # Send verification email
        if self._send_verification_email():
            self.stacked_widget.setCurrentIndex(1)
        else:
            QMessageBox.critical(self, "Error", 
                               "Failed to send verification code. Please try again.")
    
    def _send_verification_email(self):
        try:
            # Configure your email settings here
            sender_email = "your-email@example.com"
            sender_password = "your-app-specific-password"
            
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = self.reset_email
            msg['Subject'] = "DisasterConnect Password Reset Code"
            
            body = f"""
            Your password reset code is: {self.reset_code}
            
            This code will expire in 15 minutes.
            
            If you didn't request this reset, please ignore this email.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # For development/testing, just return True
            # In production, uncomment the following code and configure proper email settings
            return True
            
            # with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            #     server.login(sender_email, sender_password)
            #     server.send_message(msg)
            
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False
    
    def _verify_code(self):
        entered_code = self.code_input.text().strip()
        if not entered_code:
            QMessageBox.warning(self, "Invalid Code", "Please enter the verification code.")
            return
            
        user = mongodb_client.users.find_one({
            "email": self.reset_email,
            "reset_code": entered_code,
            "reset_code_expiry": {"$gt": datetime.now()}
        })
        
        if not user:
            QMessageBox.warning(self, "Invalid Code", 
                              "Invalid or expired verification code.")
            return
            
        self.stacked_widget.setCurrentIndex(2)
    
    def _reset_password(self):
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()
        
        if not self._validate_password(new_password):
            QMessageBox.warning(self, "Invalid Password", 
                              "Password must be at least 8 characters long and contain letters and numbers.")
            return
            
        if new_password != confirm_password:
            QMessageBox.warning(self, "Password Mismatch", 
                              "Passwords do not match.")
            return
            
        # Update password in database
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        mongodb_client.users.update_one(
            {"email": self.reset_email},
            {
                "$set": {"password": hashed_password},
                "$unset": {"reset_code": "", "reset_code_expiry": ""}
            }
        )
        
        QMessageBox.information(self, "Success", 
                              "Password has been reset successfully!")
        self.switch_to_login.emit()
    
    def _validate_email(self, email):
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        return bool(email_pattern.match(email))
    
    def _validate_password(self, password):
        if len(password) < 8:
            return False
        if not re.search(r'[A-Za-z]', password):
            return False
        if not re.search(r'\d', password):
            return False
        return True
    
    def _resend_code(self):
        self._handle_email_submit()
