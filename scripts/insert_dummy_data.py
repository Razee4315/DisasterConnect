from pymongo import MongoClient
from datetime import datetime, timedelta
import random

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['disasterconnect']

def clear_existing_data():
    """Delete all existing records from incidents and resources collections"""
    db.incidents.delete_many({})
    db.resources.delete_many({})
    print("Existing records deleted successfully")

def generate_dummy_incidents():
    """Generate dummy incident data with Pakistani locations"""
    
    # Pakistani locations with precise coordinates (longitude, latitude format for MongoDB)
    locations = [
        {"area": "Hunza Valley, Gilgit-Baltistan", "coords": [74.866667, 36.316667], "lat": 36.316667, "lng": 74.866667},
        {"area": "Skardu Valley", "coords": [75.717773, 35.245619], "lat": 35.245619, "lng": 75.717773},
        {"area": "Islamabad", "coords": [73.015137, 33.687782], "lat": 33.687782, "lng": 73.015137},
        {"area": "Chitral Valley", "coords": [71.786900, 35.850800], "lat": 35.850800, "lng": 71.786900},
        {"area": "Naltar Valley", "coords": [74.184300, 36.157700], "lat": 36.157700, "lng": 74.184300},
        {"area": "Kaghan Valley", "coords": [73.759300, 34.905400], "lat": 34.905400, "lng": 73.759300},
        {"area": "Swat Valley", "coords": [72.425800, 35.222700], "lat": 35.222700, "lng": 72.425800},
        {"area": "Neelum Valley", "coords": [74.332000, 34.589000], "lat": 34.589000, "lng": 74.332000},
        {"area": "Astore Valley", "coords": [74.850000, 35.366700], "lat": 35.366700, "lng": 74.850000},
        {"area": "Shigar Valley", "coords": [75.738900, 35.428100], "lat": 35.428100, "lng": 75.738900}
    ]
    
    incident_types = ["Flood", "Earthquake", "Fire", "Landslide", "Industrial Accident", 
                     "Building Collapse", "Gas Leak", "Chemical Spill"]
    severity_levels = ["High", "Medium", "Low", "Critical"]
    status_options = ["Active", "Resolved", "In Progress", "Under Review"]
    
    incidents = []
    for _ in range(20):  # Generate 20 incidents
        location = random.choice(locations)
        created_at = datetime.now() - timedelta(days=random.randint(0, 30))
        
        incident = {
            "title": f"{random.choice(incident_types)} in {location['area']}",
            "type": random.choice(incident_types),
            "severity": random.choice(severity_levels),
            "status": random.choice(status_options),
            "location": {
                "type": "Point",
                "coordinates": location['coords'],
                "area": location['area'],
                "description": f"Precise location in {location['area']}",
                "lat": location['lat'],
                "lng": location['lng']
            },
            "description": f"Emergency situation reported in {location['area']}",
            "created_at": created_at
        }
        incidents.append(incident)
    
    db.incidents.insert_many(incidents)
    print(f"{len(incidents)} incidents inserted successfully")

def generate_dummy_resources():
    """Generate dummy resource data with Pakistani locations"""
    
    # Pakistani locations with precise coordinates for resources (longitude, latitude format)
    locations = [
        {"area": "Shimshal Pass", "coords": [75.341200, 36.447100], "lat": 36.447100, "lng": 75.341200},
        {"area": "Khunjerab Pass", "coords": [75.421900, 36.850000], "lat": 36.850000, "lng": 75.421900},
        {"area": "Babusar Pass", "coords": [74.053300, 35.209700], "lat": 35.209700, "lng": 74.053300},
        {"area": "Lowari Pass", "coords": [71.816700, 35.583300], "lat": 35.583300, "lng": 71.816700},
        {"area": "Shandur Pass", "coords": [72.524400, 36.068300], "lat": 36.068300, "lng": 72.524400},
        {"area": "Karakoram Base", "coords": [76.513300, 35.862300], "lat": 35.862300, "lng": 76.513300},
        {"area": "Concordia Camp", "coords": [76.517200, 35.744700], "lat": 35.744700, "lng": 76.517200},
        {"area": "Baltoro Glacier", "coords": [76.645800, 35.725800], "lat": 35.725800, "lng": 76.645800},
        {"area": "Biafo Glacier", "coords": [75.553300, 35.914700], "lat": 35.914700, "lng": 75.553300},
        {"area": "Passu Glacier", "coords": [74.866600, 36.485000], "lat": 36.485000, "lng": 74.866600}
    ]
    
    resource_types = {
        "Ambulance": {"capacity": [2, 4]},
        "Fire Truck": {"capacity": [6, 8]},
        "Rescue Vehicle": {"capacity": [4, 6]},
        "Medical Supply Unit": {"capacity": [100, 500]},
        "Emergency Response Team": {"capacity": [5, 15]},
        "Mobile Hospital": {"capacity": [20, 50]},
        "Water Tanker": {"capacity": [1000, 5000]},
        "Relief Supplies Vehicle": {"capacity": [200, 1000]}
    }
    
    status_options = ["Available", "Deployed", "Maintenance", "Reserved"]
    
    resources = []
    for _ in range(30):  # Generate 30 resources
        location = random.choice(locations)
        resource_type = random.choice(list(resource_types.keys()))
        capacity_range = resource_types[resource_type]["capacity"]
        
        resource = {
            "name": f"{resource_type}-{random.randint(100, 999)}",
            "type": resource_type,
            "status": random.choice(status_options),
            "capacity": random.randint(capacity_range[0], capacity_range[1]),
            "location": {
                "type": "Point",
                "coordinates": location['coords'],
                "area": location['area'],
                "description": f"Stationed at {location['area']}",
                "lat": location['lat'],
                "lng": location['lng']
            },
            "created_at": datetime.now() - timedelta(days=random.randint(0, 60))
        }
        resources.append(resource)
    
    db.resources.insert_many(resources)
    print(f"{len(resources)} resources inserted successfully")

if __name__ == "__main__":
    try:
        clear_existing_data()
        generate_dummy_incidents()
        generate_dummy_resources()
        print("Dummy data insertion completed successfully!")
    except Exception as e:
        print(f"Error occurred: {str(e)}")
    finally:
        client.close()
