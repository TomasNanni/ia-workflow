import requests

BASE_URL = "http://localhost:8000/api/v1"

def test_create_session():
    # Attempt to create session without user_id in body
    # We need a token first, but let's see if we get a 422 even before auth if we simulate the call
    # Actually, we should get 401 if we don't provide a token, but let's see if the validation happens before or after auth dependency.
    # In FastAPI, dependencies are resolved before the body validation usually, but let's check.
    
    payload = {"title": "Test Session"}
    response = requests.post(f"{BASE_URL}/sessions", json=payload)
    print(f"POST /sessions response: {response.status_code}")
    print(response.json())

if __name__ == "__main__":
    try:
        test_create_session()
    except Exception as e:
        print(f"Error: {e}")
