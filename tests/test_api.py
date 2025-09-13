import requests
import json

# Test data
test_data = {
    "user_id": "U1234",
    "timestamp": "2025-06-15 14:30:00",
    "ip_address": "192.168.1.100",
    "geo_location": "United States of America",
    "device_id": "DF_5555",
    "login_hour": 14,
    "is_new_device": 0,
    "bytes_in": 150000,
    "bytes_out": 250000,
    "success": 1
}

# Send a POST request to the API
response = requests.post('http://localhost:5000/predict', json=test_data)

# Print the response
print("Status Code:", response.status_code)
print("Response:", response.json())