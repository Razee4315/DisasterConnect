# Development Setup Guide

## Environment Setup

### Prerequisites
1. Python 3.x
2. MongoDB Atlas Account
3. Git

### MongoDB Atlas Setup
1. Create a MongoDB Atlas account at [https://www.mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Create a new cluster (Free tier is sufficient for development)
3. Set up database access:
   - Create a database user
   - Save the credentials
4. Set up network access:
   - Add your IP address
   - For development, you can allow access from anywhere (0.0.0.0/0)
5. Get your connection string:
   - Click "Connect"
   - Choose "Connect your application"
   - Copy the connection string

### Local Development Setup

1. Clone the repository:
```bash
git clone [repository-url]
cd DisasterConnect
```

2. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
copy .env.example .env
```

5. Update `.env` with your MongoDB Atlas connection string and other configurations

## Features Configuration

### Authentication
- Local authentication (username/password)
- OAuth support (Google, Microsoft)
- JWT-based session management
- Password requirements:
  - Minimum 8 characters
  - At least one uppercase letter
  - At least one number
  - At least one special character

### Maps Integration
- OpenStreetMap implementation
- Features:
  - Incident location marking
  - Resource location tracking
  - Heatmap visualization
  - Cluster visualization for multiple incidents

### Data Export
- Supported formats:
  - PDF (with charts and maps)
  - Excel (detailed data tables)
- Custom templates for different report types

### Offline Support
- Local data caching
- Sync queue for offline changes
- Automatic sync when online
- Conflict resolution handling

### Backup & Restore
- Automated daily backups
- Manual backup option
- Point-in-time restoration
- Export/Import functionality

## Testing

### Unit Tests
- Test individual components
- Use pytest framework
- Mock external services

### Integration Tests
- Test component interactions
- Database integration tests
- API endpoint tests

### End-to-End Tests
- Full application flow tests
- UI interaction tests
- Scenario-based testing

## Project Structure
```
DisasterConnect/
├── main.py                 # Application entry point
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── .gitignore            # Git ignore rules
│
├── db/                    # Database related files
│   ├── connection.py     # MongoDB connection
│   ├── models/          # Database models
│   └── migrations/      # Database migrations
│
├── ui/                    # UI related files
│   ├── main_window.py   # Main application window
│   ├── dashboard/       # Dashboard components
│   ├── incidents/       # Incident management
│   └── resources/       # Resource management
│
├── utils/                 # Utility functions
│   ├── logger.py        # Logging configuration
│   ├── auth.py         # Authentication utilities
│   └── export.py       # Export utilities
│
├── tests/                 # Test files
│   ├── unit/           # Unit tests
│   ├── integration/    # Integration tests
│   └── e2e/           # End-to-end tests
│
└── docs/                  # Documentation
    ├── DEVELOPMENT_SETUP.md
    ├── API.md
    └── USER_GUIDE.md
```

## Development Workflow

1. Feature Development
   - Create feature branch from main
   - Implement feature
   - Write tests
   - Create pull request

2. Code Review Process
   - Code style check
   - Test coverage check
   - Peer review
   - Merge to main

3. Testing Process
   - Run unit tests
   - Run integration tests
   - Run end-to-end tests
   - Manual testing

4. Deployment
   - Version bump
   - Create release notes
   - Build executable
   - Test installation

## Coding Standards

1. Python Style Guide
   - Follow PEP 8
   - Use type hints
   - Document functions and classes

2. Git Commit Messages
   - Use conventional commits
   - Include issue references

3. Documentation
   - Update relevant docs with changes
   - Include docstrings
   - Maintain README.md
