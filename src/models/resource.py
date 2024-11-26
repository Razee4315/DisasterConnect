from datetime import datetime
from typing import List, Dict, Optional
from bson import ObjectId
from pymongo import MongoClient
import os

class ResourceManager:
    def __init__(self):
        self.mongo_client = MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.mongo_client.disasterconnect
        self.resources = self.db.resources
        
    def create_resource(self, data: Dict) -> str:
        """Create a new resource"""
        resource = {
            'name': data['name'],
            'type': data['type'],
            'status': 'available',
            'capacity': data.get('capacity', None),
            'location': data['location'],
            'description': data['description'],
            'contact_info': data.get('contact_info', None),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'created_by': data['created_by'],
            'current_incident': None,
            'maintenance_status': 'operational'
        }
        
        result = self.resources.insert_one(resource)
        return str(result.inserted_id)
        
    def update_resource(self, resource_id: str, data: Dict) -> bool:
        """Update an existing resource"""
        data['updated_at'] = datetime.utcnow()
        result = self.resources.update_one(
            {'_id': ObjectId(resource_id)},
            {'$set': data}
        )
        return result.modified_count > 0
        
    def get_resource(self, resource_id: str) -> Optional[Dict]:
        """Get resource by ID"""
        resource = self.resources.find_one({'_id': ObjectId(resource_id)})
        if resource:
            resource['_id'] = str(resource['_id'])
        return resource
        
    def list_resources(self, filters: Dict = None) -> List[Dict]:
        """List all resources with optional filters"""
        query = filters or {}
        resources = list(self.resources.find(query))
        for resource in resources:
            resource['_id'] = str(resource['_id'])
        return resources
        
    def assign_to_incident(self, resource_id: str, incident_id: str) -> bool:
        """Assign resource to an incident"""
        result = self.resources.update_one(
            {'_id': ObjectId(resource_id)},
            {
                '$set': {
                    'status': 'assigned',
                    'current_incident': incident_id,
                    'updated_at': datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0
        
    def release_from_incident(self, resource_id: str) -> bool:
        """Release resource from current incident"""
        result = self.resources.update_one(
            {'_id': ObjectId(resource_id)},
            {
                '$set': {
                    'status': 'available',
                    'current_incident': None,
                    'updated_at': datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0
        
    def mark_maintenance(self, resource_id: str, status: str, notes: str = None) -> bool:
        """Mark resource for maintenance"""
        update_data = {
            'maintenance_status': status,
            'status': 'maintenance',
            'maintenance_notes': notes,
            'maintenance_start': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = self.resources.update_one(
            {'_id': ObjectId(resource_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0
        
    def complete_maintenance(self, resource_id: str) -> bool:
        """Complete maintenance and mark resource as available"""
        update_data = {
            'maintenance_status': 'operational',
            'status': 'available',
            'maintenance_end': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = self.resources.update_one(
            {'_id': ObjectId(resource_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0
