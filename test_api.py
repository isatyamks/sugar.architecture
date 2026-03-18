import requests
import json

url = "http://localhost:8000/api/v1/reflect"
data = {
    "context": {
        "activity_id": "act-555",
        "bundle_id": "org.laptop.Write",
        "title": "My Volcano Essay",
        "description": "An essay about how volcanoes work.",
        "mime_type": "text/plain",
        "tags": ["writing", "science"],
        "duration_seconds": 900
    },
    "learner": {
        "age": 10,
        "language": "en"
    }
}

print("Sending request to FastAPI backend...") 
try:
    response = requests.post(url, json=data, timeout=60)
    print(f"Status Code: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")
