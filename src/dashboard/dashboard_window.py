from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QTabWidget, QFrame, QScrollArea,
                             QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from ui.incident_window import IncidentWindow
from ui.resource_window import ResourceWindow
from ui.reporting_window import ReportingWindow

class DashboardWindow(QMainWindow):
    def __init__(self, auth_manager):
        super().__init__()
        self.auth_manager = auth_manager
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("DisasterConnect Dashboard")
        self.resize(1200, 800)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Header with welcome message
        header = QHBoxLayout()
        welcome_label = QLabel(f"Welcome, {self.auth_manager.current_user['username']}!")
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        header.addWidget(welcome_label)
        header.addStretch()
        
        # Create tab widget
        tab_widget = QTabWidget()
        
        # Overview tab (placeholder for now)
        overview_tab = QWidget()
        overview_layout = QVBoxLayout(overview_tab)
        overview_layout.addWidget(QLabel("Overview Dashboard - Coming Soon"))
        tab_widget.addTab(overview_tab, "Overview")
        
        # Incidents tab
        incidents_tab = IncidentWindow()
        tab_widget.addTab(incidents_tab, "Incidents")
        
        # Resources tab
        resources_tab = ResourceWindow()
        tab_widget.addTab(resources_tab, "Resources")
        
        # Reports tab
        reports_tab = ReportingWindow()
        tab_widget.addTab(reports_tab, "Reports")
        
        # Add components to main layout
        layout.addLayout(header)
        layout.addWidget(tab_widget)
        
        # Set window style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QTabWidget::pane {
                border: 1px solid #cccccc;
                background: white;
            }
            QTabWidget::tab-bar {
                left: 5px;
            }
            QTabBar::tab {
                background: #e0e0e0;
                border: 1px solid #c0c0c0;
                padding: 8px 12px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #0078d4;
                color: white;
            }
            QLabel {
                color: #333333;
            }
        """)
