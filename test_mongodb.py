from src.utils.mongodb_client import mongodb_client
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

try:
    # Test connection
    db = mongodb_client.get_database()
    
    # Try to insert a test document
    result = db.test_collection.insert_one({"test": "connection"})
    print(f"Successfully inserted document with id: {result.inserted_id}")
    
    # Clean up test document
    db.test_collection.delete_one({"test": "connection"})
    print("Successfully cleaned up test document")
    
except Exception as e:
    print(f"Error connecting to MongoDB: {str(e)}")
finally:
    # Close the connection
    mongodb_client.close_connection()
