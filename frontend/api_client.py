import requests

# Backend API URL
API_URL = "http://127.0.0.1:8000"

def send_chat_message(user_id, message):
    """Send a user message to the AI assistant and get a response."""
    response = requests.post(f"{API_URL}/chat", json={"user_id": user_id, "message": message})
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to communicate with the backend"}

def get_recommendations(user_id):
    """Fetch product recommendations based on user preferences."""
    response = requests.post(f"{API_URL}/recommend", json={"user_id": user_id})
    if response.status_code == 200:
        return response.json().get("recommendations", [])
    else:
        return []
