import os
from typing import Optional
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import PyMongoError
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class MongoDBClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBClient, cls).__new__(cls)
            cls._instance.client = None
            cls._instance.db = None
        return cls._instance

    def __init__(self):
        if self.client is None:
            self.initialize_connection()

    def initialize_connection(self):
        """Initialize MongoDB connection using environment variables."""
        try:
            # Load environment variables
            load_dotenv()
            
            # Get MongoDB connection details from environment
            mongodb_uri = os.getenv('MONGODB_URI')
            database_name = os.getenv('MONGODB_DATABASE')

            logger.info(f"Connecting to MongoDB at: {mongodb_uri}")
            logger.info(f"Using database: {database_name}")

            if not mongodb_uri or not database_name:
                raise ValueError("MongoDB connection details not found in environment variables")

            # Create MongoDB client
            self.client = MongoClient(mongodb_uri)
            self.db = self.client[database_name]

            # Test connection
            self.client.admin.command('ping')
            
            # Create indexes
            self._setup_indexes()
            
            logger.info("Successfully connected to MongoDB")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            self.client = None
            self.db = None
            raise

    def _setup_indexes(self):
        """Setup necessary indexes for collections."""
        try:
            # Users collection indexes
            self.db.users.create_index("username", unique=True)
            self.db.users.create_index("email", unique=True)

            # Incidents collection indexes
            self.db.incidents.create_index([("location", "2dsphere")])
            self.db.incidents.create_index("status")
            self.db.incidents.create_index("severity")

            # Resources collection indexes
            self.db.resources.create_index([("location", "2dsphere")])
            self.db.resources.create_index("status")
            self.db.resources.create_index("type")

            logger.info("Successfully created MongoDB indexes")
        except Exception as e:
            logger.error(f"Failed to create indexes: {str(e)}")
            raise

    def get_database(self) -> Optional[Database]:
        """Get the MongoDB database instance."""
        if self.client is None:
            logger.warning("Database connection not initialized, attempting to reconnect")
            self.initialize_connection()
        return self.db

    def close_connection(self):
        """Close the MongoDB connection."""
        if self.client is not None:
            self.client.close()
            self.client = None
            self.db = None
            logger.info("MongoDB connection closed")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create a singleton instance
mongodb_client = MongoDBClient()
