from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QComboBox, QLineEdit, QTextEdit, 
                             QTableWidget, QTableWidgetItem, QMessageBox)
from PyQt5.QtCore import Qt
from models.incident import IncidentManager
from models.resource import ResourceManager
from ui.resource_assignment_dialog import ResourceAssignmentDialog

class IncidentWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.incident_manager = IncidentManager()
        self.resource_manager = ResourceManager()
        self.setup_ui()
        self.load_incidents()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Create incident section
        create_group = QVBoxLayout()
        
        # Input fields
        input_layout = QHBoxLayout()
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Incident Title")
        
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Natural Disaster", "Medical Emergency", 
                                "Infrastructure Failure", "Security Incident"])
        
        self.severity_combo = QComboBox()
        self.severity_combo.addItems(["Low", "Medium", "High", "Critical"])
        
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("Location")
        
        input_layout.addWidget(self.title_input)
        input_layout.addWidget(self.type_combo)
        input_layout.addWidget(self.severity_combo)
        input_layout.addWidget(self.location_input)
        
        # Description field
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Incident Description")
        self.description_input.setMaximumHeight(100)
        
        # Create button
        self.create_button = QPushButton("Create Incident")
        self.create_button.clicked.connect(self.create_incident)
        
        create_group.addLayout(input_layout)
        create_group.addWidget(self.description_input)
        create_group.addWidget(self.create_button)
        
        # Incidents table
        self.incidents_table = QTableWidget()
        self.incidents_table.setColumnCount(7)
        self.incidents_table.setHorizontalHeaderLabels([
            "ID", "Title", "Type", "Severity", "Location", "Status", "Actions"
        ])
        self.incidents_table.horizontalHeader().setStretchLastSection(True)
        
        layout.addLayout(create_group)
        layout.addWidget(QLabel("Active Incidents"))
        layout.addWidget(self.incidents_table)
        
        self.setLayout(layout)
        
    def create_incident(self):
        data = {
            'title': self.title_input.text(),
            'type': self.type_combo.currentText(),
            'severity': self.severity_combo.currentText(),
            'location': self.location_input.text(),
            'description': self.description_input.toPlainText(),
            'created_by': 'current_user'  # Replace with actual user ID
        }
        
        if not all([data['title'], data['location'], data['description']]):
            QMessageBox.warning(self, "Validation Error", 
                              "Please fill in all required fields.")
            return
            
        try:
            self.incident_manager.create_incident(data)
            self.clear_inputs()
            self.load_incidents()
            QMessageBox.information(self, "Success", 
                                  "Incident created successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", 
                               f"Failed to create incident: {str(e)}")
            
    def load_incidents(self):
        incidents = self.incident_manager.list_incidents({'status': 'active'})
        self.incidents_table.setRowCount(len(incidents))
        
        for row, incident in enumerate(incidents):
            self.incidents_table.setItem(row, 0, 
                QTableWidgetItem(incident['_id']))
            self.incidents_table.setItem(row, 1, 
                QTableWidgetItem(incident['title']))
            self.incidents_table.setItem(row, 2, 
                QTableWidgetItem(incident['type']))
            self.incidents_table.setItem(row, 3, 
                QTableWidgetItem(incident['severity']))
            self.incidents_table.setItem(row, 4, 
                QTableWidgetItem(incident['location']))
            self.incidents_table.setItem(row, 5, 
                QTableWidgetItem(incident['status']))
            
            # Action buttons
            actions_widget = QWidget()
            actions_layout = QHBoxLayout()
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            assign_btn = QPushButton("Assign")
            assign_btn.clicked.connect(
                lambda checked, id=incident['_id']: self.show_resource_dialog(id))
            
            close_btn = QPushButton("Close")
            close_btn.clicked.connect(
                lambda checked, id=incident['_id']: self.close_incident(id))
            
            actions_layout.addWidget(assign_btn)
            actions_layout.addWidget(close_btn)
            actions_widget.setLayout(actions_layout)
            
            self.incidents_table.setCellWidget(row, 6, actions_widget)
            
    def clear_inputs(self):
        self.title_input.clear()
        self.type_combo.setCurrentIndex(0)
        self.severity_combo.setCurrentIndex(0)
        self.location_input.clear()
        self.description_input.clear()
        
    def show_resource_dialog(self, incident_id):
        dialog = ResourceAssignmentDialog(incident_id, self)
        dialog.exec_()
        self.load_incidents()  # Refresh the incidents table after assignment
        
    def close_incident(self, incident_id):
        reply = QMessageBox.question(
            self, "Close Incident",
            "Are you sure you want to close this incident?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.incident_manager.close_incident(
                    incident_id, "Incident resolved")
                self.load_incidents()
                QMessageBox.information(
                    self, "Success", "Incident closed successfully!")
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"Failed to close incident: {str(e)}")
