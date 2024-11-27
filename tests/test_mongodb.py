import os
import pytest
from unittest.mock import patch, MagicMock
from src.utils.mongodb_client import MongoDBClient

@pytest.fixture(autouse=True)
def mock_env_vars():
    """Automatically mock environment variables for all tests."""
    with patch.dict(os.environ, {
        'MONGODB_URI': 'mongodb://localhost:27017',
        'MONGODB_DATABASE': 'test_db'
    }):
        yield

@pytest.fixture
def mock_mongo_client():
    """Mock PyMongo client."""
    with patch('pymongo.MongoClient') as mock_client:
        # Create mock instances
        client_instance = MagicMock()
        db_instance = MagicMock()
        collection_instance = MagicMock()

        # Setup mock chain
        mock_client.return_value = client_instance
        client_instance.__getitem__.return_value = db_instance
        db_instance.__getitem__.return_value = collection_instance

        yield {
            'client': mock_client,
            'client_instance': client_instance,
            'db': db_instance,
            'collection': collection_instance
        }

@pytest.fixture
def mongodb_client():
    """Create a fresh MongoDB client instance for each test."""
    client = MongoDBClient()
    client.client = None  # Reset connection
    client.db = None
    return client

def test_singleton_pattern():
    """Test that MongoDBClient follows singleton pattern."""
    client1 = MongoDBClient()
    client2 = MongoDBClient()
    assert client1 is client2

def test_lazy_initialization(mongodb_client):
    """Test that connection is initialized only when needed."""
    assert mongodb_client.client is None
    assert mongodb_client.db is None

def test_successful_connection(mongodb_client, mock_mongo_client):
    """Test successful database connection."""
    mongodb_client.initialize_connection()
    
    mock_mongo_client['client'].assert_called_once_with('mongodb://localhost:27017')
    assert mongodb_client.client is not None
    assert mongodb_client.db is not None

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

def test_close_connection(mongodb_client, mock_mongo_client):
    """Test closing the database connection."""
    mongodb_client.initialize_connection()
    mongodb_client.close()
    
    mock_mongo_client['client_instance'].close.assert_called_once()
    assert mongodb_client.client is None
    assert mongodb_client.db is None
