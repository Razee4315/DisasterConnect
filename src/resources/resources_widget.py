from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QDialog, QLabel,
                             QLineEdit, QComboBox, QSpinBox, QTextEdit)
from PyQt5.QtCore import Qt, pyqtSignal
from ..utils.map_client import map_client
from ..utils.mongodb_client import mongodb_client
from ..utils.location_picker import pick_location
from datetime import datetime
from bson import ObjectId

class ResourceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Resource")
        self.setModal(True)
        self.setMinimumWidth(400)
        self.setMinimumHeight(600)
        
        # Main layout
        layout = QVBoxLayout(self)
        
        # Add form fields
        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        
        self.type_label = QLabel("Type:")
        self.type_input = QComboBox()
        self.type_input.addItems(["Medical", "Food", "Water", "Shelter", "Transportation", "Other"])
        layout.addWidget(self.type_label)
        layout.addWidget(self.type_input)
        
        self.status_label = QLabel("Status:")
        self.status_input = QComboBox()
        self.status_input.addItems(["Available", "In Use", "Unavailable"])
        layout.addWidget(self.status_label)
        layout.addWidget(self.status_input)
        
        self.capacity_label = QLabel("Capacity:")
        self.capacity_input = QSpinBox()
        self.capacity_input.setRange(1, 1000)
        layout.addWidget(self.capacity_label)
        layout.addWidget(self.capacity_input)
        
        self.description_label = QLabel("Description:")
        self.description_input = QTextEdit()
        layout.addWidget(self.description_label)
        layout.addWidget(self.description_input)
        
        # Location selection
        location_layout = QHBoxLayout()
        self.location_label = QLabel("Location: Not selected")
        self.location_label.setStyleSheet("color: #666;")
        self.pick_location_btn = QPushButton("Pick Location")
        self.pick_location_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.pick_location_btn.clicked.connect(self.pick_location)
        location_layout.addWidget(self.location_label)
        location_layout.addWidget(self.pick_location_btn)
        layout.addLayout(location_layout)
        
        # Add buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.save_button.setEnabled(False)
        self.cancel_button = QPushButton("Cancel")
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        # Set up button connections
        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        
        # Initialize location
        self.selected_location = None
    
    def pick_location(self):
        """Open location picker dialog"""
        location = pick_location(self)
        if location:
            self.selected_location = location
            self.location_label.setText(f"Location: ({location['lat']:.6f}, {location['lng']:.6f})")
            self.location_label.setStyleSheet("color: green;")
            self.save_button.setEnabled(True)
    
    def get_resource_data(self):
        """Get the resource data from the form"""
        if not self.selected_location:
            return None
            
        return {
            "name": self.name_input.text(),
            "type": self.type_input.currentText(),
            "status": self.status_input.currentText(),
            "capacity": self.capacity_input.value(),
            "description": self.description_input.toPlainText(),
            "location": self.selected_location,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

class ResourcesWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        
        # Add resource button
        self.add_button = QPushButton("Add Resource")
        self.add_button.clicked.connect(self.add_resource)
        layout.addWidget(self.add_button)
        
        # Resources table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Name", "Type", "Status", "Capacity", "Location", "Created At"])
        layout.addWidget(self.table)
        
        # Map widget
        self.map_widget = map_client.create_map_widget()
        layout.addWidget(self.map_widget)
        
        self.refresh_data()
        
    def add_resource(self):
        """Open dialog to add a new resource"""
        dialog = ResourceDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            resource_data = dialog.get_resource_data()
            if resource_data:
                # Save to database
                result = mongodb_client.db.resources.insert_one(resource_data)
                if result.inserted_id:
                    self.refresh_data()
                
    def refresh_data(self):
        """Refresh the resources data"""
        try:
            # Clear existing data
            self.table.setRowCount(0)
            self.map_widget.clear_markers()
            
            # Fetch resources from database
            resources = list(mongodb_client.db.resources.find()) or []
            
            # Update table and map
            for resource in resources:
                try:
                    row = self.table.rowCount()
                    self.table.insertRow(row)
                    
                    # Add to table
                    self.table.setItem(row, 0, QTableWidgetItem(resource.get("name", "Untitled")))
                    self.table.setItem(row, 1, QTableWidgetItem(resource.get("type", "Unknown")))
                    self.table.setItem(row, 2, QTableWidgetItem(resource.get("status", "Unknown")))
                    self.table.setItem(row, 3, QTableWidgetItem(str(resource.get("capacity", 0))))
                    
                    # Handle location data safely
                    location = resource.get("location", {})
                    if location and "lat" in location and "lng" in location:
                        self.table.setItem(row, 4, QTableWidgetItem(f"({location['lat']:.6f}, {location['lng']:.6f})"))
                        
                        # Add to map
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
                    else:
                        self.table.setItem(row, 4, QTableWidgetItem("No location"))
                    
                    # Handle date safely
                    created_at = resource.get("created_at")
                    if created_at:
                        self.table.setItem(row, 5, QTableWidgetItem(created_at.strftime("%Y-%m-%d %H:%M")))
                    else:
                        self.table.setItem(row, 5, QTableWidgetItem("Unknown"))
                        
                except Exception as e:
                    print(f"Error processing resource: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error refreshing resources data: {e}")
