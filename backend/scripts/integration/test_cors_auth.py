import requests

url = "http://localhost:8000/api/v1/sessions/17/chat"
headers = {
    "Origin": "http://localhost:5173",
    "Content-Type": "application/json",
    "Authorization": "Bearer fake_token",
}
data = {"message": "hola"}

try:
    response = requests.post(url, headers=headers, json=data)
    print(f"Status: {response.status_code}")
    print(f"Headers: {response.headers}")
    print(f"Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")
