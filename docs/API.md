# DisasterConnect API Documentation

## Overview

The DisasterConnect API provides programmatic access to disaster response coordination features. This RESTful API allows you to manage incidents, resources, and communications programmatically.

## Authentication

All API requests require authentication using JWT (JSON Web Tokens).

```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" https://api.disasterconnect.local/v1/incidents
```

### Obtaining a Token

```bash
POST /api/v1/auth/token
```

Request body:
```json
{
    "username": "your_username",
    "password": "your_password"
}
```

Response:
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer",
    "expires_in": 3600
}
```

## API Endpoints

### Incidents

#### List Incidents

```bash
GET /api/v1/incidents
```

Query parameters:
- `status` (string): Filter by incident status
- `severity` (string): Filter by severity level
- `page` (integer): Page number for pagination
- `limit` (integer): Results per page

Response:
```json
{
    "incidents": [
        {
            "id": "inc_123",
            "title": "Flood in Downtown",
            "status": "active",
            "severity": "high",
            "location": {
                "lat": 40.7128,
                "lng": -74.0060
            },
            "created_at": "2023-11-14T12:00:00Z"
        }
    ],
    "total": 100,
    "page": 1,
    "limit": 10
}
```

#### Create Incident

```bash
POST /api/v1/incidents
```

Request body:
```json
{
    "title": "Flood in Downtown",
    "description": "Severe flooding reported",
    "severity": "high",
    "location": {
        "lat": 40.7128,
        "lng": -74.0060
    }
}
```

### Resources

#### List Resources

```bash
GET /api/v1/resources
```

Query parameters:
- `type` (string): Filter by resource type
- `status` (string): Filter by status
- `page` (integer): Page number
- `limit` (integer): Results per page

#### Assign Resource

```bash
POST /api/v1/incidents/{incident_id}/resources
```

Request body:
```json
{
    "resource_id": "res_456",
    "assignment_duration": "2h",
    "priority": "high"
}
```

### Communications

#### Send Message

```bash
POST /api/v1/messages
```

Request body:
```json
{
    "recipient_id": "user_789",
    "content": "Emergency response needed",
    "priority": "high"
}
```

#### Get Messages

```bash
GET /api/v1/messages
```

Query parameters:
- `since` (timestamp): Get messages after timestamp
- `limit` (integer): Number of messages to return

## Webhooks

### Register Webhook

```bash
POST /api/v1/webhooks
```

Request body:
```json
{
    "url": "https://your-server.com/webhook",
    "events": ["incident.created", "resource.assigned"]
}
```

### Webhook Events

- `incident.created`
- `incident.updated`
- `resource.assigned`
- `resource.updated`
- `message.sent`

## Rate Limiting

- 1000 requests per hour per API key
- Rate limit headers included in responses:
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`

## Error Handling

### Error Responses

```json
{
    "error": {
        "code": "unauthorized",
        "message": "Invalid or expired token",
        "details": {
            "token_expired_at": "2023-11-14T13:00:00Z"
        }
    }
}
```

### Common Error Codes

- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `429`: Too Many Requests
- `500`: Internal Server Error

## SDKs and Libraries

- [Python SDK](https://github.com/Razee4315/DisasterConnect-python)
- [JavaScript SDK](https://github.com/Razee4315/DisasterConnect-js)

## Examples

### Python Example

```python
from disasterconnect import DisasterConnectClient

client = DisasterConnectClient('your_api_key')

# Create an incident
incident = client.incidents.create(
    title="Flood in Downtown",
    description="Severe flooding reported",
    severity="high",
    location={"lat": 40.7128, "lng": -74.0060}
)

# Assign a resource
client.incidents.assign_resource(
    incident_id=incident.id,
    resource_id="res_456",
    assignment_duration="2h"
)
```

### JavaScript Example

```javascript
const DisasterConnect = require('disasterconnect');

const client = new DisasterConnect('your_api_key');

// List active incidents
client.incidents.list({ status: 'active' })
    .then(incidents => {
        console.log(incidents);
    })
    .catch(error => {
        console.error(error);
    });
```

## Support

For API support:
- Email: saqlainrazee@gmail.com
- GitHub Issues: [Report a bug](https://github.com/Razee4315/DisasterConnect/issues)
- API Status: [status.disasterconnect.local](https://status.disasterconnect.local)
