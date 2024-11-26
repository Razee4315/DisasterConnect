from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QComboBox, QLineEdit, QTextEdit, 
                             QTableWidget, QTableWidgetItem, QMessageBox)
from PyQt5.QtCore import Qt
from models.resource import ResourceManager

class ResourceWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resource_manager = ResourceManager()
        self.setup_ui()
        self.load_resources()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Create resource section
        create_group = QVBoxLayout()
        
        # Input fields
        input_layout = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Resource Name")
        
        self.type_combo = QComboBox()
        self.type_combo.addItems([
            "Vehicle", "Medical Equipment", "Personnel", 
            "Emergency Supplies", "Communication Equipment"
        ])
        
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("Current Location")
        
        self.capacity_input = QLineEdit()
        self.capacity_input.setPlaceholderText("Capacity/Quantity")
        
        input_layout.addWidget(self.name_input)
        input_layout.addWidget(self.type_combo)
        input_layout.addWidget(self.location_input)
        input_layout.addWidget(self.capacity_input)
        
        # Description and contact info
        details_layout = QHBoxLayout()
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Resource Description")
        self.description_input.setMaximumHeight(80)
        
        self.contact_input = QTextEdit()
        self.contact_input.setPlaceholderText("Contact Information")
        self.contact_input.setMaximumHeight(80)
        
        details_layout.addWidget(self.description_input)
        details_layout.addWidget(self.contact_input)
        
        # Create button
        self.create_button = QPushButton("Add Resource")
        self.create_button.clicked.connect(self.create_resource)
        
        create_group.addLayout(input_layout)
        create_group.addLayout(details_layout)
        create_group.addWidget(self.create_button)
        
        # Resources table
        self.resources_table = QTableWidget()
        self.resources_table.setColumnCount(8)
        self.resources_table.setHorizontalHeaderLabels([
            "ID", "Name", "Type", "Location", "Status", 
            "Maintenance Status", "Current Incident", "Actions"
        ])
        self.resources_table.horizontalHeader().setStretchLastSection(True)
        
        layout.addLayout(create_group)
        layout.addWidget(QLabel("Available Resources"))
        layout.addWidget(self.resources_table)
        
        self.setLayout(layout)
        
    def create_resource(self):
        data = {
            'name': self.name_input.text(),
            'type': self.type_combo.currentText(),
            'location': self.location_input.text(),
            'capacity': self.capacity_input.text(),
            'description': self.description_input.toPlainText(),
            'contact_info': self.contact_input.toPlainText(),
            'created_by': 'current_user'  # Replace with actual user ID
        }
        
        if not all([data['name'], data['location'], data['description']]):
            QMessageBox.warning(self, "Validation Error", 
                              "Please fill in all required fields.")
            return
            
        try:
            self.resource_manager.create_resource(data)
            self.clear_inputs()
            self.load_resources()
            QMessageBox.information(self, "Success", 
                                  "Resource added successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", 
                               f"Failed to add resource: {str(e)}")
            
    def load_resources(self):
        resources = self.resource_manager.list_resources()
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
            self.resources_table.setItem(row, 5, 
                QTableWidgetItem(resource['maintenance_status']))
            self.resources_table.setItem(row, 6, 
                QTableWidgetItem(resource.get('current_incident', 'None')))
            
            # Action buttons
            actions_widget = QWidget()
            actions_layout = QHBoxLayout()
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            if resource['status'] != 'maintenance':
                maintenance_btn = QPushButton("Maintenance")
                maintenance_btn.clicked.connect(
                    lambda checked, id=resource['_id']: 
                    self.start_maintenance(id))
                actions_layout.addWidget(maintenance_btn)
            else:
                complete_btn = QPushButton("Complete")
                complete_btn.clicked.connect(
                    lambda checked, id=resource['_id']: 
                    self.complete_maintenance(id))
                actions_layout.addWidget(complete_btn)
            
            actions_widget.setLayout(actions_layout)
            self.resources_table.setCellWidget(row, 7, actions_widget)
            
    def clear_inputs(self):
        self.name_input.clear()
        self.type_combo.setCurrentIndex(0)
        self.location_input.clear()
        self.capacity_input.clear()
        self.description_input.clear()
        self.contact_input.clear()
        
    def start_maintenance(self, resource_id):
        try:
            self.resource_manager.mark_maintenance(
                resource_id, "under_maintenance", 
                "Scheduled maintenance started")
            self.load_resources()
            QMessageBox.information(
                self, "Success", "Resource marked for maintenance!")
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Failed to start maintenance: {str(e)}")
            
    def complete_maintenance(self, resource_id):
        try:
            self.resource_manager.complete_maintenance(resource_id)
            self.load_resources()
            QMessageBox.information(
                self, "Success", "Maintenance completed successfully!")
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Failed to complete maintenance: {str(e)}")
