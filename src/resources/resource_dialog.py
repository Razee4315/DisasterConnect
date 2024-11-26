from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                            QLineEdit, QComboBox, QPushButton, QFormLayout,
                            QTextEdit, QMessageBox, QTableWidget, QTableWidgetItem,
                            QWidget)
from PyQt5.QtCore import Qt, pyqtSlot
from ..utils.mongodb_client import mongodb_client
from ..utils.map_client import map_client
from datetime import datetime
import json
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

class ResourceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Manage Resources")
        self.setModal(True)
        self.init_ui()
        
    def init_ui(self):
        main_layout = QHBoxLayout()
        
        # Left panel for form and table
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Resource List
        self.resource_table = QTableWidget()
        self.resource_table.setColumnCount(6)
        self.resource_table.setHorizontalHeaderLabels([
            "Name", "Type", "Status", "Location", "Capacity", "Actions"
        ])
        left_layout.addWidget(self.resource_table)
        
        # Add Resource Form
        form_layout = QFormLayout()
        
        # Name
        self.name_edit = QLineEdit()
        form_layout.addRow("Name:", self.name_edit)
        
        # Type
        self.type_combo = QComboBox()
        self.type_combo.addItems([
            "Medical",
            "Fire Fighting",
            "Search and Rescue",
            "Transportation",
            "Shelter",
            "Food and Water",
            "Other"
        ])
        form_layout.addRow("Type:", self.type_combo)
        
        # Status
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Available", "In Use", "Maintenance"])
        form_layout.addRow("Status:", self.status_combo)
        
        # Location
        location_widget = QWidget()
        location_layout = QHBoxLayout(location_widget)
        
        self.lat_edit = QLineEdit()
        self.lat_edit.setPlaceholderText("Latitude")
        self.lat_edit.setReadOnly(True)
        
        self.lng_edit = QLineEdit()
        self.lng_edit.setPlaceholderText("Longitude")
        self.lng_edit.setReadOnly(True)
        
        location_layout.addWidget(self.lat_edit)
        location_layout.addWidget(self.lng_edit)
        
        form_layout.addRow("Location:", location_widget)
        
        # Capacity
        self.capacity_edit = QLineEdit()
        form_layout.addRow("Capacity:", self.capacity_edit)
        
        # Description
        self.description_edit = QTextEdit()
        form_layout.addRow("Description:", self.description_edit)
        
        left_layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        add_button = QPushButton("Add Resource")
        add_button.clicked.connect(self.add_resource)
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(add_button)
        button_layout.addWidget(close_button)
        left_layout.addLayout(button_layout)
        
        main_layout.addWidget(left_panel)
        
        # Right panel for map
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Instructions label
        instructions = QLabel("Click on the map to select resource location")
        instructions.setStyleSheet("font-weight: bold;")
        right_layout.addWidget(instructions)
        
        # Map for location selection
        self.map_widget = map_client.create_map_widget(selection_mode=True)
        self.map_widget.location_selected.connect(self.on_location_selected)
        right_layout.addWidget(self.map_widget)
        
        main_layout.addWidget(right_panel)
        
        # Set size ratio between form and map (1:1)
        main_layout.setStretch(0, 1)  # Left panel
        main_layout.setStretch(1, 1)  # Right panel
        
        self.setLayout(main_layout)
        
        # Load existing resources
        self.load_resources()
        
    @pyqtSlot(float, float)
    def on_location_selected(self, lat, lng):
        """Handle location selection from map"""
        self.lat_edit.setText(f"{lat:.6f}")
        self.lng_edit.setText(f"{lng:.6f}")
        
    def load_resources(self):
        """Load existing resources into the table"""
        try:
            db = mongodb_client.get_database()
            resources = db.resources.find()
            
            self.resource_table.setRowCount(0)
            for resource in resources:
                row = self.resource_table.rowCount()
                self.resource_table.insertRow(row)
                
                self.resource_table.setItem(row, 0, QTableWidgetItem(resource.get("name", "")))
                self.resource_table.setItem(row, 1, QTableWidgetItem(resource.get("type", "")))
                self.resource_table.setItem(row, 2, QTableWidgetItem(resource.get("status", "")))
                
                location = resource.get("location", {}).get("coordinates", [0, 0])
                location_str = f"{location[1]}, {location[0]}"  # lat, lng
                self.resource_table.setItem(row, 3, QTableWidgetItem(location_str))
                
                self.resource_table.setItem(row, 4, QTableWidgetItem(str(resource.get("capacity", ""))))
                
                # Add action buttons
                action_widget = QWidget()
                action_layout = QHBoxLayout(action_widget)
                action_layout.setContentsMargins(0, 0, 0, 0)
                
                edit_btn = QPushButton("Edit")
                delete_btn = QPushButton("Delete")
                
                # Store resource data as JSON string in button property
                resource_json = json.dumps(resource, cls=JSONEncoder)
                edit_btn.setProperty("resource_data", resource_json)
                delete_btn.setProperty("resource_data", resource_json)
                
                edit_btn.clicked.connect(self.edit_resource)
                delete_btn.clicked.connect(self.delete_resource)
                
                action_layout.addWidget(edit_btn)
                action_layout.addWidget(delete_btn)
                
                self.resource_table.setCellWidget(row, 5, action_widget)
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load resources: {str(e)}")
    
    def add_resource(self):
        """Add a new resource to the database"""
        try:
            # Validate inputs
            if not self.name_edit.text():
                QMessageBox.warning(self, "Validation Error", "Name is required")
                return
                
            if not self.lat_edit.text() or not self.lng_edit.text():
                QMessageBox.warning(self, "Validation Error", "Please select a location on the map")
                return
            
            try:
                capacity = int(self.capacity_edit.text())
                if capacity < 0:
                    raise ValueError
            except ValueError:
                QMessageBox.warning(self, "Validation Error", "Capacity must be a positive number")
                return
            
            lat = float(self.lat_edit.text())
            lng = float(self.lng_edit.text())
            
            # Create resource document
            resource = {
                "name": self.name_edit.text(),
                "type": self.type_combo.currentText(),
                "status": self.status_combo.currentText(),
                "location": {
                    "type": "Point",
                    "coordinates": [lng, lat]  # GeoJSON format is [longitude, latitude]
                },
                "capacity": capacity,
                "description": self.description_edit.toPlainText(),
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            # Save to database
            db = mongodb_client.get_database()
            result = db.resources.insert_one(resource)
            
            if result.inserted_id:
                QMessageBox.information(self, "Success", "Resource added successfully")
                self.load_resources()  # Refresh the table
                
                # Clear the form
                self.name_edit.clear()
                self.lat_edit.clear()
                self.lng_edit.clear()
                self.capacity_edit.clear()
                self.description_edit.clear()
            else:
                QMessageBox.warning(self, "Error", "Failed to add resource")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            raise  # Re-raise for debugging
    
    def edit_resource(self):
        """Edit an existing resource"""
        try:
            button = self.sender()
            resource_json = button.property("resource_data")
            resource = json.loads(resource_json)
            
            # TODO: Implement resource editing
            QMessageBox.information(self, "Info", "Resource editing will be implemented in a future update")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
    
    def delete_resource(self):
        """Delete a resource"""
        try:
            button = self.sender()
            resource_json = button.property("resource_data")
            resource = json.loads(resource_json)
            
            reply = QMessageBox.question(self, "Confirm Delete",
                                       f"Are you sure you want to delete the resource '{resource.get('name')}'?",
                                       QMessageBox.Yes | QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                db = mongodb_client.get_database()
                result = db.resources.delete_one({"_id": ObjectId(resource["_id"])})
                
                if result.deleted_count:
                    QMessageBox.information(self, "Success", "Resource deleted successfully")
                    self.load_resources()  # Refresh the table
                else:
                    QMessageBox.warning(self, "Error", "Failed to delete resource")
                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            raise  # Re-raise for debugging
