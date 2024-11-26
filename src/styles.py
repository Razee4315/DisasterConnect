def get_app_stylesheet():
    return """
        QMainWindow {
            background-color: #f0f0f0;
        }
        
        QFrame {
            border: 1px solid #cccccc;
            border-radius: 4px;
            background-color: white;
            padding: 8px;
            margin: 4px;
        }
        
        QPushButton {
            background-color: #0078d4;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            min-width: 80px;
        }
        
        QPushButton:hover {
            background-color: #106ebe;
        }
        
        QPushButton:pressed {
            background-color: #005a9e;
        }
        
        QLabel {
            color: #333333;
        }
        
        QLineEdit {
            padding: 6px;
            border: 1px solid #cccccc;
            border-radius: 4px;
            background-color: white;
        }
        
        QLineEdit:focus {
            border-color: #0078d4;
        }
        
        /* Dashboard specific styles */
        #dashboard-header {
            background-color: white;
            border-bottom: 1px solid #cccccc;
            padding: 8px;
        }
        
        #sidebar {
            background-color: #f8f8f8;
            border-right: 1px solid #cccccc;
            min-width: 200px;
        }
        
        #stat-card {
            background-color: white;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 16px;
            margin: 8px;
        }
        
        #stat-value {
            color: #0078d4;
            font-size: 24px;
            font-weight: bold;
        }
    """
