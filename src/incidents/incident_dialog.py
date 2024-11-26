from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QComboBox, QPushButton, QFormLayout,
                            QTextEdit, QMessageBox, QWidget)
from PyQt5.QtCore import Qt, pyqtSlot
from ..utils.mongodb_client import mongodb_client
from ..utils.map_client import map_client
from datetime import datetime

class IncidentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Report New Incident")
        self.setModal(True)
        self.init_ui()
        
    def init_ui(self):
        main_layout = QHBoxLayout()
        
        # Left panel for form
        form_panel = QWidget()
        form_layout = QFormLayout(form_panel)
        
        # Title
        self.title_edit = QLineEdit()
        form_layout.addRow("Title:", self.title_edit)
        
        # Type
        self.type_combo = QComboBox()
        self.type_combo.addItems([
            "Natural Disaster",
            "Fire",
            "Medical Emergency",
            "Infrastructure Failure",
            "Security Incident",
            "Other"
        ])
        form_layout.addRow("Type:", self.type_combo)
        
        # Severity
        self.severity_combo = QComboBox()
        self.severity_combo.addItems(["Low", "Medium", "High", "Critical"])
        form_layout.addRow("Severity:", self.severity_combo)
        
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
        
        # Description
        self.description_edit = QTextEdit()
        form_layout.addRow("Description:", self.description_edit)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_incident)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        
        form_layout.addRow(button_layout)
        
        main_layout.addWidget(form_panel)
        
        # Right panel for map
        map_panel = QWidget()
        map_layout = QVBoxLayout(map_panel)
        
        # Instructions label
        instructions = QLabel("Click on the map to select incident location")
        instructions.setStyleSheet("font-weight: bold;")
        map_layout.addWidget(instructions)
        
        # Map for location selection
        self.map_widget = map_client.create_map_widget(selection_mode=True)
        self.map_widget.location_selected.connect(self.on_location_selected)
        map_layout.addWidget(self.map_widget)
        
        main_layout.addWidget(map_panel)
        
        # Set size ratio between form and map (1:2)
        main_layout.setStretch(0, 1)  # Form panel
        main_layout.setStretch(1, 2)  # Map panel
        
        self.setLayout(main_layout)
        
    @pyqtSlot(float, float)
    def on_location_selected(self, lat, lng):
        """Handle location selection from map"""
        self.lat_edit.setText(f"{lat:.6f}")
        self.lng_edit.setText(f"{lng:.6f}")
    
    def save_incident(self):
        """Save the incident to the database"""
        try:
            # Validate inputs
            if not self.title_edit.text():
                QMessageBox.warning(self, "Validation Error", "Title is required")
                return
                
            if not self.lat_edit.text() or not self.lng_edit.text():
                QMessageBox.warning(self, "Validation Error", "Please select a location on the map")
                return
            
            lat = float(self.lat_edit.text())
            lng = float(self.lng_edit.text())
            
            # Create incident document
            incident = {
                "title": self.title_edit.text(),
                "type": self.type_combo.currentText(),
                "severity": self.severity_combo.currentText(),
                "location": {
                    "type": "Point",
                    "coordinates": [lng, lat]  # GeoJSON format is [longitude, latitude]
                },
                "description": self.description_edit.toPlainText(),
                "status": "Active",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            # Save to database
            db = mongodb_client.get_database()
            result = db.incidents.insert_one(incident)
            
            if result.inserted_id:
                QMessageBox.information(self, "Success", "Incident reported successfully")
                self.accept()
            else:
                QMessageBox.warning(self, "Error", "Failed to save incident")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            raise  # Re-raise the exception for debugging
