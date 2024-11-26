"""OpenStreetMap integration utility for DisasterConnect."""
import os
from typing import Dict
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton
from PyQt5.QtCore import QUrl, pyqtSignal, QObject, pyqtSlot
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWebChannel import QWebChannel
import json

class WebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        print(f"JS: {message} (line {lineNumber})")

class WebBridge(QObject):
    locationSelected = pyqtSignal(float, float)
    locationUpdated = pyqtSignal(float, float)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        print("WebBridge initialized")
    
    @pyqtSlot(float, float)
    def onLocationSelected(self, lat, lng):
        """Handle location selection from map"""
        print(f"Location selected in bridge: {lat}, {lng}")
        self.locationSelected.emit(lat, lng)
        
    @pyqtSlot(float, float)
    def onLocationUpdated(self, lat, lng):
        """Handle location updates from map"""
        print(f"Location updated in bridge: {lat}, {lng}")
        self.locationUpdated.emit(lat, lng)

class MapWidget(QWebEngineView):
    location_selected = pyqtSignal(float, float)
    location_updated = pyqtSignal(float, float)
    
    def __init__(self, parent=None, selection_mode=False):
        super().__init__(parent)
        self.selection_mode = selection_mode
        print(f"MapWidget initialized, selection_mode: {selection_mode}")
        
        # Create custom page with console message handling
        self.setPage(WebEnginePage(self))
        
        # Set up web channel for JavaScript communication
        self.channel = QWebChannel()
        self.web_bridge = WebBridge()
        self.web_bridge.locationSelected.connect(self.on_location_selected)
        self.web_bridge.locationUpdated.connect(self.on_location_updated)
        self.channel.registerObject("bridge", self.web_bridge)
        self.page().setWebChannel(self.channel)
        
        # Initialize map
        self.init_map()
        
    def init_map(self):
        """Initialize the map view"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(current_dir, 'map.html')
        
        if not os.path.exists(html_path):
            raise FileNotFoundError(f"Map HTML file not found at {html_path}")
            
        self.setUrl(QUrl.fromLocalFile(html_path))
        self.loadFinished.connect(self.on_load_finished)
    
    def on_load_finished(self, ok):
        """Handle map load completion"""
        if ok:
            print("Map loaded successfully")
            if self.selection_mode:
                self.page().runJavaScript("setSelectionMode(true);")
        else:
            print("Error loading map")
    
    def on_location_selected(self, lat, lng):
        """Handle location selection"""
        print(f"Location selected: {lat}, {lng}")
        self.location_selected.emit(lat, lng)
    
    def on_location_updated(self, lat, lng):
        """Handle location updates"""
        print(f"Location updated: {lat}, {lng}")
        self.location_updated.emit(lat, lng)
        
    def add_incident_marker(self, lat: float, lng: float, data: Dict):
        """Add an incident marker to the map"""
        js = f"addIncidentMarker({lat}, {lng}, {json.dumps(data)});"
        self.page().runJavaScript(js)
        
    def add_resource_marker(self, lat: float, lng: float, data: Dict):
        """Add a resource marker to the map"""
        js = f"addResourceMarker({lat}, {lng}, {json.dumps(data)});"
        self.page().runJavaScript(js)
        
    def clear_markers(self):
        """Clear all markers from the map"""
        self.page().runJavaScript("clearMarkers();")

class MapClient:
    def create_map_widget(self, selection_mode=False):
        """Create a new map widget"""
        return MapWidget(selection_mode=selection_mode)

# Create singleton instance
map_client = MapClient()
