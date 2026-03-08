"""
Test signup endpoint
"""
import requests
import json

url = "http://localhost:8000/auth/candidate/signup"
payload = {
    "email": "test@example.com",
    "name": "Test User",
    "password": "SecurePass123!",
    "gender": "male",
    "college": "MIT",
    "engineer_level": "senior"
}

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")
    print(f"Response text: {response.text if 'response' in locals() else 'No response'}")
