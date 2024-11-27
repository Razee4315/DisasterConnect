"""Splash screen for DisasterConnect."""
from PyQt5.QtWidgets import QSplashScreen, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QPainter
import os

class SplashScreen(QSplashScreen):
    def __init__(self):
        # Load splash image
        splash_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                 'resources', 'images', 'logo_splash.png')
        splash_pixmap = QPixmap(splash_path)
        super().__init__(splash_pixmap)
        
        # Create layout for additional content
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        # Add loading text
        self.loading_label = QLabel("Loading DisasterConnect...")
        self.loading_label.setStyleSheet("""
            QLabel {
                color: #2C3E50;
                font-size: 18px;
                font-weight: bold;
                margin-top: 20px;
            }
        """)
        self.loading_label.setAlignment(Qt.AlignCenter)
        
        # Create widget to hold the layout
        widget = QWidget(self)
        widget.setLayout(layout)
        layout.addWidget(self.loading_label)
        
        # Position the widget at the bottom of the splash screen
        widget.move(0, splash_pixmap.height() - widget.height() - 50)
        
        # Set window flags
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        
        # Initialize progress
        self.progress = 0
        self.progress_texts = [
            "Initializing application...",
            "Loading resources...",
            "Connecting to database...",
            "Preparing user interface...",
            "Starting DisasterConnect..."
        ]
        
        # Setup progress timer
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_progress)
        self.timer.start(800)  # Update every 800ms
    
    def _update_progress(self):
        """Update the loading progress text."""
        self.progress += 1
        if self.progress < len(self.progress_texts):
            self.loading_label.setText(self.progress_texts[self.progress])
        else:
            self.timer.stop()
    
    def drawContents(self, painter):
        """Override to add custom drawing."""
        super().drawContents(painter)
