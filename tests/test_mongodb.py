import os
import pytest
from unittest.mock import patch, MagicMock, PropertyMock
from pymongo.errors import ConnectionFailure
from src.utils.mongodb_client import MongoDBClient

@pytest.fixture(autouse=True)
def setup_environment():
    """Set up environment variables for testing."""
    os.environ['MONGODB_URI'] = 'mongodb://localhost:27017'
    os.environ['MONGODB_DATABASE'] = 'test_db'
    yield
    # Clean up
    os.environ.pop('MONGODB_URI', None)
    os.environ.pop('MONGODB_DATABASE', None)

@pytest.fixture(autouse=True)
def reset_singleton():
    """Reset the MongoDB client singleton between tests."""
    MongoDBClient._instance = None
    MongoDBClient._client = None
    MongoDBClient._db = None
    yield

@patch('src.utils.mongodb_client.MongoClient')
def test_successful_connection(mock_mongo_client):
    """Test successful MongoDB connection."""
    # Setup mock
    mock_client = MagicMock()
    mock_client.admin.command.return_value = True
    mock_mongo_client.return_value = mock_client

    # Initialize client
    client = MongoDBClient()
    client.initialize_connection()

    # Verify
    mock_mongo_client.assert_called_once_with('mongodb://localhost:27017')
    mock_client.admin.command.assert_called_once_with('ping')
    assert client.initialized is True

@patch('src.utils.mongodb_client.MongoClient')
def test_insert_one(mock_mongo_client):
    """Test insert_one operation."""
    # Setup mock
    mock_client = MagicMock()
    mock_db = MagicMock()
    mock_collection = MagicMock()
    
    mock_client.admin.command.return_value = True
    mock_client.__getitem__.return_value = mock_db
    mock_db.__getitem__.return_value = mock_collection
    mock_collection.insert_one.return_value.inserted_id = 'test_id'
    
    mock_mongo_client.return_value = mock_client

    # Perform insert
    client = MongoDBClient()
    result = client.insert_one('test_collection', {'test': 'data'})

    # Verify
    mock_collection.insert_one.assert_called_once_with({'test': 'data'})
    assert result == 'test_id'

@patch('src.utils.mongodb_client.MongoClient')
def test_find_one(mock_mongo_client):
    """Test find_one operation."""
    # Setup mock
    mock_client = MagicMock()
    mock_db = MagicMock()
    mock_collection = MagicMock()
    
    mock_client.admin.command.return_value = True
    mock_client.__getitem__.return_value = mock_db
    mock_db.__getitem__.return_value = mock_collection
    mock_collection.find_one.return_value = {'test': 'data'}
    
    mock_mongo_client.return_value = mock_client

    # Perform find
    client = MongoDBClient()
    result = client.find_one('test_collection', {'test': 'data'})

    # Verify
    mock_collection.find_one.assert_called_once_with({'test': 'data'})
    assert result == {'test': 'data'}

@patch('src.utils.mongodb_client.MongoClient')
def test_connection_error(mock_mongo_client):
    """Test connection error handling."""
    # Setup mock to raise ConnectionFailure
    mock_mongo_client.side_effect = ConnectionFailure("Connection failed")

    # Initialize client
    client = MongoDBClient()

    # Verify that connection error is raised
    with pytest.raises(Exception) as exc_info:
        client.initialize_connection()
    assert "Failed to connect to MongoDB: Connection failed" in str(exc_info.value)

@patch('src.utils.mongodb_client.MongoClient')
def test_singleton_pattern(mock_mongo_client):
    """Test that MongoDBClient follows singleton pattern."""
    # Setup mock
    mock_client = MagicMock()
    mock_mongo_client.return_value = mock_client
    mock_client.admin.command.return_value = True

    # Create two instances
    client1 = MongoDBClient()
    client2 = MongoDBClient()

    # Verify they are the same instance
    assert client1 is client2

def test_missing_env_vars():
    """Test handling of missing environment variables."""
    # Remove environment variables
    os.environ.pop('MONGODB_URI', None)
    os.environ.pop('MONGODB_DATABASE', None)

    # Initialize client
    client = MongoDBClient()

    # Verify that ValueError is raised
    with pytest.raises(ValueError) as exc_info:
        client.initialize_connection()
    assert "MongoDB connection details not found in environment variables" in str(exc_info.value)
