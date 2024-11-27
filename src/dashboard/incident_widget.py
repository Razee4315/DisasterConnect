"""Incident management widget for DisasterConnect."""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QFrame, QTableWidget, QTableWidgetItem,
                           QComboBox, QLineEdit, QDialog, QFormLayout,
                           QTextEdit, QMessageBox, QHeaderView)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
import os
from datetime import datetime

class IncidentDialog(QDialog):
    """Dialog for creating/editing incidents."""
    
    def __init__(self, parent=None, incident_data=None):
        super().__init__(parent)
        self.incident_data = incident_data
        self.setWindowTitle("Incident Details")
        self.setModal(True)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        form = QFormLayout()
        
        # Title
        self.title_input = QLineEdit()
        if self.incident_data:
            self.title_input.setText(self.incident_data.get('title', ''))
        form.addRow("Title:", self.title_input)
        
        # Type
        self.type_combo = QComboBox()
        self.type_combo.addItems([
            "Natural Disaster",
            "Industrial Accident",
            "Medical Emergency",
            "Infrastructure Failure",
            "Security Incident",
            "Other"
        ])
        if self.incident_data:
            self.type_combo.setCurrentText(self.incident_data.get('type', ''))
        form.addRow("Type:", self.type_combo)
        
        # Severity
        self.severity_combo = QComboBox()
        self.severity_combo.addItems(["Low", "Medium", "High", "Critical"])
        if self.incident_data:
            self.severity_combo.setCurrentText(self.incident_data.get('severity', ''))
        form.addRow("Severity:", self.severity_combo)
        
        # Location
        self.location_input = QLineEdit()
        if self.incident_data:
            self.location_input.setText(self.incident_data.get('location', ''))
        form.addRow("Location:", self.location_input)
        
        # Description
        self.description_input = QTextEdit()
        if self.incident_data:
            self.description_input.setText(self.incident_data.get('description', ''))
        form.addRow("Description:", self.description_input)
        
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
            QLineEdit, QComboBox, QTextEdit {
                padding: 8px;
                border: 1px solid #dadce0;
                border-radius: 4px;
                background-color: #f8f9fa;
            }
            QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
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
    
    def get_incident_data(self):
        """Get the incident data from the form."""
        return {
            'title': self.title_input.text(),
            'type': self.type_combo.currentText(),
            'severity': self.severity_combo.currentText(),
            'location': self.location_input.text(),
            'description': self.description_input.toPlainText(),
            'timestamp': datetime.now().isoformat()
        }

class IncidentWidget(QWidget):
    """Widget for managing incidents."""
    
    def __init__(self, auth_manager=None):
        super().__init__()
        self.auth_manager = auth_manager
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the incident management UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header = QFrame()
        header.setObjectName("page-header")
        header_layout = QHBoxLayout(header)
        
        title = QLabel("Incident Management")
        title.setObjectName("page-title")
        header_layout.addWidget(title)
        
        # Add incident button
        add_button = QPushButton("Report Incident")
        add_button.setObjectName("primary-button")
        add_button.clicked.connect(self.show_incident_dialog)
        header_layout.addWidget(add_button, alignment=Qt.AlignRight)
        
        layout.addWidget(header)
        
        # Filters
        filter_frame = QFrame()
        filter_frame.setObjectName("filter-frame")
        filter_layout = QHBoxLayout(filter_frame)
        
        # Search
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search incidents...")
        self.search_input.textChanged.connect(self.filter_incidents)
        filter_layout.addWidget(self.search_input)
        
        # Type filter
        self.type_filter = QComboBox()
        self.type_filter.addItems(["All Types", "Natural Disaster", "Industrial Accident",
                                 "Medical Emergency", "Infrastructure Failure",
                                 "Security Incident", "Other"])
        self.type_filter.currentTextChanged.connect(self.filter_incidents)
        filter_layout.addWidget(self.type_filter)
        
        # Severity filter
        self.severity_filter = QComboBox()
        self.severity_filter.addItems(["All Severities", "Low", "Medium", "High", "Critical"])
        self.severity_filter.currentTextChanged.connect(self.filter_incidents)
        filter_layout.addWidget(self.severity_filter)
        
        layout.addWidget(filter_frame)
        
        # Incident table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Title", "Type", "Severity", "Location", "Time", "Actions"
        ])
        
        # Set column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        
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
        self.load_incidents()
    
    def show_incident_dialog(self, incident_data=None):
        """Show dialog for creating/editing incidents."""
        dialog = IncidentDialog(self, incident_data)
        if dialog.exec_() == QDialog.Accepted:
            incident_data = dialog.get_incident_data()
            self.save_incident(incident_data)
    
    def save_incident(self, incident_data):
        """Save incident data."""
        # TODO: Implement incident saving logic with backend
        self.load_incidents()
    
    def load_incidents(self):
        """Load incidents from the backend."""
        # TODO: Implement incident loading logic
        # For now, using dummy data
        incidents = [
            {
                'title': 'Flood in Downtown',
                'type': 'Natural Disaster',
                'severity': 'High',
                'location': 'Downtown Area',
                'timestamp': '2024-02-20T10:30:00'
            },
            {
                'title': 'Chemical Spill',
                'type': 'Industrial Accident',
                'severity': 'Critical',
                'location': 'Industrial Park',
                'timestamp': '2024-02-20T09:15:00'
            }
        ]
        
        self.update_table(incidents)
    
    def update_table(self, incidents):
        """Update the incident table with data."""
        self.table.setRowCount(0)
        for incident in incidents:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # Add incident data
            self.table.setItem(row, 0, QTableWidgetItem(incident['title']))
            self.table.setItem(row, 1, QTableWidgetItem(incident['type']))
            self.table.setItem(row, 2, QTableWidgetItem(incident['severity']))
            self.table.setItem(row, 3, QTableWidgetItem(incident['location']))
            
            # Format timestamp
            timestamp = datetime.fromisoformat(incident['timestamp'])
            time_str = timestamp.strftime("%Y-%m-%d %H:%M")
            self.table.setItem(row, 4, QTableWidgetItem(time_str))
            
            # Add action buttons
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(4, 4, 4, 4)
            
            edit_btn = QPushButton("Edit")
            edit_btn.setObjectName("action-button")
            edit_btn.clicked.connect(lambda checked, i=incident: self.show_incident_dialog(i))
            
            delete_btn = QPushButton("Delete")
            delete_btn.setObjectName("action-button")
            delete_btn.clicked.connect(lambda checked, r=row: self.delete_incident(r))
            
            action_layout.addWidget(edit_btn)
            action_layout.addWidget(delete_btn)
            
            self.table.setCellWidget(row, 5, action_widget)
    
    def filter_incidents(self):
        """Filter incidents based on search and filters."""
        # TODO: Implement filtering logic
        self.load_incidents()
    
    def delete_incident(self, row):
        """Delete an incident."""
        reply = QMessageBox.question(
            self, "Confirm Delete",
            "Are you sure you want to delete this incident?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # TODO: Implement deletion logic
            self.table.removeRow(row)
