from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem)
from models.resource import ResourceManager
from models.incident import IncidentManager

class ResourceAssignmentDialog(QDialog):
    def __init__(self, incident_id, parent=None):
        super().__init__(parent)
        self.incident_id = incident_id
        self.resource_manager = ResourceManager()
        self.incident_manager = IncidentManager()
        
        self.setWindowTitle("Assign Resources")
        self.setup_ui()
        self.load_available_resources()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Resources table
        self.resources_table = QTableWidget()
        self.resources_table.setColumnCount(6)
        self.resources_table.setHorizontalHeaderLabels([
            "ID", "Name", "Type", "Location", "Status", "Action"
        ])
        self.resources_table.horizontalHeader().setStretchLastSection(True)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.reject)
        button_layout.addWidget(self.close_button)
        
        layout.addWidget(QLabel("Available Resources"))
        layout.addWidget(self.resources_table)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.resize(800, 400)
        
    def load_available_resources(self):
        # Get available resources (not in maintenance or assigned)
        resources = self.resource_manager.list_resources({
            'status': 'available',
            'maintenance_status': 'operational'
        })
        
        self.resources_table.setRowCount(len(resources))
        
        for row, resource in enumerate(resources):
            self.resources_table.setItem(row, 0, 
                QTableWidgetItem(resource['_id']))
            self.resources_table.setItem(row, 1, 
                QTableWidgetItem(resource['name']))
            self.resources_table.setItem(row, 2, 
                QTableWidgetItem(resource['type']))
            self.resources_table.setItem(row, 3, 
                QTableWidgetItem(resource['location']))
            self.resources_table.setItem(row, 4, 
                QTableWidgetItem(resource['status']))
            
            # Assign button
            assign_btn = QPushButton("Assign")
            assign_btn.clicked.connect(
                lambda checked, rid=resource['_id']: 
                self.assign_resource(rid))
            
            self.resources_table.setCellWidget(row, 5, assign_btn)
            
    def assign_resource(self, resource_id):
        try:
            # Assign resource to incident
            self.incident_manager.assign_resource(
                self.incident_id, resource_id)
            
            # Update resource status
            self.resource_manager.assign_to_incident(
                resource_id, self.incident_id)
            
            # Refresh the table
            self.load_available_resources()
        except Exception as e:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(
                self, "Error", f"Failed to assign resource: {str(e)}")
