from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QDialog, QLabel,
                             QLineEdit, QComboBox, QTextEdit, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
from ..utils.map_client import map_client
from ..utils.mongodb_client import mongodb_client
from ..utils.location_picker import pick_location
from datetime import datetime
from bson import ObjectId

class IncidentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Incident")
        self.setModal(True)
        self.setMinimumWidth(400)
        self.setMinimumHeight(600)
        
        # Main layout
        layout = QVBoxLayout(self)
        
        # Add form fields
        self.title_label = QLabel("Title:")
        self.title_input = QLineEdit()
        layout.addWidget(self.title_label)
        layout.addWidget(self.title_input)
        
        self.type_label = QLabel("Type:")
        self.type_input = QComboBox()
        self.type_input.addItems(["Natural Disaster", "Medical Emergency", "Infrastructure Failure", "Other"])
        layout.addWidget(self.type_label)
        layout.addWidget(self.type_input)
        
        self.severity_label = QLabel("Severity:")
        self.severity_input = QComboBox()
        self.severity_input.addItems(["Low", "Medium", "High", "Critical"])
        layout.addWidget(self.severity_label)
        layout.addWidget(self.severity_input)
        
        self.status_label = QLabel("Status:")
        self.status_input = QComboBox()
        self.status_input.addItems(["Reported", "In Progress", "Resolved"])
        layout.addWidget(self.status_label)
        layout.addWidget(self.status_input)
        
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
    
    def get_incident_data(self):
        """Get the incident data from the form"""
        if not self.selected_location:
            return None
            
        return {
            "title": self.title_input.text(),
            "type": self.type_input.currentText(),
            "severity": self.severity_input.currentText(),
            "status": self.status_input.currentText(),
            "description": self.description_input.toPlainText(),
            "location": self.selected_location,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

class IncidentsWidget(QWidget):
    incident_deleted = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        
        # Add incident button
        self.add_button = QPushButton("Add Incident")
        self.add_button.clicked.connect(self.add_incident)
        layout.addWidget(self.add_button)
        
        # Incidents table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Title", "Type", "Severity", "Status", "Location", "Actions"])
        layout.addWidget(self.table)
        
        # Map widget
        self.map_widget = map_client.create_map_widget()
        layout.addWidget(self.map_widget)
        
        self.refresh_data()
        
    def add_incident(self):
        """Open dialog to add a new incident"""
        dialog = IncidentDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            incident_data = dialog.get_incident_data()
            if incident_data:
                # Save to database
                result = mongodb_client.db.incidents.insert_one(incident_data)
                if result.inserted_id:
                    self.refresh_data()
                
    def refresh_data(self):
        """Refresh the incidents data"""
        try:
            # Clear existing data
            self.table.setRowCount(0)
            self.map_widget.clear_markers()
            
            # Fetch incidents from database
            incidents = list(mongodb_client.db.incidents.find()) or []
            
            # Update table and map
            for incident in incidents:
                try:
                    row = self.table.rowCount()
                    self.table.insertRow(row)
                    
                    # Create delete button
                    delete_btn = QPushButton("Delete")
                    delete_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #ff4444;
                            color: white;
                            border: none;
                            padding: 5px;
                            border-radius: 3px;
                        }
                        QPushButton:hover {
                            background-color: #ff0000;
                        }
                    """)
                    delete_btn.clicked.connect(lambda checked, id=str(incident['_id']): self.delete_incident(id))
                    
                    # Set table items
                    self.table.setItem(row, 0, QTableWidgetItem(str(incident['_id'])))
                    self.table.setItem(row, 1, QTableWidgetItem(incident.get("title", "Untitled")))
                    self.table.setItem(row, 2, QTableWidgetItem(incident.get("type", "Unknown")))
                    self.table.setItem(row, 3, QTableWidgetItem(incident.get("severity", "Unknown")))
                    self.table.setItem(row, 4, QTableWidgetItem(incident.get("status", "Unknown")))
                    
                    # Handle location data safely
                    location = incident.get("location", {})
                    if location and "lat" in location and "lng" in location:
                        self.table.setItem(row, 5, QTableWidgetItem(f"({location['lat']:.6f}, {location['lng']:.6f})"))
                        
                        # Add to map
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
                    else:
                        self.table.setItem(row, 5, QTableWidgetItem("No location"))
                    
                    self.table.setCellWidget(row, 6, delete_btn)
                    
                except Exception as e:
                    print(f"Error processing incident: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error refreshing incidents data: {e}")
            
    def delete_incident(self, incident_id):
        """Delete an incident"""
        try:
            reply = QMessageBox.question(
                self,
                'Delete Incident',
                'Are you sure you want to delete this incident?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                from bson import ObjectId
                result = mongodb_client.db.incidents.delete_one({'_id': ObjectId(incident_id)})
                if result.deleted_count > 0:
                    print(f"Successfully deleted incident {incident_id}")
                    self.refresh_data()
                    # Emit signal to refresh map
                    self.incident_deleted.emit()
                else:
                    print(f"Failed to delete incident {incident_id}")
                    QMessageBox.warning(self, 'Error', 'Failed to delete incident')
                    
        except Exception as e:
            print(f"Error deleting incident: {e}")
            QMessageBox.warning(self, 'Error', f'Error deleting incident: {str(e)}')
