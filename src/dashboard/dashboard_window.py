"""Main dashboard window for DisasterConnect."""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QLabel, QPushButton, QFrame, QStackedWidget,
                           QScrollArea, QSizePolicy, QGridLayout, QSpacerItem)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon, QFont, QColor, QPainter
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
import os
from datetime import datetime
from src.utils.map_client import map_client
from src.dashboard.incident_widget import IncidentWidget
from src.dashboard.resource_widget import ResourceWidget
from src.dashboard.alert_widget import AlertWidget

class DashboardWindow(QMainWindow):
    """Main dashboard window for the application."""
    
    def __init__(self, auth_manager=None):
        super().__init__()
        self.auth_manager = auth_manager
        self.setWindowTitle("DisasterConnect - Dashboard")
        self.setMinimumSize(1200, 800)
        
        # Set window icon
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                'resources', 'images', 'logo_small.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Initialize UI components
        self.init_ui()
        
        # Start auto-refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_dashboard)
        self.refresh_timer.start(30000)  # Refresh every 30 seconds
    
    def init_ui(self):
        """Initialize the dashboard UI."""
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create sidebar
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)
        
        # Create main content area
        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack)
        
        # Add different views to the stack
        self.overview_page = self.create_overview_page()
        self.incident_page = IncidentWidget(self.auth_manager)
        self.resource_page = ResourceWidget(self.auth_manager)
        self.alert_page = AlertWidget(self.auth_manager)
        
        self.content_stack.addWidget(self.overview_page)
        self.content_stack.addWidget(self.incident_page)
        self.content_stack.addWidget(self.resource_page)
        self.content_stack.addWidget(self.alert_page)
        
        # Set the stylesheet
        self.setStyleSheet(self.get_stylesheet())
    
    def create_sidebar(self):
        """Create the sidebar with navigation buttons."""
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Add logo
        logo_container = QFrame()
        logo_container.setObjectName("logo-container")
        logo_container.setFixedHeight(100)
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setAlignment(Qt.AlignCenter)
        
        # Add logo image
        logo_image = QLabel()
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                'resources', 'images', 'logo_medium.png')
        if os.path.exists(logo_path):
            logo_image.setPixmap(QIcon(logo_path).pixmap(64, 64))
            logo_image.setAlignment(Qt.AlignCenter)
        
        # Add logo text
        logo_label = QLabel("DisasterConnect")
        logo_label.setObjectName("logo-text")
        logo_label.setAlignment(Qt.AlignCenter)
        
        logo_layout.addWidget(logo_image)
        logo_layout.addWidget(logo_label)
        
        layout.addWidget(logo_container)
        
        # Add navigation buttons
        nav_buttons = [
            ("Overview", lambda: self.content_stack.setCurrentIndex(0)),
            ("Incidents", lambda: self.content_stack.setCurrentIndex(1)),
            ("Resources", lambda: self.content_stack.setCurrentIndex(2)),
            ("Alerts", lambda: self.content_stack.setCurrentIndex(3))
        ]
        
        for text, callback in nav_buttons:
            btn = QPushButton(text)
            btn.setObjectName("nav-button")
            btn.clicked.connect(callback)
            layout.addWidget(btn)
        
        # Add spacer
        layout.addStretch()
        
        # Add user info
        if self.auth_manager and self.auth_manager.current_user:
            user_frame = QFrame()
            user_frame.setObjectName("user-info")
            user_layout = QVBoxLayout(user_frame)
            
            user_name = QLabel(f"{self.auth_manager.current_user.get('first_name', '')} "
                             f"{self.auth_manager.current_user.get('last_name', '')}")
            user_name.setObjectName("user-name")
            
            user_role = QLabel(self.auth_manager.current_user.get('role', 'User'))
            user_role.setObjectName("user-role")
            
            user_layout.addWidget(user_name)
            user_layout.addWidget(user_role)
            
            layout.addWidget(user_frame)
        
        return sidebar
    
    def create_overview_page(self):
        """Create the overview dashboard page."""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Header
        header = QFrame()
        header.setObjectName("page-header")
        header_layout = QHBoxLayout(header)
        
        title = QLabel("Dashboard Overview")
        title.setObjectName("page-title")
        header_layout.addWidget(title)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setObjectName("refresh-button")
        refresh_btn.clicked.connect(self.refresh_dashboard)
        header_layout.addWidget(refresh_btn, alignment=Qt.AlignRight)
        
        layout.addWidget(header)
        
        # Main content
        content = QScrollArea()
        content.setWidgetResizable(True)
        content.setObjectName("content-area")
        
        content_widget = QWidget()
        content_layout = QGridLayout(content_widget)
        
        # Add statistics cards
        stats_cards = [
            ("Active Incidents", "25", "warning"),
            ("Available Resources", "150", "success"),
            ("Active Alerts", "10", "danger"),
            ("Response Teams", "8", "info")
        ]
        
        for i, (title, value, status) in enumerate(stats_cards):
            card = self.create_stat_card(title, value, status)
            content_layout.addWidget(card, 0, i)
        
        # Add charts
        incident_chart = self.create_incident_chart()
        resource_chart = self.create_resource_chart()
        
        content_layout.addWidget(incident_chart, 1, 0, 1, 2)
        content_layout.addWidget(resource_chart, 1, 2, 1, 2)
        
        # Add map widget
        map_widget = map_client.create_map_widget()
        map_widget.setMinimumHeight(400)
        content_layout.addWidget(map_widget, 2, 0, 1, 4)
        
        content.setWidget(content_widget)
        layout.addWidget(content)
        
        return page
    
    def create_stat_card(self, title, value, status):
        """Create a statistics card widget."""
        card = QFrame()
        card.setObjectName(f"stat-card-{status}")
        layout = QVBoxLayout(card)
        
        value_label = QLabel(value)
        value_label.setObjectName("stat-value")
        
        title_label = QLabel(title)
        title_label.setObjectName("stat-title")
        
        layout.addWidget(value_label)
        layout.addWidget(title_label)
        
        return card
    
    def create_incident_chart(self):
        """Create incident distribution chart."""
        # Create chart
        chart = QChart()
        chart.setTitle("Incident Distribution")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        
        # Create pie series
        series = QPieSeries()
        series.append("Natural", 35)
        series.append("Man-made", 25)
        series.append("Health", 20)
        series.append("Other", 20)
        
        # Add series to chart
        chart.addSeries(series)
        chart.legend().setAlignment(Qt.AlignRight)
        
        # Create chart view
        chart_view = QChartView(chart)
        chart_view.setMinimumHeight(300)
        chart_view.setRenderHints(QPainter.Antialiasing)
        
        return chart_view
    
    def create_resource_chart(self):
        """Create resource allocation chart."""
        # Create chart
        chart = QChart()
        chart.setTitle("Resource Allocation")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        
        # Create bar series
        series = QBarSeries()
        
        # Add data
        set0 = QBarSet("Available")
        set1 = QBarSet("Deployed")
        set0.append([80, 65, 45, 70])
        set1.append([20, 35, 55, 30])
        series.append(set0)
        series.append(set1)
        
        # Set up axes
        categories = ["Medical", "Transport", "Rescue", "Supply"]
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)
        
        axis_y = QValueAxis()
        axis_y.setRange(0, 100)
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)
        
        # Add series to chart
        chart.addSeries(series)
        chart.legend().setAlignment(Qt.AlignBottom)
        
        # Create chart view
        chart_view = QChartView(chart)
        chart_view.setMinimumHeight(300)
        chart_view.setRenderHints(QPainter.Antialiasing)
        
        return chart_view
    
    def refresh_dashboard(self):
        """Refresh dashboard data."""
        # TODO: Implement dashboard refresh logic
        pass
    
    def get_stylesheet(self):
        """Return the stylesheet for the dashboard."""
        return """
            QMainWindow {
                background-color: #f5f6fa;
            }
            
            #sidebar {
                background-color: #2C3E50;
                border: none;
            }
            
            #logo-container {
                background-color: #34495e;
                padding: 15px;
                margin-bottom: 10px;
            }
            
            #logo-text {
                color: white;
                font-size: 16px;
                font-weight: bold;
                margin-top: 5px;
            }
            
            #nav-button {
                background-color: transparent;
                border: none;
                color: #ecf0f1;
                padding: 15px 20px;
                text-align: left;
                font-size: 14px;
            }
            
            #nav-button:hover {
                background-color: #34495e;
            }
            
            #overview-container {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
                margin: 20px;
            }
            
            #page-header {
                background-color: white;
                padding: 20px;
                border-bottom: 1px solid #e0e0e0;
            }
            
            #page-title {
                font-size: 24px;
                font-weight: bold;
                color: #202124;
            }
            
            #refresh-button {
                background-color: #1a73e8;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            
            #refresh-button:hover {
                background-color: #1557b0;
            }
            
            #content-area {
                background-color: #f8f9fa;
                border: none;
            }
            
            #stat-card-warning, #stat-card-success, #stat-card-danger, #stat-card-info {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
                margin: 10px;
            }
            
            #stat-card-warning {
                border-left: 4px solid #ffc107;
            }
            
            #stat-card-success {
                border-left: 4px solid #28a745;
            }
            
            #stat-card-danger {
                border-left: 4px solid #dc3545;
            }
            
            #stat-card-info {
                border-left: 4px solid #17a2b8;
            }
            
            #stat-value {
                font-size: 32px;
                font-weight: bold;
                color: #202124;
            }
            
            #stat-title {
                font-size: 14px;
                color: #5f6368;
                margin-top: 5px;
            }
        """
