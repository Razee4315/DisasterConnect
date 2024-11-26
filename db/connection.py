from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)

class DatabaseConnection:
    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._client:
            self.connect()

    def connect(self):
        """
        Establish connection to MongoDB
        """
        try:
            self._client = MongoClient(Config.MONGODB_URI)
            self._db = self._client[Config.MONGODB_DATABASE]
            # Verify connection
            self._client.admin.command('ping')
            logger.info("Successfully connected to MongoDB")
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise

    @property
    def db(self):
        """
        Get database instance
        """
        if not self._db:
            self.connect()
        return self._db

    @property
    def client(self):
        """
        Get MongoDB client instance
        """
        if not self._client:
            self.connect()
        return self._client

    def close(self):
        """
        Close MongoDB connection
        """
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
            logger.info("MongoDB connection closed")

# Create a singleton instance
db_connection = DatabaseConnection()
