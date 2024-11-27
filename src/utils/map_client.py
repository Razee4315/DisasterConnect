"""OpenStreetMap integration utility for DisasterConnect."""
import os
from typing import Dict, List
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
    searchCompleted = pyqtSignal(list)
    
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
        
    @pyqtSlot(str, result='QVariant')
    def onSearchResults(self, results):
        """Handle search results from map"""
        results_list = json.loads(results)
        self.searchCompleted.emit(results_list)
        return results_list

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
        """Initialize the map view with enhanced template"""
        template_path = os.path.join(
            os.path.dirname(__file__),
            'templates',
            'map_enhanced.html'
        )
        self.load(QUrl.fromLocalFile(template_path))
        self.loadFinished.connect(self.on_load_finished)
        
    def on_load_finished(self, ok):
        """Handle map load completion"""
        if ok:
            print("Map loaded successfully")
            if self.selection_mode:
                print("Map in selection mode - click to select location")
                # Enable click handling for location selection
                self.page().runJavaScript("console.log('Selection mode enabled');")
        else:
            print("Error loading map")
            
    def on_location_selected(self, lat, lng):
        """Handle location selection"""
        print(f"Location selected in MapWidget: {lat}, {lng}")
        if self.selection_mode:
            # Clear any existing markers
            self.page().runJavaScript("clearMarkers();")
            # Add a temporary marker at the selected location
            self.page().runJavaScript(f"""
                let marker = L.marker([{lat}, {lng}]).addTo(map);
                setTimeout(() => map.removeLayer(marker), 2000);  // Remove after 2 seconds
            """)
        # Emit the signal
        self.location_selected.emit(lat, lng)
        
    def on_location_updated(self, lat, lng):
        """Handle location updates"""
        print(f"Location updated: {lat}, {lng}")
        self.location_updated.emit(lat, lng)
        
    def add_incident_marker(self, lat: float, lng: float, data: Dict):
        """Add an incident marker with heatmap point"""
        js = f"addIncidentMarker({lat}, {lng}, {json.dumps(data)})"
        self.page().runJavaScript(js)
        
    def add_resource_marker(self, lat: float, lng: float, data: Dict):
        """Add a resource marker to the map"""
        js = f"addResourceMarker({lat}, {lng}, {json.dumps(data)})"
        self.page().runJavaScript(js)
        
    def add_alert_marker(self, lat: float, lng: float, data: Dict):
        """Add an alert marker to the map"""
        js = f"addAlertMarker({lat}, {lng}, {json.dumps(data)})"
        self.page().runJavaScript(js)
        
    def add_cluster_markers(self, markers: List[Dict]):
        """Add clustered markers to the map"""
        js = f"addClusterMarkers({json.dumps(markers)})"
        self.page().runJavaScript(js)
        
    def update_alert_radius(self, lat: float, lng: float, radius: float, data: Dict):
        """Update alert radius circle on the map"""
        js = f"updateAlertRadius({lat}, {lng}, {radius}, {json.dumps(data)})"
        self.page().runJavaScript(js)
        
    def clear_markers(self):
        """Clear all markers and heatmap from the map"""
        self.page().runJavaScript("clearMarkers()")
        
    def clear_alerts(self):
        """Clear all alert markers and radius circles"""
        self.page().runJavaScript("clearAlerts()")
        
    def update_heatmap(self, points: List[Dict]):
        """Update heatmap with new points"""
        js = f"updateHeatmap({json.dumps(points)})"
        self.page().runJavaScript(js)
        
    def set_view(self, lat: float, lng: float, zoom: int = 13):
        """Set the map view to specific coordinates"""
        js = f"map.setView([{lat}, {lng}], {zoom})"
        self.page().runJavaScript(js)
        
    def toggle_clustering(self, enabled: bool):
        """Toggle marker clustering on/off"""
        js = f"toggleClustering({str(enabled).lower()})"
        self.page().runJavaScript(js)

class MapClient:
    """Singleton map client for creating map widgets"""
    
    def create_map_widget(self, selection_mode=False) -> MapWidget:
        """Create a new map widget"""
        return MapWidget(selection_mode=selection_mode)

# Create singleton instance
map_client = MapClient()
