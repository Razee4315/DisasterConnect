import pytest
from unittest.mock import patch, MagicMock
from src.utils.mongodb_client import MongoDBClient

@pytest.fixture
def mock_mongodb():
    with patch('pymongo.MongoClient') as mock_client:
        # Create a mock client instance
        client_instance = MagicMock()
        mock_client.return_value = client_instance
        
        # Mock the database and collection
        db = MagicMock()
        collection = MagicMock()
        client_instance.__getitem__.return_value = db
        db.__getitem__.return_value = collection
        
        yield mock_client

def test_mongodb_connection(mock_mongodb):
    with patch.dict('os.environ', {
        'MONGODB_URI': 'mongodb://localhost:27017',
        'MONGODB_DATABASE': 'test_db'
    }):
        client = MongoDBClient()
        assert client.client is not None
        assert client.db is not None

def test_mongodb_operations(mock_mongodb):
    with patch.dict('os.environ', {
        'MONGODB_URI': 'mongodb://localhost:27017',
        'MONGODB_DATABASE': 'test_db'
    }):
        client = MongoDBClient()
        
        # Test insert operation
        test_data = {"name": "test"}
        client.insert_one("test_collection", test_data)
        client.db["test_collection"].insert_one.assert_called_once_with(test_data)
        
        # Test find operation
        client.find_one("test_collection", {"name": "test"})
        client.db["test_collection"].find_one.assert_called_once_with({"name": "test"})

def test_mongodb_error_handling(mock_mongodb):
    # Test connection error
    mock_mongodb.side_effect = Exception("Connection failed")
    
    with pytest.raises(Exception):
        with patch.dict('os.environ', {
            'MONGODB_URI': 'mongodb://localhost:27017',
            'MONGODB_DATABASE': 'test_db'
        }):
            MongoDBClient()
