"""Main entry point for DisasterConnect application."""
import sys
import os
from dotenv import load_dotenv
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, 
                           QVBoxLayout, QStackedWidget)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon

from src.auth.auth_manager import AuthManager
from src.auth.login_window import LoginWindow
from src.dashboard.dashboard_window import DashboardWindow
from src.widgets.splash_screen import SplashScreen
from src.styles import get_app_stylesheet

# Load environment variables
load_dotenv()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DisasterConnect")
        self.setMinimumSize(1200, 800)
        
        # Set window icon
        icon_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'images', 'logo_icon.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Initialize authentication manager
        self.auth_manager = AuthManager()
        
        # Create central widget and main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Create stacked widget for different pages
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)
        
        # Initialize UI components
        self.setup_ui()
        
    def setup_ui(self):
        """Initialize all UI components"""
        # Create login window
        self.login_window = LoginWindow(auth_manager=self.auth_manager)
        self.login_window.login_successful.connect(self.on_login_successful)
        self.stacked_widget.addWidget(self.login_window)
        
        # Create dashboard window
        self.dashboard_window = DashboardWindow(auth_manager=self.auth_manager)
        self.stacked_widget.addWidget(self.dashboard_window)
        
        # Set initial page
        self.stacked_widget.setCurrentWidget(self.login_window)
    
    def on_login_successful(self, user_data):
        """Handle successful login"""
        # Switch to dashboard view
        self.stacked_widget.setCurrentWidget(self.dashboard_window)
        # Set window to full screen
        self.showMaximized()
        # Update window title
        self.setWindowTitle(f"DisasterConnect - Welcome {user_data['username']}")

def main():
    # Create application
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for a modern look
    
    # Set application icon
    icon_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'images', 'logo_icon.png')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # Show splash screen
    splash = SplashScreen()
    splash.show()
    
    # Process events to show splash immediately
    app.processEvents()
    
    # Create and setup main window
    window = MainWindow()
    
    # Close splash and show main window after 4 seconds
    def show_main_window():
        splash.finish(window)
        window.show()
    
    timer = QTimer()
    timer.singleShot(4000, show_main_window)
    
    # Apply application stylesheet
    app.setStyleSheet(get_app_stylesheet())
    
    # Start event loop
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
