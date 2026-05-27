import requests

url = "http://localhost:8000/health"
headers = {
    "Origin": "http://localhost:5173",
    "Access-Control-Request-Method": "GET",
}

try:
    response = requests.options(url, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Headers: {response.headers}")
except Exception as e:
    print(f"Error: {e}")
