# DisasterConnect API Documentation

## API Overview
DisasterConnect provides a comprehensive API for managing disaster response operations. This document outlines the available endpoints, authentication methods, and data structures.

## Authentication

### User Authentication
```http
POST /api/auth/login
Content-Type: application/json

{
    "username": "string",
    "password": "string"
}
```

Response:
```json
{
    "token": "string",
    "user": {
        "id": "string",
        "username": "string",
        "role": "string"
    }
}
```

### Token Validation
```http
GET /api/auth/validate
Authorization: Bearer <token>
```

Response:
```json
{
    "valid": true,
    "user": {
        "id": "string",
        "username": "string",
        "role": "string"
    }
}
```

## Database Schema

### Users Collection
```javascript
{
  _id: ObjectId,
  username: String,
  email: String,
  password_hash: String,
  role: String,  // "admin" or "operator"
  created_at: DateTime,
  last_login: DateTime
}
```

### Incidents Collection
```javascript
{
  _id: ObjectId,
  type: String,
  location: {
    type: "Point",
    coordinates: [longitude, latitude]
  },
  severity: String,  // "Low", "Medium", "High", "Critical"
  description: String,
  status: String,  // "Open", "In Progress", "Resolved", "Closed"
  assigned_resources: [ObjectId],  // References to resources
  created_by: ObjectId,  // Reference to user
  created_at: DateTime,
  updated_at: DateTime,
  resolved_at: DateTime
}
```

### Resources Collection
```javascript
{
  _id: ObjectId,
  name: String,
  type: String,  // "Vehicle", "Personnel", "Equipment"
  status: String,  // "Available", "Deployed", "Maintenance"
  capabilities: [String],
  location: {
    type: "Point",
    coordinates: [longitude, latitude]
  },
  assigned_to: ObjectId,  // Reference to incident
  maintenance_history: [{
    date: DateTime,
    description: String,
    performed_by: ObjectId
  }],
  created_at: DateTime,
  updated_at: DateTime
}
```

## API Endpoints

### Incidents

#### List Incidents
```http
GET /api/incidents
Authorization: Bearer <token>
```

Query Parameters:
- `status` (string): Filter by status
- `type` (string): Filter by incident type
- `severity` (string): Filter by severity
- `from_date` (string): Filter by date range start
- `to_date` (string): Filter by date range end
- `page` (integer): Page number
- `limit` (integer): Items per page

#### Create Incident
```http
POST /api/incidents
Authorization: Bearer <token>
Content-Type: application/json

{
    "type": "string",
    "location": {
        "coordinates": [number, number]
    },
    "severity": "string",
    "description": "string"
}
```

#### Update Incident
```http
PUT /api/incidents/{incident_id}
Authorization: Bearer <token>
Content-Type: application/json

{
    "status": "string",
    "severity": "string",
    "description": "string"
}
```

### Resources

#### List Resources
```http
GET /api/resources
Authorization: Bearer <token>
```

Query Parameters:
- `status` (string): Filter by status
- `type` (string): Filter by resource type
- `page` (integer): Page number
- `limit` (integer): Items per page

#### Create Resource
```http
POST /api/resources
Authorization: Bearer <token>
Content-Type: application/json

{
    "name": "string",
    "type": "string",
    "capabilities": ["string"],
    "location": {
        "coordinates": [number, number]
    }
}
```

#### Update Resource
```http
PUT /api/resources/{resource_id}
Authorization: Bearer <token>
Content-Type: application/json

{
    "status": "string",
    "location": {
        "coordinates": [number, number]
    }
}
```

## Error Handling

### Error Response Format
```json
{
    "error": {
        "code": "string",
        "message": "string",
        "details": {}
    }
}
```

### Common Error Codes
- `AUTH_001`: Authentication failed
- `AUTH_002`: Token expired
- `AUTH_003`: Invalid token
- `VAL_001`: Validation error
- `DB_001`: Database operation failed
- `RES_001`: Resource not found
- `RES_002`: Resource already exists

## Rate Limiting

Rate limiting is implemented to ensure API stability:

- Anonymous requests: 60 requests per hour
- Authenticated requests: 1000 requests per hour
- Burst: 10 requests per second

Rate limit headers:
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1623456789
```

## Versioning

The API uses URL versioning:
- Current version: `/api/v1`
- Legacy support: `/api/v0` (deprecated)

## Best Practices

1. Always include authentication token
2. Use appropriate HTTP methods
3. Handle rate limiting gracefully
4. Implement proper error handling
5. Cache responses when appropriate

## Support

For API support:
- Email: api-support@disasterconnect.com
- Documentation: api.disasterconnect.com
- Status: status.disasterconnect.com
