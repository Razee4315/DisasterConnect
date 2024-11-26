from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from ..dashboard.dashboard_widget import DashboardWidget
from ..incidents.incidents_widget import IncidentsWidget
from ..resources.resources_widget import ResourcesWidget
from ..auth.login_widget import LoginWidget
from ..utils.mongodb_client import mongodb_client

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DisasterConnect")
        self.setGeometry(100, 100, 1200, 800)
        
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
        # Refresh data in all tabs
        self.dashboard.refresh_data()
        self.incidents.refresh_data()
        self.resources.refresh_data()
