from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from backend.chat_logic import get_ai_response
from backend.user_profile import get_user_profile
from backend.recommendation import recommend_products
from backend.config import DATA_PATH

app = FastAPI()

try:
    with open(DATA_PATH, "r") as file:
        product_data = json.load(file)
except FileNotFoundError:
    raise FileNotFoundError(f"⚠️ Cannot find 'products.json' at {DATA_PATH}. Ensure the file exists.")

class ChatRequest(BaseModel):
    user_id: str
    message: str

class RecommendRequest(BaseModel):
    user_id: str

@app.post("/chat")
async def chat(request: ChatRequest):
    """Handles user messages and returns AI responses."""
    ai_message, user_profile_dict, suggested_product = get_ai_response(request.user_id, request.message)

    user_profile = get_user_profile(request.user_id)

    # Update the stored user profile with AI-inferred details
    user_profile.preferred_category = user_profile_dict.get("preferred_category", user_profile.preferred_category)
    user_profile.budget_range = user_profile_dict.get("budget_range", user_profile.budget_range)
    user_profile.brand_preference = user_profile_dict.get("brand_preference", user_profile.brand_preference)
    user_profile.color = user_profile_dict.get("color", user_profile.color)

    # Ensure AI-suggested product appears in recommendations
    recommendations = recommend_products(user_profile, product_data, suggested_product)

    return {
        "response": ai_message,
        "user_profile": user_profile.to_dict(),
        "recommendations": recommendations 
    }

@app.post("/recommend")
async def recommend(request: RecommendRequest):
    """Returns product recommendations based on user preferences."""
    user_profile = get_user_profile(request.user_id)

    if not user_profile:
        raise HTTPException(status_code=400, detail="User profile not found. Start a chat first.")

    recommendations = recommend_products(user_profile, product_data)
    return {"recommendations": recommendations}
