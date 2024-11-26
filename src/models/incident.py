from datetime import datetime
from typing import List, Dict, Optional
from bson import ObjectId
from pymongo import MongoClient
import os

class IncidentManager:
    def __init__(self):
        self.mongo_client = MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.mongo_client.disasterconnect
        self.incidents = self.db.incidents
        
    def create_incident(self, data: Dict) -> str:
        """Create a new incident"""
        incident = {
            'title': data['title'],
            'type': data['type'],
            'severity': data['severity'],
            'location': data['location'],
            'description': data['description'],
            'status': 'active',
            'resources_assigned': [],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'created_by': data['created_by'],
            'coordinates': data.get('coordinates', None)
        }
        
        result = self.incidents.insert_one(incident)
        return str(result.inserted_id)
        
    def update_incident(self, incident_id: str, data: Dict) -> bool:
        """Update an existing incident"""
        data['updated_at'] = datetime.utcnow()
        result = self.incidents.update_one(
            {'_id': ObjectId(incident_id)},
            {'$set': data}
        )
        return result.modified_count > 0
        
    def get_incident(self, incident_id: str) -> Optional[Dict]:
        """Get incident by ID"""
        incident = self.incidents.find_one({'_id': ObjectId(incident_id)})
        if incident:
            incident['_id'] = str(incident['_id'])
        return incident
        
    def list_incidents(self, filters: Dict = None) -> List[Dict]:
        """List all incidents with optional filters"""
        query = filters or {}
        incidents = list(self.incidents.find(query).sort('created_at', -1))
        for incident in incidents:
            incident['_id'] = str(incident['_id'])
        return incidents
        
    def assign_resource(self, incident_id: str, resource_id: str) -> bool:
        """Assign a resource to an incident"""
        result = self.incidents.update_one(
            {'_id': ObjectId(incident_id)},
            {'$addToSet': {'resources_assigned': resource_id}}
        )
        return result.modified_count > 0
        
    def unassign_resource(self, incident_id: str, resource_id: str) -> bool:
        """Remove a resource from an incident"""
        result = self.incidents.update_one(
            {'_id': ObjectId(incident_id)},
            {'$pull': {'resources_assigned': resource_id}}
        )
        return result.modified_count > 0
        
    def close_incident(self, incident_id: str, resolution_notes: str) -> bool:
        """Close an incident"""
        result = self.incidents.update_one(
            {'_id': ObjectId(incident_id)},
            {
                '$set': {
                    'status': 'closed',
                    'closed_at': datetime.utcnow(),
                    'resolution_notes': resolution_notes
                }
            }
        )
        return result.modified_count > 0
