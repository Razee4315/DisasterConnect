import sys
from PyQt5.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from src.utils.mongodb_client import mongodb_client
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """
    Main entry point of the DisasterConnect application
    """
    try:
        # Initialize the application
        app = QApplication(sys.argv)
        
        # Set application style
        app.setStyle('Fusion')
        
        # Create and show main window
        main_window = MainWindow()
        main_window.show()
        
        # Start the application event loop
        sys.exit(app.exec_())
        
    except Exception as e:
        logger.error(f"Application failed to start: {str(e)}")
        sys.exit(1)
    finally:
        # Clean up resources
        mongodb_client.close_connection()

if __name__ == '__main__':
    main()
