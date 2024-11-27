from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QWidget, 
                             QVBoxLayout, QHBoxLayout, QPushButton)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from ..dashboard.dashboard_widget import DashboardWidget
from ..incidents.incidents_widget import IncidentsWidget
from ..resources.resources_widget import ResourcesWidget
from ..auth.login_widget import LoginWidget
from ..utils.mongodb_client import mongodb_client
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DisasterConnect")
        # Set initial size for login window
        self.setGeometry(100, 100, 400, 500)
        
        # Set window icon
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                               'resources', 'images', 'logo_new.svg')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Initialize central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # Initialize authentication
        self.login_widget = LoginWidget(self)
        self.login_widget.login_success.connect(self.on_login_success)  # Connect the signal
        self.layout.addWidget(self.login_widget)
        
        # Initialize main content (hidden initially)
        self.main_content = QWidget()
        self.main_layout = QVBoxLayout(self.main_content)
        
        # Add logout button in a horizontal layout at the top
        top_bar = QHBoxLayout()
        top_bar.addStretch()  # Push the logout button to the right
        
        self.logout_button = QPushButton("Logout")
        self.logout_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        self.logout_button.clicked.connect(self.logout)
        top_bar.addWidget(self.logout_button)
        
        self.main_layout.addLayout(top_bar)
        
        # Add tab widget
        self.tab_widget = QTabWidget()
        self.main_layout.addWidget(self.tab_widget)
        self.layout.addWidget(self.main_content)
        self.main_content.hide()
        
        # Initialize tabs
        self.init_tabs()
    
    def init_tabs(self):
        """Initialize application tabs"""
        # Dashboard Tab
        self.dashboard = DashboardWidget()
        self.tab_widget.addTab(self.dashboard, "Dashboard")
        
        # Incidents Tab
        self.incidents = IncidentsWidget()
        self.tab_widget.addTab(self.incidents, "Incidents")
        
        # Resources Tab
        self.resources = ResourcesWidget()
        self.tab_widget.addTab(self.resources, "Resources")
    
    def on_login_success(self, user_data):
        """Handle successful login"""
        print(f"Login successful for user: {user_data.get('username')}")  # Debug print
        self.login_widget.hide()
        self.main_content.show()
        # Set window to maximum size after login
        self.showMaximized()
        # Update window title with username
        self.setWindowTitle(f"DisasterConnect - Welcome {user_data.get('username')}")
        # Refresh data in all tabs
        self.dashboard.refresh_data()
        self.incidents.refresh_data()
        self.resources.refresh_table()
    
    def logout(self):
        """Handle logout"""
        # Hide main content and show login widget
        self.main_content.hide()
        self.login_widget.show()
        self.login_widget.clear_fields()  # Clear the login fields
        self.setWindowTitle("DisasterConnect")  # Reset window title
