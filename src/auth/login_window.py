"""Login window for DisasterConnect."""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QLabel, QLineEdit, QPushButton, QFrame, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
import os

class LoginWindow(QMainWindow):
    """Login window for the application."""
    
    login_successful = pyqtSignal(dict)
    
    def __init__(self, auth_manager=None):
        super().__init__()
        self.auth_manager = auth_manager
        self.setup_window()
        self.setup_ui()
        self.setup_styles()
        
    def setup_window(self):
        """Setup the main window properties."""
        self.setWindowTitle("DisasterConnect - Login")
        self.setFixedSize(1200, 700)  # Increased size for better readability
        
        # Set window icon
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                'resources', 'images', 'logo_icon.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
    def setup_ui(self):
        """Setup the user interface."""
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create and add left panel (branding)
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel)
        
        # Create and add right panel (login form)
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel)
        
    def create_left_panel(self):
        """Create the left panel with branding."""
        left_panel = QFrame()
        left_panel.setObjectName("left-panel")
        left_panel.setFixedWidth(600)  # Increased width
        
        layout = QVBoxLayout(left_panel)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(30)  # Increased spacing
        
        # Add logo
        logo_label = QLabel()
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                'resources', 'images', 'logo_large.png')
        pixmap = QPixmap(logo_path)
        if pixmap:
            scaled_pixmap = pixmap.scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
        
        # Add welcome text
        welcome_label = QLabel("Welcome to DisasterConnect")
        welcome_label.setObjectName("welcome-text")
        welcome_label.setAlignment(Qt.AlignCenter)
        
        description_label = QLabel("Your comprehensive disaster management solution")
        description_label.setObjectName("description-text")
        description_label.setAlignment(Qt.AlignCenter)
        
        layout.addStretch(1)
        layout.addWidget(logo_label)
        layout.addWidget(welcome_label)
        layout.addWidget(description_label)
        layout.addStretch(1)
        
        return left_panel
    
    def create_right_panel(self):
        """Create the right panel with login form."""
        right_panel = QFrame()
        right_panel.setObjectName("right-panel")
        right_panel.setFixedWidth(600)  # Increased width
        
        layout = QVBoxLayout(right_panel)
        layout.setAlignment(Qt.AlignCenter)
        
        # Create login form container
        form_container = QFrame()
        form_container.setObjectName("form-container")
        form_container.setFixedWidth(450)  # Increased width
        
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(25)  # Increased spacing
        form_layout.setContentsMargins(50, 50, 50, 50)  # Increased padding
        
        # Login title
        title = QLabel("Login to your account")
        title.setObjectName("form-title")
        title.setAlignment(Qt.AlignCenter)
        
        # Username field
        username_label = QLabel("Username")
        username_label.setObjectName("input-label")
        self.username_input = QLineEdit()
        self.username_input.setObjectName("input-field")
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setFixedHeight(50)  # Increased height
        
        # Password field
        password_label = QLabel("Password")
        password_label.setObjectName("input-label")
        self.password_input = QLineEdit()
        self.password_input.setObjectName("input-field")
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(50)  # Increased height
        
        # Login button
        login_button = QPushButton("Login")
        login_button.setObjectName("primary-button")
        login_button.setFixedHeight(50)  # Increased height
        login_button.clicked.connect(self.handle_login)
        
        # Forgot password button
        forgot_button = QPushButton("Forgot Password?")
        forgot_button.setObjectName("text-button")
        forgot_button.clicked.connect(self.show_forgot_password)
        
        # Sign up section
        signup_container = QFrame()
        signup_container.setObjectName("signup-container")
        signup_layout = QVBoxLayout(signup_container)
        signup_layout.setSpacing(10)
        
        signup_label = QLabel("Don't have an account?")
        signup_label.setObjectName("signup-text")
        signup_label.setAlignment(Qt.AlignCenter)
        
        signup_button = QPushButton("Sign Up")
        signup_button.setObjectName("text-button")
        signup_button.clicked.connect(self.show_signup)
        
        # Add all elements to form
        form_layout.addWidget(title)
        form_layout.addSpacing(20)
        form_layout.addWidget(username_label)
        form_layout.addWidget(self.username_input)
        form_layout.addSpacing(15)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)
        form_layout.addSpacing(30)
        form_layout.addWidget(login_button)
        form_layout.addSpacing(20)
        form_layout.addWidget(forgot_button, alignment=Qt.AlignCenter)
        form_layout.addSpacing(10)
        
        signup_layout.addWidget(signup_label)
        signup_layout.addWidget(signup_button)
        form_layout.addWidget(signup_container)
        
        # Add form to right panel
        layout.addWidget(form_container)
        
        return right_panel
    
    def setup_styles(self):
        """Setup the stylesheet for the window."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f6fa;
            }
            
            #left-panel {
                background-color: #2C3E50;
                border: none;
            }
            
            #right-panel {
                background-color: white;
                border: none;
            }
            
            #welcome-text {
                color: white;
                font-size: 32px;
                font-weight: bold;
                margin: 20px 0;
            }
            
            #description-text {
                color: #bdc3c7;
                font-size: 18px;
            }
            
            #form-container {
                background-color: white;
                border-radius: 15px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            
            #form-title {
                color: #2C3E50;
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 20px;
            }
            
            #input-label {
                color: #2C3E50;
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            
            #input-field {
                padding: 15px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 16px;
                background-color: #f8f9fa;
            }
            
            #input-field:focus {
                border: 2px solid #3498db;
                outline: none;
                background-color: white;
            }
            
            #primary-button {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 18px;
                font-weight: bold;
                padding: 12px;
            }
            
            #primary-button:hover {
                background-color: #2980b9;
                cursor: pointer;
            }
            
            #text-button {
                background: none;
                border: none;
                color: #3498db;
                font-size: 16px;
                padding: 10px;
                margin: 5px;
            }
            
            #text-button:hover {
                color: #2980b9;
                text-decoration: underline;
                cursor: pointer;
            }
            
            #signup-text {
                color: #7f8c8d;
                font-size: 16px;
                margin: 5px;
            }
            
            #signup-container {
                margin-top: 10px;
                padding: 10px;
            }
            
            QLabel, QPushButton, QLineEdit {
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
    
    def handle_login(self):
        """Handle login button click."""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Login Error", 
                              "Please enter both username and password.",
                              QMessageBox.Ok)
            return
        
        # For testing, allow any login
        user_data = {"username": username}
        self.login_successful.emit(user_data)
    
    def show_signup(self):
        """Show signup window."""
        pass  # TODO: Implement signup window
    
    def show_forgot_password(self):
        """Show forgot password window."""
        pass  # TODO: Implement forgot password window
