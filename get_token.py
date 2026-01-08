import requests
import json

url = "http://127.0.0.1:8000/api/login/"
data = {"username": "test", "password": "test123"}
headers = {"Content-Type": "application/json"}

response = requests.post(url, data=json.dumps(data), headers=headers)

if response.status_code == 200:
    tokens = response.json()
    print(tokens.get("access"))
else:
    print(f"Error: {response.status_code}")
    print(response.text)
