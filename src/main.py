import sys
import os
from dotenv import load_dotenv
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, 
                           QVBoxLayout, QStackedWidget)
from PyQt5.QtCore import Qt

from auth.auth_manager import AuthManager
from auth.login_window import LoginWindow
from dashboard.dashboard_window import DashboardWindow
from styles import get_app_stylesheet

# Load environment variables
load_dotenv()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DisasterConnect")
        self.setMinimumSize(1200, 800)
        
        # Initialize authentication manager
        self.auth_manager = AuthManager()
        
        # Create central widget and main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # Create stacked widget for different pages
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)
        
        # Initialize UI components
        self.setup_ui()
        
    def setup_ui(self):
        """Initialize all UI components"""
        # Create login window
        self.login_window = LoginWindow(self.auth_manager)
        self.login_window.login_successful.connect(self.on_login_successful)
        self.stacked_widget.addWidget(self.login_window)
        
        # Create dashboard window
        self.dashboard_window = DashboardWindow(self.auth_manager)
        self.stacked_widget.addWidget(self.dashboard_window)
        
    def on_login_successful(self, user_data):
        """Handle successful login"""
        # Switch to dashboard view
        self.stacked_widget.setCurrentWidget(self.dashboard_window)

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for a modern look
    
    # Apply application stylesheet
    app.setStyleSheet(get_app_stylesheet())
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
