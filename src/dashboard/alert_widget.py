"""Alert management widget for DisasterConnect."""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QFrame, QTableWidget, QTableWidgetItem,
                           QComboBox, QLineEdit, QDialog, QFormLayout,
                           QTextEdit, QMessageBox, QHeaderView)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QColor
import os
from datetime import datetime

class AlertDialog(QDialog):
    """Dialog for creating/editing alerts."""
    
    def __init__(self, parent=None, alert_data=None):
        super().__init__(parent)
        self.alert_data = alert_data
        self.setWindowTitle("Alert Details")
        self.setModal(True)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        form = QFormLayout()
        
        # Title
        self.title_input = QLineEdit()
        if self.alert_data:
            self.title_input.setText(self.alert_data.get('title', ''))
        form.addRow("Title:", self.title_input)
        
        # Type
        self.type_combo = QComboBox()
        self.type_combo.addItems([
            "Emergency",
            "Warning",
            "Advisory",
            "Information"
        ])
        if self.alert_data:
            self.type_combo.setCurrentText(self.alert_data.get('type', ''))
        form.addRow("Type:", self.type_combo)
        
        # Severity
        self.severity_combo = QComboBox()
        self.severity_combo.addItems(["Low", "Medium", "High", "Critical"])
        if self.alert_data:
            self.severity_combo.setCurrentText(self.alert_data.get('severity', ''))
        form.addRow("Severity:", self.severity_combo)
        
        # Area
        self.area_input = QLineEdit()
        if self.alert_data:
            self.area_input.setText(self.alert_data.get('area', ''))
        form.addRow("Affected Area:", self.area_input)
        
        # Message
        self.message_input = QTextEdit()
        if self.alert_data:
            self.message_input.setText(self.alert_data.get('message', ''))
        form.addRow("Message:", self.message_input)
        
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
    
    def get_alert_data(self):
        """Get the alert data from the form."""
        return {
            'title': self.title_input.text(),
            'type': self.type_combo.currentText(),
            'severity': self.severity_combo.currentText(),
            'area': self.area_input.text(),
            'message': self.message_input.toPlainText(),
            'timestamp': datetime.now().isoformat()
        }

class AlertWidget(QWidget):
    """Widget for managing alerts."""
    
    def __init__(self, auth_manager=None):
        super().__init__()
        self.auth_manager = auth_manager
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the alert management UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header = QFrame()
        header.setObjectName("page-header")
        header_layout = QHBoxLayout(header)
        
        title = QLabel("Alert Management")
        title.setObjectName("page-title")
        header_layout.addWidget(title)
        
        # Add alert button
        add_button = QPushButton("Create Alert")
        add_button.setObjectName("primary-button")
        add_button.clicked.connect(self.show_alert_dialog)
        header_layout.addWidget(add_button, alignment=Qt.AlignRight)
        
        layout.addWidget(header)
        
        # Filters
        filter_frame = QFrame()
        filter_frame.setObjectName("filter-frame")
        filter_layout = QHBoxLayout(filter_frame)
        
        # Search
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search alerts...")
        self.search_input.textChanged.connect(self.filter_alerts)
        filter_layout.addWidget(self.search_input)
        
        # Type filter
        self.type_filter = QComboBox()
        self.type_filter.addItems([
            "All Types",
            "Emergency",
            "Warning",
            "Advisory",
            "Information"
        ])
        self.type_filter.currentTextChanged.connect(self.filter_alerts)
        filter_layout.addWidget(self.type_filter)
        
        # Severity filter
        self.severity_filter = QComboBox()
        self.severity_filter.addItems([
            "All Severities",
            "Low",
            "Medium",
            "High",
            "Critical"
        ])
        self.severity_filter.currentTextChanged.connect(self.filter_alerts)
        filter_layout.addWidget(self.severity_filter)
        
        layout.addWidget(filter_frame)
        
        # Alert table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Title", "Type", "Severity", "Area", "Message", "Time", "Actions"
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
        self.load_alerts()
    
    def show_alert_dialog(self, alert_data=None):
        """Show dialog for creating/editing alerts."""
        dialog = AlertDialog(self, alert_data)
        if dialog.exec_() == QDialog.Accepted:
            alert_data = dialog.get_alert_data()
            self.save_alert(alert_data)
    
    def save_alert(self, alert_data):
        """Save alert data."""
        # TODO: Implement alert saving logic with backend
        self.load_alerts()
    
    def load_alerts(self):
        """Load alerts from the backend."""
        # TODO: Implement alert loading logic
        # For now, using dummy data
        alerts = [
            {
                'title': 'Flash Flood Warning',
                'type': 'Emergency',
                'severity': 'Critical',
                'area': 'Downtown Area',
                'message': 'Immediate evacuation required due to rising water levels.',
                'timestamp': '2024-02-20T10:30:00'
            },
            {
                'title': 'Power Outage Advisory',
                'type': 'Advisory',
                'severity': 'Medium',
                'area': 'North District',
                'message': 'Temporary power outage expected. Restoration in progress.',
                'timestamp': '2024-02-20T09:15:00'
            }
        ]
        
        self.update_table(alerts)
    
    def update_table(self, alerts):
        """Update the alert table with data."""
        self.table.setRowCount(0)
        for alert in alerts:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # Add alert data
            self.table.setItem(row, 0, QTableWidgetItem(alert['title']))
            
            # Type with color coding
            type_item = QTableWidgetItem(alert['type'])
            type_color = {
                'Emergency': '#dc3545',
                'Warning': '#ffc107',
                'Advisory': '#17a2b8',
                'Information': '#28a745'
            }.get(alert['type'], '#6c757d')
            type_item.setForeground(QColor(type_color))
            self.table.setItem(row, 1, type_item)
            
            # Severity with color coding
            severity_item = QTableWidgetItem(alert['severity'])
            severity_color = {
                'Critical': '#dc3545',
                'High': '#ffc107',
                'Medium': '#17a2b8',
                'Low': '#28a745'
            }.get(alert['severity'], '#6c757d')
            severity_item.setForeground(QColor(severity_color))
            self.table.setItem(row, 2, severity_item)
            
            self.table.setItem(row, 3, QTableWidgetItem(alert['area']))
            self.table.setItem(row, 4, QTableWidgetItem(alert['message']))
            
            # Format timestamp
            timestamp = datetime.fromisoformat(alert['timestamp'])
            time_str = timestamp.strftime("%Y-%m-%d %H:%M")
            self.table.setItem(row, 5, QTableWidgetItem(time_str))
            
            # Add action buttons
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(4, 4, 4, 4)
            
            edit_btn = QPushButton("Edit")
            edit_btn.setObjectName("action-button")
            edit_btn.clicked.connect(lambda checked, a=alert: self.show_alert_dialog(a))
            
            delete_btn = QPushButton("Delete")
            delete_btn.setObjectName("action-button")
            delete_btn.clicked.connect(lambda checked, r=row: self.delete_alert(r))
            
            action_layout.addWidget(edit_btn)
            action_layout.addWidget(delete_btn)
            
            self.table.setCellWidget(row, 6, action_widget)
    
    def filter_alerts(self):
        """Filter alerts based on search and filters."""
        # TODO: Implement filtering logic
        self.load_alerts()
    
    def delete_alert(self, row):
        """Delete an alert."""
        reply = QMessageBox.question(
            self, "Confirm Delete",
            "Are you sure you want to delete this alert?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # TODO: Implement deletion logic
            self.table.removeRow(row)
