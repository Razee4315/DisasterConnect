import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # MongoDB Settings
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
    MONGODB_DATABASE = os.getenv('MONGODB_DATABASE', 'disasterconnect')

    # Application Settings
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    JWT_SECRET = os.getenv('JWT_SECRET', 'default_jwt_secret')

    # WebSocket Configuration
    WEBSOCKET_HOST = os.getenv('WEBSOCKET_HOST', 'localhost')
    WEBSOCKET_PORT = int(os.getenv('WEBSOCKET_PORT', '8765'))

    # Map Services
    MAP_API_KEY = os.getenv('MAP_API_KEY', '')

    # UI Theme
    THEME = {
        'primary_color': '#00796B',
        'secondary_color': '#FFA726',
        'background_color': '#F5F5F5',
        'text_color': '#333333',
        'font_family': 'Roboto'
    }

    # Collection Names
    COLLECTIONS = {
        'incidents': 'incidents',
        'resources': 'resources',
        'users': 'users',
        'messages': 'messages',
        'tasks': 'tasks'
    }

    # Logging Configuration
    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'default': {
                'level': LOG_LEVEL,
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
            },
            'file': {
                'level': LOG_LEVEL,
                'formatter': 'standard',
                'class': 'logging.FileHandler',
                'filename': 'app.log',
                'mode': 'a'
            }
        },
        'loggers': {
            '': {
                'handlers': ['default', 'file'],
                'level': LOG_LEVEL,
                'propagate': True
            }
        }
    }
