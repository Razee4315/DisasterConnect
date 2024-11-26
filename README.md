# DisasterConnect

## Project Overview
DisasterConnect is a robust desktop application designed for efficient disaster management and collaboration. Built with PyQt5 and MongoDB, it provides comprehensive incident tracking, resource management, and reporting capabilities for disaster response teams.

## Core Features

### 1. Authentication System
- Secure user registration and login
- Password hashing with SHA-256
- MongoDB-based user storage
- Session management

### 2. Dashboard
- Modern, responsive PyQt5-based interface
- Tabbed navigation system
- Quick access to all major features
- User-friendly layout

### 3. Incident Management
- Create and track incidents
- Incident details (title, type, severity, location)
- Status tracking (active/closed)
- Resource assignment
- Features:
  - Create new incidents
  - Update incident status
  - Assign resources
  - Close resolved incidents

### 4. Resource Management
- Comprehensive resource tracking
- Resource types (vehicles, medical equipment, personnel)
- Status monitoring (available, assigned, maintenance)
- Features:
  - Add new resources
  - Track resource status
  - Manage maintenance
  - Assign to incidents

### 5. Reporting System
- PDF report generation
- Data visualization
- Features:
  - Incident reports with date filtering
  - Resource status reports
  - Analytics charts
  - Export capabilities

## Technical Details

### Built With
- Python 3.11
- PyQt5 for GUI
- MongoDB Atlas for database
- ReportLab for PDF generation
- Matplotlib for data visualization

### Dependencies
- PyQt5==5.15.9
- pymongo==4.5.0
- python-dotenv==1.0.0
- bcrypt==4.0.1
- reportlab==4.0.4
- matplotlib==3.7.2
- pandas==2.1.0
- pytest==7.4.2

## Getting Started

### Prerequisites
- Python 3.11 or higher
- MongoDB Atlas account
- Git

### Installation
1. Clone the repository:
```bash
git clone [repository-url]
cd DisasterConnect
```

2. Create and activate virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
copy .env.example .env
# Edit .env with your MongoDB connection string
```

5. Run the application:
```bash
python src/main.py
```

## Documentation
- [Development Setup](docs/DEVELOPMENT_SETUP.md)
- [API Documentation](docs/API.md)
- [User Guide](docs/USER_GUIDE.md)

## Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
