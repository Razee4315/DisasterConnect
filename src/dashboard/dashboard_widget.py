from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QFrame)
from PyQt5.QtCore import Qt
from ..utils.mongodb_client import mongodb_client
from ..utils.map_client import map_client
import json
from bson import ObjectId
from datetime import datetime

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

class DashboardWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """Initialize the dashboard UI"""
        layout = QHBoxLayout()
        
        # Left panel for statistics
        left_panel = QFrame()
        left_panel.setFrameStyle(QFrame.StyledPanel)
        left_layout = QVBoxLayout(left_panel)
        
        # Statistics
        stats_label = QLabel("Statistics")
        stats_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        left_layout.addWidget(stats_label)
        
        # Statistics labels
        self.total_incidents_label = QLabel("Total Incidents: 0")
        self.active_incidents_label = QLabel("Active Incidents: 0")
        self.total_resources_label = QLabel("Total Resources: 0")
        self.available_resources_label = QLabel("Available Resources: 0")
        
        left_layout.addWidget(self.total_incidents_label)
        left_layout.addWidget(self.active_incidents_label)
        left_layout.addWidget(self.total_resources_label)
        left_layout.addWidget(self.available_resources_label)
        
        # Add buttons
        self.add_action_buttons(left_layout)
        
        left_layout.addStretch()
        layout.addWidget(left_panel, 1)
        
        # Right panel for map
        right_panel = QFrame()
        right_panel.setFrameStyle(QFrame.StyledPanel)
        right_layout = QVBoxLayout(right_panel)
        
        # Map widget
        self.map_widget = map_client.create_map_widget()
        right_layout.addWidget(self.map_widget)
        
        layout.addWidget(right_panel, 2)
        self.setLayout(layout)
        
        # Load initial data
        self.refresh_data()
        
    def add_action_buttons(self, layout):
        """Add action buttons to the layout"""
        # New Incident button
        new_incident_btn = QPushButton("Report New Incident")
        new_incident_btn.clicked.connect(self.report_incident)
        new_incident_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        layout.addWidget(new_incident_btn)
        
        # Manage Resources button
        manage_resources_btn = QPushButton("Manage Resources")
        manage_resources_btn.clicked.connect(self.manage_resources)
        manage_resources_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        layout.addWidget(manage_resources_btn)
        
    def refresh_data(self):
        """Refresh dashboard data"""
        try:
            # Clear existing markers
            self.map_widget.clear_markers()
            
            # Update incidents
            incidents = list(mongodb_client.db.incidents.find()) or []
            active_incidents = [i for i in incidents if i.get("status") != "Resolved"]
            
            self.total_incidents_label.setText(f"Total Incidents: {len(incidents)}")
            self.active_incidents_label.setText(f"Active Incidents: {len(active_incidents)}")
            
            # Add incident markers
            for incident in incidents:
                location = incident.get("location", {})
                if location and "lat" in location and "lng" in location:
                    self.map_widget.add_incident_marker(
                        location["lat"],
                        location["lng"],
                        {
                            "title": incident.get("title", "Untitled"),
                            "type": incident.get("type", "Unknown"),
                            "severity": incident.get("severity", "Unknown"),
                            "status": incident.get("status", "Unknown")
                        }
                    )
            
            # Update resources
            resources = list(mongodb_client.db.resources.find()) or []
            available_resources = [r for r in resources if r.get("status") == "Available"]
            
            self.total_resources_label.setText(f"Total Resources: {len(resources)}")
            self.available_resources_label.setText(f"Available Resources: {len(available_resources)}")
            
            # Add resource markers
            for resource in resources:
                location = resource.get("location", {})
                if location and "lat" in location and "lng" in location:
                    self.map_widget.add_resource_marker(
                        location["lat"],
                        location["lng"],
                        {
                            "name": resource.get("name", "Untitled"),
                            "type": resource.get("type", "Unknown"),
                            "status": resource.get("status", "Unknown"),
                            "capacity": resource.get("capacity", 0)
                        }
                    )
                    
        except Exception as e:
            print(f"Error refreshing dashboard data: {e}")
            
    def report_incident(self):
        """Switch to the incidents tab"""
        main_window = self.get_main_window()
        if main_window:
            main_window.tab_widget.setCurrentIndex(1)  # Switch to Incidents tab
            
    def manage_resources(self):
        """Switch to the resources tab"""
        main_window = self.get_main_window()
        if main_window:
            main_window.tab_widget.setCurrentIndex(2)  # Switch to Resources tab
            
    def get_main_window(self):
        """Get reference to main window"""
        parent = self.parent()
        while parent:
            if hasattr(parent, 'tab_widget'):
                return parent
            parent = parent.parent()
        return None
