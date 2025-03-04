# AI Shopping Assistant – Project Report

## Introduction

The AI Shopping Assistant is a conversational agent designed to assist users in discovering products, refining preferences, and making informed purchasing decisions. It utilizes multi-turn dialogue, user profiling, and real-time recommendations to create a personalized shopping experience.

This project integrates OpenAI's GPT-4o-mini, a FastAPI backend, and a Streamlit-based frontend to deliver an interactive and dynamic AI shopping assistant.

---

## How It Works (Architecture Overview)

The system is split into two main parts: the backend (API) and the frontend (chat UI).

### 1. Frontend (Streamlit UI)

    - Built using Streamlit for simplicity and real-time updates.
    - Shows the chat history, recommended products, and lets users interact with the AI.
    - Calls the backend API whenever a user sends a message.

### 2. Backend (FastAPI)

    - Uses OpenAI GPT-4o-mini to generate natural responses.
    - Stores and updates a user profile dynamically based on conversation.
    - Pulls product recommendations from a local JSON file (products.json).
    - Ensures that recommendations improve as the conversation progresses.

### 3. AI Chat + User Memory

    - The AI extracts user preferences (category, brand, budget, color) from chat.
    - If a product matches exactly, it gets recommended.
    - If no perfect match exists, the system suggests alternatives based on preferences.
    - If no good alternatives exist, it picks random products (but avoids totally irrelevant ones).

---

## Key Features

- **Conversational AI** – It actually chats, not just searches.
- **User Profile Memory** – The AI remembers preferences across conversations.
- **Real-time Product Recommendations** – Dynamically updates based on new info.
- **Multi-turn Interaction** – The longer you chat, the smarter the recommendations get.
- **Lightweight JSON-based Database** – Easy to modify and expand product offerings.

---

## 🛠️ Tech Stack (Tool used)

Here’s what I used to build this:

| Tool               | What It Does                                      |
|--------------------|--------------------------------------------------|
| **FastAPI**       | Runs the backend and handles API requests.       |
| **OpenAI GPT-4o-mini** | Generates chat responses and infers user preferences. |
| **Streamlit**     | Creates the frontend chat interface.             |
| **Uvicorn**       | Runs the FastAPI server.                         |
| **Requests**      | Handles API communication between frontend and backend. |
| **Python 3.13.1** | The programming language for the whole project.  |
| **JSON**         | Stores the product database (simple but effective). |


---

## Future Improvements

If I had more time, I’d love to add: 
🔹 Clarifying Questions – If the AI isn’t sure what you want, it could ask instead of guessing.
🔹 A Bigger Product Database – More categories and brands would make the recommendations better.
🔹 Persistent User Profiles – Right now, preferences reset when you restart. Saving them would make the AI even smarter.

---

## Final Thoughts

This project was super fun and challenging. It’s more than just a chatbot—it actually remembers and refines suggestions based on real conversations. AI-powered shopping assistants are a cool idea, and I think this could be a great foundation for a more advanced version.

Hope you like it! Let me know if you have any feedback. 🚀