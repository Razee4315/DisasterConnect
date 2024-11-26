from datetime import datetime, timedelta
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import matplotlib.pyplot as plt
import pandas as pd
from models.incident import IncidentManager
from models.resource import ResourceManager

class ReportGenerator:
    def __init__(self):
        self.incident_manager = IncidentManager()
        self.resource_manager = ResourceManager()
        self.styles = getSampleStyleSheet()
        
    def generate_incident_report(self, start_date, end_date, output_path):
        """Generate a PDF report for incidents within the date range"""
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        elements = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30
        )
        elements.append(Paragraph("Incident Report", title_style))
        elements.append(Paragraph(
            f"Period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
            self.styles['Normal']
        ))
        elements.append(Spacer(1, 20))
        
        # Summary statistics
        incidents = self.incident_manager.list_incidents({
            'created_at': {
                '$gte': start_date,
                '$lte': end_date
            }
        })
        
        total_incidents = len(incidents)
        active_incidents = sum(1 for i in incidents if i['status'] == 'active')
        closed_incidents = total_incidents - active_incidents
        
        summary_data = [
            ["Total Incidents", str(total_incidents)],
            ["Active Incidents", str(active_incidents)],
            ["Closed Incidents", str(closed_incidents)]
        ]
        
        summary_table = Table(summary_data, colWidths=[200, 100])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 14),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 20))
        
        # Incident details table
        if incidents:
            incident_data = [["Title", "Type", "Severity", "Status", "Created"]]
            for incident in incidents:
                incident_data.append([
                    incident['title'],
                    incident['type'],
                    incident['severity'],
                    incident['status'],
                    incident['created_at'].strftime('%Y-%m-%d')
                ])
            
            incident_table = Table(incident_data, colWidths=[120, 100, 80, 80, 100])
            incident_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(Paragraph("Incident Details", self.styles['Heading2']))
            elements.append(incident_table)
        
        doc.build(elements)
        return output_path
        
    def generate_resource_report(self, output_path):
        """Generate a PDF report for current resource status"""
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        elements = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30
        )
        elements.append(Paragraph("Resource Status Report", title_style))
        elements.append(Paragraph(
            f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            self.styles['Normal']
        ))
        elements.append(Spacer(1, 20))
        
        # Get resources
        resources = self.resource_manager.list_resources()
        
        # Summary statistics
        total_resources = len(resources)
        available_resources = sum(1 for r in resources if r['status'] == 'available')
        assigned_resources = sum(1 for r in resources if r['status'] == 'assigned')
        maintenance_resources = sum(1 for r in resources if r['status'] == 'maintenance')
        
        summary_data = [
            ["Total Resources", str(total_resources)],
            ["Available", str(available_resources)],
            ["Assigned", str(assigned_resources)],
            ["In Maintenance", str(maintenance_resources)]
        ]
        
        summary_table = Table(summary_data, colWidths=[200, 100])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 14),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 20))
        
        # Resource details table
        if resources:
            resource_data = [["Name", "Type", "Location", "Status", "Current Incident"]]
            for resource in resources:
                resource_data.append([
                    resource['name'],
                    resource['type'],
                    resource['location'],
                    resource['status'],
                    resource.get('current_incident', 'None')
                ])
            
            resource_table = Table(resource_data, colWidths=[100, 100, 100, 80, 100])
            resource_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(Paragraph("Resource Details", self.styles['Heading2']))
            elements.append(resource_table)
        
        doc.build(elements)
        return output_path
        
    def generate_analytics_charts(self, output_dir):
        """Generate analytics charts for incidents and resources"""
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Get data
        incidents = self.incident_manager.list_incidents()
        resources = self.resource_manager.list_resources()
        
        # Convert to pandas DataFrames
        incidents_df = pd.DataFrame(incidents)
        resources_df = pd.DataFrame(resources)
        
        # 1. Incident Type Distribution
        plt.figure(figsize=(10, 6))
        incidents_df['type'].value_counts().plot(kind='bar')
        plt.title('Incident Distribution by Type')
        plt.xlabel('Incident Type')
        plt.ylabel('Count')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'incident_types.png'))
        plt.close()
        
        # 2. Incident Status
        plt.figure(figsize=(8, 8))
        incidents_df['status'].value_counts().plot(kind='pie', autopct='%1.1f%%')
        plt.title('Incident Status Distribution')
        plt.axis('equal')
        plt.savefig(os.path.join(output_dir, 'incident_status.png'))
        plt.close()
        
        # 3. Resource Status
        plt.figure(figsize=(8, 8))
        resources_df['status'].value_counts().plot(kind='pie', autopct='%1.1f%%')
        plt.title('Resource Status Distribution')
        plt.axis('equal')
        plt.savefig(os.path.join(output_dir, 'resource_status.png'))
        plt.close()
        
        # 4. Resource Types
        plt.figure(figsize=(10, 6))
        resources_df['type'].value_counts().plot(kind='bar')
        plt.title('Resource Distribution by Type')
        plt.xlabel('Resource Type')
        plt.ylabel('Count')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'resource_types.png'))
        plt.close()
        
        return output_dir
