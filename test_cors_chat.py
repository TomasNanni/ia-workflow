import requests

url = "http://localhost:8000/api/v1/sessions/17/chat"
headers = {
    "Origin": "http://localhost:5173",
    "Access-Control-Request-Method": "POST",
    "Access-Control-Request-Headers": "authorization,content-type",
}

try:
    response = requests.options(url, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Headers: {response.headers}")
except Exception as e:
    print(f"Error: {e}")
