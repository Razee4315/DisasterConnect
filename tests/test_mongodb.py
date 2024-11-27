import os
import pytest
from unittest.mock import patch, MagicMock
from pymongo.errors import ConnectionFailure
from bson import ObjectId
from src.utils.mongodb_client import MongoDBClient, get_mongodb_client

@pytest.fixture(autouse=True)
def mock_env_vars():
    """Mock environment variables for all tests."""
    with patch.dict(os.environ, {
        'MONGODB_URI': 'mongodb://localhost:27017',
        'MONGODB_DATABASE': 'test_db'
    }):
        yield

@pytest.fixture
def mongodb_client():
    """Get a MongoDB client instance."""
    client = get_mongodb_client()
    client._client = None
    client._db = None
    client.initialized = False
    return client

@pytest.fixture
def mock_mongo_client():
    """Create mock MongoDB client."""
    with patch('src.utils.mongodb_client.MongoClient') as mock_client:
        client_instance = MagicMock()
        db = MagicMock()
        collection = MagicMock()
        
        # Setup mock chain
        mock_client.return_value = client_instance
        client_instance.__getitem__.return_value = db
        db.__getitem__.return_value = collection
        client_instance.admin.command.return_value = True
        
        return {
            'client': mock_client,
            'client_instance': client_instance,
            'db': db,
            'collection': collection
        }

def test_singleton_pattern():
    """Test that MongoDBClient follows singleton pattern."""
    client1 = get_mongodb_client()
    client2 = get_mongodb_client()
    assert client1 is client2

def test_lazy_initialization(mongodb_client):
    """Test that connection is initialized only when needed."""
    assert mongodb_client._client is None
    assert mongodb_client._db is None

def test_successful_connection(mongodb_client, mock_mongo_client):
    """Test successful database connection."""
    mongodb_client.initialize_connection()
    mock_mongo_client['client'].assert_called_once_with('mongodb://localhost:27017')
    mock_mongo_client['client_instance'].admin.command.assert_called_once_with('ping')
    assert mongodb_client.initialized is True

def test_insert_one(mongodb_client, mock_mongo_client):
    """Test inserting a single document."""
    test_doc = {"name": "test"}
    collection = mock_mongo_client['collection']
    collection.insert_one.return_value.inserted_id = "test_id"

    result = mongodb_client.insert_one("test_collection", test_doc)
    collection.insert_one.assert_called_once_with(test_doc)
    assert result == "test_id"

def test_find_one(mongodb_client, mock_mongo_client):
    """Test finding a single document."""
    test_query = {"name": "test"}
    expected_doc = {"_id": "test_id", "name": "test"}
    collection = mock_mongo_client['collection']
    collection.find_one.return_value = expected_doc

    result = mongodb_client.find_one("test_collection", test_query)
    collection.find_one.assert_called_once_with(test_query)
    assert result == expected_doc

def test_connection_error(mock_mongo_client):
    """Test handling of connection errors."""
    mock_mongo_client['client'].side_effect = ConnectionFailure("Connection failed")
    client = get_mongodb_client()
    client._client = None

    with pytest.raises(Exception) as exc_info:
        client.initialize_connection()
    assert "Failed to connect to MongoDB: Connection failed" in str(exc_info.value)

def test_missing_env_vars():
    """Test handling of missing environment variables."""
    with patch.dict(os.environ, {}, clear=True):
        client = get_mongodb_client()
        with pytest.raises(ValueError) as exc_info:
            client.initialize_connection()
        assert "MongoDB connection details not found in environment variables" in str(exc_info.value)
