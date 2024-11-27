from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QFrame, QGroupBox, QCheckBox)

from ..utils.mongodb_client import mongodb_client
from ..utils.map_client import map_client

import json
import os
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
        
        # Add logo at the top
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                               'resources', 'images', 'logo_new.svg')
        if os.path.exists(logo_path):
            logo_label = QLabel()
            logo_pixmap = QPixmap(logo_path)
            scaled_pixmap = logo_pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
            left_layout.addWidget(logo_label)
            
        # Add refresh button at the top
        refresh_button = QPushButton("Refresh Dashboard")
        refresh_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        refresh_button.clicked.connect(self.refresh_data)
        left_layout.addWidget(refresh_button)
        
        # Add map controls section
        map_controls_group = QGroupBox("Map Controls")
        map_controls_layout = QVBoxLayout()
        
        # Clustering toggle
        self.cluster_checkbox = QCheckBox("Enable Clustering")
        self.cluster_checkbox.setChecked(True)
        self.cluster_checkbox.stateChanged.connect(self.toggle_clustering)
        map_controls_layout.addWidget(self.cluster_checkbox)
        
        # Heatmap toggle
        self.heatmap_checkbox = QCheckBox("Show Heatmap")
        self.heatmap_checkbox.setChecked(False)
        self.heatmap_checkbox.stateChanged.connect(self.toggle_heatmap)
        map_controls_layout.addWidget(self.heatmap_checkbox)
        
        # Alert radius toggle
        self.alert_radius_checkbox = QCheckBox("Show Alert Radius")
        self.alert_radius_checkbox.setChecked(True)
        self.alert_radius_checkbox.stateChanged.connect(self.toggle_alert_radius)
        map_controls_layout.addWidget(self.alert_radius_checkbox)
        
        map_controls_group.setLayout(map_controls_layout)
        left_layout.addWidget(map_controls_group)
        
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
    
    def toggle_clustering(self, state):
        """Toggle marker clustering"""
        self.map_widget.toggle_clustering(state == Qt.Checked)
        self.refresh_data()
    
    def toggle_heatmap(self, state):
        """Toggle heatmap layer"""
        try:
            if state == Qt.Checked:
                print("Enabling heatmap...")
                # Prepare heatmap data from incidents
                heatmap_points = []
                incidents = list(mongodb_client.db.incidents.find()) or []
                
                if not incidents:
                    print("No incidents found for heatmap")
                    self.heatmap_checkbox.setChecked(False)
                    return
                
                for incident in incidents:
                    location = incident.get("location", {})
                    severity = incident.get("severity", "Low")
                    status = incident.get("status", "Active")
                    
                    if location and "lat" in location and "lng" in location:
                        # Base intensity on severity
                        base_intensity = {
                            "Critical": 1.0,
                            "High": 0.7,
                            "Medium": 0.5,
                            "Low": 0.3
                        }.get(severity, 0.3)
                        
                        # Reduce intensity for resolved incidents
                        if status == "Resolved":
                            base_intensity *= 0.5
                        
                        heatmap_points.append({
                            "lat": location["lat"],
                            "lng": location["lng"],
                            "intensity": base_intensity
                        })
                
                if heatmap_points:
                    print(f"Updating heatmap with {len(heatmap_points)} points")
                    self.map_widget.update_heatmap(heatmap_points)
                else:
                    print("No valid points for heatmap")
                    self.heatmap_checkbox.setChecked(False)
            else:
                print("Disabling heatmap...")
                self.map_widget.update_heatmap([])
                
        except Exception as e:
            print(f"Error updating heatmap: {e}")
            self.heatmap_checkbox.setChecked(False)
    
    def toggle_alert_radius(self, state):
        """Toggle alert radius circles"""
        try:
            incidents = list(mongodb_client.db.incidents.find()) or []
            for incident in incidents:
                location = incident.get("location", {})
                if location and "lat" in location and "lng" in location:
                    severity = incident.get("severity", "Low")
                    # Adjust radius based on severity
                    radius = {
                        "Critical": 5000,  # 5km
                        "High": 3000,      # 3km
                        "Medium": 2000,    # 2km
                        "Low": 1000        # 1km
                    }.get(severity, 1000)
                    
                    if state == Qt.Checked:
                        self.map_widget.update_alert_radius(
                            location["lat"],
                            location["lng"],
                            radius,
                            {
                                "severity": severity,
                                "title": incident.get("title", "Untitled"),
                                "type": incident.get("type", "Unknown")
                            }
                        )
                    else:
                        self.map_widget.update_alert_radius(
                            location["lat"],
                            location["lng"],
                            0,  # 0 radius to hide
                            {}
                        )
        except Exception as e:
            print(f"Error updating alert radius: {e}")
