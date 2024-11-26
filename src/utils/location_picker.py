from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QLabel, QLineEdit, QWidget)
from PyQt5.QtCore import Qt, pyqtSignal
from .map_client import map_client

class LocationPickerDialog(QDialog):
    """Dialog for picking a location on the map"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Location")
        self.setModal(True)
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        
        # Main layout
        layout = QVBoxLayout(self)
        
        # Add coordinate display
        coord_widget = QWidget()
        coord_layout = QHBoxLayout(coord_widget)
        
        # Latitude display
        lat_widget = QWidget()
        lat_layout = QVBoxLayout(lat_widget)
        self.lat_label = QLabel("Latitude:")
        self.lat_display = QLineEdit()
        self.lat_display.setReadOnly(True)
        self.lat_display.setPlaceholderText("Click on map to select")
        lat_layout.addWidget(self.lat_label)
        lat_layout.addWidget(self.lat_display)
        coord_layout.addWidget(lat_widget)
        
        # Longitude display
        lng_widget = QWidget()
        lng_layout = QVBoxLayout(lng_widget)
        self.lng_label = QLabel("Longitude:")
        self.lng_display = QLineEdit()
        self.lng_display.setReadOnly(True)
        self.lng_display.setPlaceholderText("Click on map to select")
        lng_layout.addWidget(self.lng_label)
        lng_layout.addWidget(self.lng_display)
        coord_layout.addWidget(lng_widget)
        
        layout.addWidget(coord_widget)
        
        # Map widget
        self.map_widget = map_client.create_map_widget(selection_mode=True)
        self.map_widget.location_selected.connect(self.on_location_selected)
        layout.addWidget(self.map_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.confirm_button = QPushButton("Confirm Location")
        self.confirm_button.setEnabled(False)
        self.confirm_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        
        button_layout.addWidget(self.confirm_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        # Connect buttons
        self.confirm_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        
        # Initialize location
        self.selected_location = None
        
    def on_location_selected(self, lat, lng):
        """Handle location selection from map"""
        self.selected_location = {"lat": lat, "lng": lng}
        self.lat_display.setText(f"{lat:.6f}")
        self.lng_display.setText(f"{lng:.6f}")
        self.confirm_button.setEnabled(True)
        
    def get_location(self):
        """Get the selected location"""
        return self.selected_location

def pick_location(parent=None):
    """Show location picker dialog and return selected location"""
    dialog = LocationPickerDialog(parent)
    result = dialog.exec_()
    
    if result == QDialog.Accepted:
        return dialog.get_location()
    return None
