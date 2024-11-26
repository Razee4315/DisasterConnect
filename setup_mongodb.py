from pymongo import MongoClient
from pymongo.errors import CollectionInvalid
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_mongodb():
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        
        # Create/Get database
        db = client['disasterconnect']
        
        # Create collections if they don't exist
        collections = ['users', 'incidents', 'resources']
        for collection in collections:
            try:
                db.create_collection(collection)
                logger.info(f"Created collection: {collection}")
            except CollectionInvalid:
                logger.info(f"Collection {collection} already exists")
        
        # Create indexes
        # Users collection
        db.users.create_index("username", unique=True)
        db.users.create_index("email", unique=True)
        
        # Incidents collection
        db.incidents.create_index([("location", "2dsphere")])
        db.incidents.create_index("status")
        db.incidents.create_index("severity")
        
        # Resources collection
        db.resources.create_index([("location", "2dsphere")])
        db.resources.create_index("status")
        db.resources.create_index("type")
        
        # Insert sample user for testing
        sample_user = {
            "username": "admin",
            "email": "admin@example.com",
            "password": "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918",  # admin
            "role": "admin",
            "created_at": "2024-03-17T00:00:00Z"
        }
        
        # Update admin user if exists, create if not
        db.users.update_one(
            {"username": "admin"},
            {"$set": sample_user},
            upsert=True
        )
        logger.info("Admin user created/updated")
        
        logger.info("MongoDB setup completed successfully!")
        
    except Exception as e:
        logger.error(f"Error setting up MongoDB: {str(e)}")
        raise
    finally:
        client.close()

if __name__ == "__main__":
    setup_mongodb()
