import os
import json
from typing import Optional, Dict
from pymongo import MongoClient
from datetime import datetime, timedelta
import hashlib
import secrets

class AuthManager:
    def __init__(self):
        self.mongo_client = MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.mongo_client.disasterconnect
        self.users = self.db.users
        self._current_user = None
        
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        salt = secrets.token_hex(16)
        hash_obj = hashlib.sha256((password + salt).encode())
        return f"{salt}:{hash_obj.hexdigest()}"
    
    def verify_password(self, stored_hash: str, password: str) -> bool:
        """Verify password against stored hash"""
        salt, hash_value = stored_hash.split(':')
        hash_obj = hashlib.sha256((password + salt).encode())
        return hash_obj.hexdigest() == hash_value
    
    def register_user(self, username: str, password: str, email: str) -> bool:
        """Register a new user"""
        if self.users.find_one({'username': username}):
            return False
            
        user_doc = {
            'username': username,
            'password': self.hash_password(password),
            'email': email,
            'created_at': datetime.utcnow(),
            'last_login': None,
            'is_active': True,
            'role': 'user'
        }
        
        self.users.insert_one(user_doc)
        return True
    
    def login(self, username: str, password: str) -> Optional[Dict]:
        """Login user and return user data if successful"""
        user = self.users.find_one({'username': username})
        if not user or not self.verify_password(user['password'], password):
            return None
            
        user['last_login'] = datetime.utcnow()
        self.users.update_one(
            {'_id': user['_id']},
            {'$set': {'last_login': user['last_login']}}
        )
        
        self._current_user = user
        return {
            'username': user['username'],
            'email': user['email'],
            'role': user['role']
        }
    
    def logout(self):
        """Logout current user"""
        self._current_user = None
    
    @property
    def current_user(self) -> Optional[Dict]:
        """Get current logged in user"""
        return self._current_user
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return self._current_user is not None
