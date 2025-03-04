# 🛍️ AI Shopping Assistant

## 📌 Introduction

AI Shopping Assistant is a conversational agent designed to help users **discover products, refine preferences, and make informed purchase decisions**. It holds **multi-turn dialogues**, remembers user preferences, and provides **dynamic product recommendations**.

This project was built using **OpenAI's GPT-4o-mini, Streamlit for UI, and Python for backend processing**.

---

## 🚀 Features

✅ **Multi-turn AI-powered chat**  
✅ **User Profile Memory** (remembers preferred brands, categories, budget, and color)  
✅ **Dynamic Product Recommendations** based on AI understanding and user preferences  
✅ **Real-time UI Updates** with Streamlit  
✅ **Local JSON Product Database** (easily customizable)  

---

## 🛠️ Installation Guide

### **1. Clone the Repository**
```sh
git clone https://github.com/GilEizenberg/ai-shopping-assistant.git
cd ai-shopping-assistant
```

### **2. Create & Activate Virtual Environment**

Mac/Linux
```sh
python3 -m venv venv
source venv/bin/activate
```
Windows
```sh
python -m venv venv
venv\Scripts\activate
```

### **3. Install Dependencies**

```sh
pip install -r requirements.txt
```

### **4. Set Up Configuration**

Create a .env file in the root directory and add your OpenAI API Key:
```ini
OPENAI_API_KEY=your_openai_api_key_here
```

### **5. Start the Backend**

```sh
uvicorn backend.app:app --reload
```
or

```sh
python -m uvicorn backend.app:app --reload
```

### **6. Start the Frontend**

```sh
streamlit run frontend/app.py
```
or

```sh
python -m streamlit run frontend/app.py
```

App will be available at: http://localhost:8501

---

## 📝 Usage Guide

- Open the chat interface (localhost:8501).
- Start a conversation (e.g., "I want running shoes for $100").
- AI remembers your preferences over time.
- See personalized product recommendations in the sidebar.
- AI refines recommendations as you keep chatting.

---

## 🔧 API Endpoints

### Base URL: http://127.0.0.1:8000

### 1. Send a Chat Message & Get AI Response

    Method: POST
    Endpoint: /chat
    Description: Sends a user message to the AI assistant and receives a response along with updated user preferences.

### 2. Fetch Product Recommendations

    Method: POST
    Endpoint: /recommend
    Description: Retrieves product recommendations based on the user profile.

### Example API Request (Using cURL)
```sh
curl -X POST http://127.0.0.1:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"user_id": "user123", "message": "I want running shoes"}'

```
### Example API Response
```json
{
  "response": "Great choice! Here are the details for the Running Shoes...",
  "user_profile": {
    "preferred_category": "footwear",
    "budget_range": [0, 1000000],
    "brand_preference": ["Nike"],
    "color": "Red"
  },
  "recommendations": [
    {
      "name": "Running Shoes",
      "category": "Footwear",
      "price": 89.99,
      "brand": "Nike",
      "color": "Red",
      "short_description": "Comfortable and durable running shoes."
    }
  ]
}
```

---

## 🛒 Customizing the Product Catalog

You can modify backend/products.json to include your own products.
Simply edit the JSON file and restart the backend:
```json
[
  {
    "name": "Gaming Mouse",
    "category": "Electronics",
    "price": 49.99,
    "brand": "Razer",
    "color": "Black",
    "short_description": "High-performance gaming mouse with customizable buttons."
  }
]
```
---

## 📦 Project Structure:

```bash
project-root/
│── backend/
│   ├── app.py                # FastAPI server
│   ├── chat_logic.py         # Chat handling logic
│   ├── recommendation.py     # Recommendation system
│   ├── user_profile.py       # User profile management
│   ├── config.py             # Configuration settings
│   ├── products.json         # Product dataset
│
│── frontend/
│   ├── app.py                # Streamlit UI
│   ├── api_client.py         # Handles API requests to backend
│
│── README.md
│── requirements.txt

```

---

## 🛠️ Troubleshooting

### 1️. OpenAI API Key Error

- Ensure you have added OPENAI_API_KEY in .env
- If using Windows, run:

```sh
set OPENAI_API_KEY=your_key_here
```
- If using Mac/Linux:
```sh
export OPENAI_API_KEY=your_key_here
```

### 2. Backend Not Responding

- Run uvicorn backend.app:app --reload before starting the frontend.
- Check for API errors in the terminal.
- Ensure port 8000 is free.

### 3️. UI Not Updating

- Restart Streamlit:
```sh
streamlit run frontend/app.py
```
- Check st.session_state updates in app.py.