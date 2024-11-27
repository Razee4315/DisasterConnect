"""Resource management widget for DisasterConnect."""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QFrame, QTableWidget, QTableWidgetItem,
                           QComboBox, QLineEdit, QDialog, QFormLayout,
                           QSpinBox, QMessageBox, QHeaderView)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
import os
from datetime import datetime

class ResourceDialog(QDialog):
    """Dialog for adding/editing resources."""
    
    def __init__(self, parent=None, resource_data=None):
        super().__init__(parent)
        self.resource_data = resource_data
        self.setWindowTitle("Resource Details")
        self.setModal(True)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        form = QFormLayout()
        
        # Name
        self.name_input = QLineEdit()
        if self.resource_data:
            self.name_input.setText(self.resource_data.get('name', ''))
        form.addRow("Name:", self.name_input)
        
        # Type
        self.type_combo = QComboBox()
        self.type_combo.addItems([
            "Medical Supplies",
            "Food and Water",
            "Transportation",
            "Shelter",
            "Communication Equipment",
            "Power Supply",
            "Search and Rescue Equipment",
            "Other"
        ])
        if self.resource_data:
            self.type_combo.setCurrentText(self.resource_data.get('type', ''))
        form.addRow("Type:", self.type_combo)
        
        # Quantity
        self.quantity_input = QSpinBox()
        self.quantity_input.setRange(0, 10000)
        if self.resource_data:
            self.quantity_input.setValue(self.resource_data.get('quantity', 0))
        form.addRow("Quantity:", self.quantity_input)
        
        # Location
        self.location_input = QLineEdit()
        if self.resource_data:
            self.location_input.setText(self.resource_data.get('location', ''))
        form.addRow("Location:", self.location_input)
        
        # Status
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Available", "In Use", "Reserved", "Maintenance"])
        if self.resource_data:
            self.status_combo.setCurrentText(self.resource_data.get('status', ''))
        form.addRow("Status:", self.status_combo)
        
        layout.addLayout(form)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.accept)
        save_button.setObjectName("primary-button")
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        
        # Set stylesheet
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLineEdit, QComboBox, QSpinBox {
                padding: 8px;
                border: 1px solid #dadce0;
                border-radius: 4px;
                background-color: #f8f9fa;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
                border-color: #1a73e8;
                background-color: white;
            }
            #primary-button {
                background-color: #1a73e8;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            #primary-button:hover {
                background-color: #1557b0;
            }
        """)
    
    def get_resource_data(self):
        """Get the resource data from the form."""
        return {
            'name': self.name_input.text(),
            'type': self.type_combo.currentText(),
            'quantity': self.quantity_input.value(),
            'location': self.location_input.text(),
            'status': self.status_combo.currentText(),
            'last_updated': datetime.now().isoformat()
        }

class ResourceWidget(QWidget):
    """Widget for managing resources."""
    
    def __init__(self, auth_manager=None):
        super().__init__()
        self.auth_manager = auth_manager
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the resource management UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header = QFrame()
        header.setObjectName("page-header")
        header_layout = QHBoxLayout(header)
        
        title = QLabel("Resource Management")
        title.setObjectName("page-title")
        header_layout.addWidget(title)
        
        # Add resource button
        add_button = QPushButton("Add Resource")
        add_button.setObjectName("primary-button")
        add_button.clicked.connect(self.show_resource_dialog)
        header_layout.addWidget(add_button, alignment=Qt.AlignRight)
        
        layout.addWidget(header)
        
        # Filters
        filter_frame = QFrame()
        filter_frame.setObjectName("filter-frame")
        filter_layout = QHBoxLayout(filter_frame)
        
        # Search
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search resources...")
        self.search_input.textChanged.connect(self.filter_resources)
        filter_layout.addWidget(self.search_input)
        
        # Type filter
        self.type_filter = QComboBox()
        self.type_filter.addItems([
            "All Types",
            "Medical Supplies",
            "Food and Water",
            "Transportation",
            "Shelter",
            "Communication Equipment",
            "Power Supply",
            "Search and Rescue Equipment",
            "Other"
        ])
        self.type_filter.currentTextChanged.connect(self.filter_resources)
        filter_layout.addWidget(self.type_filter)
        
        # Status filter
        self.status_filter = QComboBox()
        self.status_filter.addItems([
            "All Statuses",
            "Available",
            "In Use",
            "Reserved",
            "Maintenance"
        ])
        self.status_filter.currentTextChanged.connect(self.filter_resources)
        filter_layout.addWidget(self.status_filter)
        
        layout.addWidget(filter_frame)
        
        # Resource table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Name", "Type", "Quantity", "Location", "Status", "Last Updated", "Actions"
        ])
        
        # Set column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        
        layout.addWidget(self.table)
        
        # Set stylesheet
        self.setStyleSheet("""
            #filter-frame {
                background-color: white;
                border-radius: 8px;
                margin: 10px;
                padding: 10px;
            }
            QLineEdit, QComboBox {
                padding: 8px;
                border: 1px solid #dadce0;
                border-radius: 4px;
                background-color: #f8f9fa;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #1a73e8;
                background-color: white;
            }
            QTableWidget {
                background-color: white;
                border: none;
                border-radius: 8px;
                margin: 10px;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #e8f0fe;
                color: #1a73e8;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 8px;
                border: none;
                border-bottom: 1px solid #dadce0;
                font-weight: bold;
            }
        """)
        
        # Load initial data
        self.load_resources()
    
    def show_resource_dialog(self, resource_data=None):
        """Show dialog for adding/editing resources."""
        dialog = ResourceDialog(self, resource_data)
        if dialog.exec_() == QDialog.Accepted:
            resource_data = dialog.get_resource_data()
            self.save_resource(resource_data)
    
    def save_resource(self, resource_data):
        """Save resource data."""
        # TODO: Implement resource saving logic with backend
        self.load_resources()
    
    def load_resources(self):
        """Load resources from the backend."""
        # TODO: Implement resource loading logic
        # For now, using dummy data
        resources = [
            {
                'name': 'Ambulance A1',
                'type': 'Transportation',
                'quantity': 1,
                'location': 'Central Station',
                'status': 'Available',
                'last_updated': '2024-02-20T10:30:00'
            },
            {
                'name': 'Medical Supplies Kit',
                'type': 'Medical Supplies',
                'quantity': 50,
                'location': 'Main Hospital',
                'status': 'In Use',
                'last_updated': '2024-02-20T09:15:00'
            }
        ]
        
        self.update_table(resources)
    
    def update_table(self, resources):
        """Update the resource table with data."""
        self.table.setRowCount(0)
        for resource in resources:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # Add resource data
            self.table.setItem(row, 0, QTableWidgetItem(resource['name']))
            self.table.setItem(row, 1, QTableWidgetItem(resource['type']))
            self.table.setItem(row, 2, QTableWidgetItem(str(resource['quantity'])))
            self.table.setItem(row, 3, QTableWidgetItem(resource['location']))
            self.table.setItem(row, 4, QTableWidgetItem(resource['status']))
            
            # Format timestamp
            timestamp = datetime.fromisoformat(resource['last_updated'])
            time_str = timestamp.strftime("%Y-%m-%d %H:%M")
            self.table.setItem(row, 5, QTableWidgetItem(time_str))
            
            # Add action buttons
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(4, 4, 4, 4)
            
            edit_btn = QPushButton("Edit")
            edit_btn.setObjectName("action-button")
            edit_btn.clicked.connect(lambda checked, r=resource: self.show_resource_dialog(r))
            
            delete_btn = QPushButton("Delete")
            delete_btn.setObjectName("action-button")
            delete_btn.clicked.connect(lambda checked, r=row: self.delete_resource(r))
            
            action_layout.addWidget(edit_btn)
            action_layout.addWidget(delete_btn)
            
            self.table.setCellWidget(row, 6, action_widget)
    
    def filter_resources(self):
        """Filter resources based on search and filters."""
        # TODO: Implement filtering logic
        self.load_resources()
    
    def delete_resource(self, row):
        """Delete a resource."""
        reply = QMessageBox.question(
            self, "Confirm Delete",
            "Are you sure you want to delete this resource?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # TODO: Implement deletion logic
            self.table.removeRow(row)
