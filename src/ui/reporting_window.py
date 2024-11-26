from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QCalendarWidget, QFileDialog,
                             QTabWidget, QScrollArea, QMessageBox)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QPixmap
import os
from datetime import datetime
from reporting.report_generator import ReportGenerator

class ReportingWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.report_generator = ReportGenerator()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Create tab widget
        tab_widget = QTabWidget()
        
        # PDF Reports tab
        pdf_tab = self.create_pdf_tab()
        tab_widget.addTab(pdf_tab, "PDF Reports")
        
        # Analytics tab
        analytics_tab = self.create_analytics_tab()
        tab_widget.addTab(analytics_tab, "Analytics")
        
        layout.addWidget(tab_widget)
        self.setLayout(layout)
        
    def create_pdf_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Date selection for incident report
        date_layout = QHBoxLayout()
        
        # Start date
        start_date_layout = QVBoxLayout()
        start_date_layout.addWidget(QLabel("Start Date:"))
        self.start_calendar = QCalendarWidget()
        self.start_calendar.setMaximumDate(QDate.currentDate())
        start_date_layout.addWidget(self.start_calendar)
        date_layout.addLayout(start_date_layout)
        
        # End date
        end_date_layout = QVBoxLayout()
        end_date_layout.addWidget(QLabel("End Date:"))
        self.end_calendar = QCalendarWidget()
        self.end_calendar.setMaximumDate(QDate.currentDate())
        end_date_layout.addWidget(self.end_calendar)
        date_layout.addLayout(end_date_layout)
        
        layout.addLayout(date_layout)
        
        # Report generation buttons
        buttons_layout = QHBoxLayout()
        
        incident_report_btn = QPushButton("Generate Incident Report")
        incident_report_btn.clicked.connect(self.generate_incident_report)
        buttons_layout.addWidget(incident_report_btn)
        
        resource_report_btn = QPushButton("Generate Resource Report")
        resource_report_btn.clicked.connect(self.generate_resource_report)
        buttons_layout.addWidget(resource_report_btn)
        
        layout.addLayout(buttons_layout)
        widget.setLayout(layout)
        return widget
        
    def create_analytics_tab(self):
        widget = QScrollArea()
        widget.setWidgetResizable(True)
        content = QWidget()
        layout = QVBoxLayout()
        
        # Generate charts button
        generate_btn = QPushButton("Generate Analytics Charts")
        generate_btn.clicked.connect(self.generate_analytics)
        layout.addWidget(generate_btn)
        
        # Chart display areas
        self.chart_labels = []
        for title in ["Incident Types", "Incident Status", 
                     "Resource Status", "Resource Types"]:
            label = QLabel(title)
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)
            
            chart_label = QLabel()
            chart_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(chart_label)
            self.chart_labels.append(chart_label)
        
        content.setLayout(layout)
        widget.setWidget(content)
        return widget
        
    def generate_incident_report(self):
        try:
            start_date = datetime.combine(
                self.start_calendar.selectedDate().toPyDate(),
                datetime.min.time()
            )
            end_date = datetime.combine(
                self.end_calendar.selectedDate().toPyDate(),
                datetime.max.time()
            )
            
            if start_date > end_date:
                QMessageBox.warning(
                    self, "Invalid Date Range",
                    "Start date must be before end date."
                )
                return
                
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save Incident Report",
                os.path.expanduser("~/incident_report.pdf"),
                "PDF Files (*.pdf)"
            )
            
            if file_path:
                self.report_generator.generate_incident_report(
                    start_date, end_date, file_path)
                QMessageBox.information(
                    self, "Success",
                    f"Incident report saved to: {file_path}"
                )
        except Exception as e:
            QMessageBox.critical(
                self, "Error",
                f"Failed to generate incident report: {str(e)}"
            )
            
    def generate_resource_report(self):
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save Resource Report",
                os.path.expanduser("~/resource_report.pdf"),
                "PDF Files (*.pdf)"
            )
            
            if file_path:
                self.report_generator.generate_resource_report(file_path)
                QMessageBox.information(
                    self, "Success",
                    f"Resource report saved to: {file_path}"
                )
        except Exception as e:
            QMessageBox.critical(
                self, "Error",
                f"Failed to generate resource report: {str(e)}"
            )
            
    def generate_analytics(self):
        try:
            # Create charts directory in user's documents
            charts_dir = os.path.expanduser("~/disaster_connect_charts")
            output_dir = self.report_generator.generate_analytics_charts(charts_dir)
            
            # Display charts
            chart_files = [
                'incident_types.png',
                'incident_status.png',
                'resource_status.png',
                'resource_types.png'
            ]
            
            for label, chart_file in zip(self.chart_labels, chart_files):
                pixmap = QPixmap(os.path.join(output_dir, chart_file))
                scaled_pixmap = pixmap.scaled(
                    600, 400,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                label.setPixmap(scaled_pixmap)
            
            QMessageBox.information(
                self, "Success",
                f"Analytics charts generated and saved to: {output_dir}"
            )
        except Exception as e:
            QMessageBox.critical(
                self, "Error",
                f"Failed to generate analytics charts: {str(e)}"
            )
