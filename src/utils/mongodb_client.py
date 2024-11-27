import os
from typing import Any, Dict, List, Optional
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import ConnectionFailure

class MongoDBClient:
    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBClient, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = False

    @property
    def client(self):
        if not self._client:
            self.initialize_connection()
        return self._client

    @property
    def db(self):
        if not self._db:
            self.initialize_connection()
        return self._db

    def initialize_connection(self) -> None:
        """Initialize MongoDB connection using environment variables."""
        if self._client is not None:
            return

        mongodb_uri = os.getenv('MONGODB_URI')
        database_name = os.getenv('MONGODB_DATABASE')

        if not mongodb_uri or not database_name:
            raise ValueError("MongoDB connection details not found in environment variables")

        try:
            # Create MongoDB client
            self._client = MongoClient(mongodb_uri)
            
            # Test connection with ping command
            self._client.admin.command('ping')
            
            # Set database after successful connection test
            self._db = self._client[database_name]
            self.initialized = True
        except ConnectionFailure as e:
            self._client = None
            self._db = None
            raise Exception(f"Failed to connect to MongoDB: Connection failed - {str(e)}")
        except Exception as e:
            self._client = None
            self._db = None
            raise Exception(f"Failed to connect to MongoDB: {str(e)}")

    def get_collection(self, collection_name: str) -> Collection:
        """Get a MongoDB collection."""
        if not self._client or not self._db:
            self.initialize_connection()
        return self._db[collection_name]

    def insert_one(self, collection_name: str, document: Dict[str, Any]) -> str:
        """Insert a single document into a collection."""
        collection = self.get_collection(collection_name)
        result = collection.insert_one(document)
        return str(result.inserted_id)

    def insert_many(self, collection_name: str, documents: List[Dict[str, Any]]) -> List[str]:
        """Insert multiple documents into a collection."""
        collection = self.get_collection(collection_name)
        result = collection.insert_many(documents)
        return [str(id_) for id_ in result.inserted_ids]

    def find_one(self, collection_name: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find a single document in a collection."""
        collection = self.get_collection(collection_name)
        return collection.find_one(query)

    def find_many(self, collection_name: str, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find multiple documents in a collection."""
        collection = self.get_collection(collection_name)
        return list(collection.find(query))

    def update_one(self, collection_name: str, query: Dict[str, Any], update: Dict[str, Any]) -> int:
        """Update a single document in a collection."""
        collection = self.get_collection(collection_name)
        result = collection.update_one(query, {'$set': update})
        return result.modified_count

    def update_many(self, collection_name: str, query: Dict[str, Any], update: Dict[str, Any]) -> int:
        """Update multiple documents in a collection."""
        collection = self.get_collection(collection_name)
        result = collection.update_many(query, {'$set': update})
        return result.modified_count

    def delete_one(self, collection_name: str, query: Dict[str, Any]) -> int:
        """Delete a single document from a collection."""
        collection = self.get_collection(collection_name)
        result = collection.delete_one(query)
        return result.deleted_count

    def delete_many(self, collection_name: str, query: Dict[str, Any]) -> int:
        """Delete multiple documents from a collection."""
        collection = self.get_collection(collection_name)
        result = collection.delete_many(query)
        return result.deleted_count

    def close(self) -> None:
        """Close the MongoDB connection."""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
            self.initialized = False

def get_mongodb_client() -> MongoDBClient:
    """Get the MongoDB client instance."""
    return MongoDBClient()
