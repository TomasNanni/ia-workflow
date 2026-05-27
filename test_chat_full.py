import requests

base_url = "http://localhost:8000/api/v1"

# 1. Login
login_data = {
    "email": "user1@example.com",
    "password": "password1"
}
try:
    response = requests.post(f"{base_url}/auth/login", json=login_data)
    if response.status_code != 200:
        print(f"Login failed: {response.status_code} {response.text}")
        exit(1)
    
    token = response.json()["access_token"]
    print(f"Token obtained: {token[:10]}...")
    
    # 2. Chat
    chat_url = f"{base_url}/sessions/17/chat"
    headers = {
        "Origin": "http://localhost:5173",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    data = {"message": "List tables"}
    
    print(f"Sending chat request to {chat_url}...")
    response = requests.post(chat_url, headers=headers, json=data)
    print(f"Status: {response.status_code}")
    print(f"Headers: {response.headers}")
    print(f"Body: {response.text}")
    
except Exception as e:
    print(f"Error: {e}")
