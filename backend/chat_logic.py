import openai
import json
import random
from backend.config import OPENAI_API_KEY, DATA_PATH
from backend.user_profile import get_user_profile

try:
    with open(DATA_PATH, "r") as file:
        product_data = json.load(file)
except FileNotFoundError:
    raise FileNotFoundError(f"⚠️ Cannot find 'products.json' at {DATA_PATH}. Ensure the file exists.")

openai.api_key = OPENAI_API_KEY

conversation_history = {}

def get_best_matching_product(user_message):
    """Finds the most relevant product from `products.json` based on user message."""
    user_message_lower = user_message.lower()

    matching_products = [
        p for p in product_data
        if p["name"].lower() in user_message_lower
        or p["category"].lower() in user_message_lower
        or p["brand"].lower() in user_message_lower
    ]

    if not matching_products:
        inferred_category = infer_category(user_message)
        if inferred_category:
            matching_products = [p for p in product_data if p["category"] == inferred_category]

    return matching_products[0] if matching_products else None

def infer_category(user_message):
    """Uses AI to infer the category when the user does not specify one."""
    category_list = list(set([p['category'] for p in product_data]))  # ✅ Ensure valid categories

    category_prompt = f"""
    You are an AI shopping assistant. Your job is to classify products into categories.

    **Available categories (STRICTLY choose one from this list):**
    {json.dumps(category_list)}

    **User Message:** "{user_message}"

    **Rules:**
    - ONLY return a category name from the list above.
    - DO NOT make up categories.
    - If unsure, return the closest matching category.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": category_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        inferred_category = response["choices"][0]["message"]["content"].strip()

        valid_categories = {p["category"] for p in product_data}
        if inferred_category in valid_categories:
            print(f"✅ AI-inferred category: {inferred_category}")
            return inferred_category
        else:
            print(f"⚠️ Invalid AI-inferred category: {inferred_category}, falling back to 'Unknown'")
            return "Unknown"

    except Exception as e:
        print(f"⚠️ Error inferring category: {e}")
        return "Unknown"


def suggest_alternative_products():
    """If no direct match, offer three random products as alternatives."""
    return random.sample(product_data, min(3, len(product_data)))

def get_ai_response(user_id, user_message):
    """
    Generates AI response using OpenAI GPT-4o-mini and updates user preferences.
    """
    if user_id not in conversation_history:
        conversation_history[user_id] = {"messages": [], "recommended_products": []}

    user_profile = get_user_profile(user_id)
    inferred_category = infer_category(user_message)

    price_mentions = [int(s) for s in user_message.split() if s.isdigit()]
    inferred_budget = [0, max(price_mentions)] if price_mentions else None
    inferred_brand = next((p["brand"] for p in product_data if p["brand"].lower() in user_message.lower()), None)
    inferred_color = next((p["color"] for p in product_data if p["color"].lower() in user_message.lower()), None)

    user_profile.update(user_message, inferred_category, inferred_budget, inferred_brand, inferred_color)

    suggested_product = get_best_matching_product(user_message)

    conversation_history[user_id]["messages"].append({"role": "user", "content": user_message})

    recommended_products = []

    if suggested_product:
        recommended_products.append(suggested_product) 
        ai_prompt = f"""
        You are an AI shopping assistant with a friendly and engaging personality. You remember previous conversations and continuously refine recommendations based on user preferences.

        **STRICT RULES:**
        - DO NOT suggest any product that is NOT in the list below.
        - If no clear match is found, present three valid options from the list.
        - If the user asks a follow-up question, refine recommendations accordingly.

        **Available Products (DO NOT go outside this list):**
        {json.dumps(product_data, indent=2)}

        **User Profile:**
        - Preferred Category: {user_profile.preferred_category or "Not set"}
        - Budget: ${user_profile.budget_range[0]} - ${user_profile.budget_range[1]}
        - Preferred Brands: {', '.join(user_profile.brand_preference) if user_profile.brand_preference else "None"}
        - Preferred Colors: {user_profile.color or "Not set"}

        **Product Recommendation:**
        - Name: {suggested_product['name']}
        - Category: {suggested_product['category']}
        - Brand: {suggested_product['brand']}
        - Price: ${suggested_product['price']}
        - Color: {suggested_product['color']}
        - Description: {suggested_product['short_description']}

        **Your Task:**
        1. **Respond in an engaging and natural tone**.
        2. **Acknowledge the user’s past requests** and maintain memory of preferences.
        3. **Provide the best matching product recommendation dynamically**.
        4. **NEVER suggest products outside of `products.json`**.
        5. If the user asks a follow-up question, adjust recommendations accordingly.
        6. Ask the user follow-up question to find more specific product if more than one product matches the request.
        7. Present product recommendations in an easy-to-read format.
        8. **Update {user_profile} in accordance to the user response.**
        """

    else:
        alternative_products = suggest_alternative_products()
        recommended_products.extend(alternative_products)

        inferred_category = infer_category(user_message)
        if inferred_category:
            user_profile.preferred_category = inferred_category

        price_mentions = [int(s) for s in user_message.split() if s.isdigit()]
        if price_mentions:
            user_profile.budget_range = [0, max(price_mentions)]

        for product in product_data:
            if product["color"].lower() in user_message.lower():
                user_profile.color = product["color"] 
                break

        ai_prompt = f"""
        The user did not provide enough details for a specific product match.

        **STRICT RULES:**
        - DO NOT suggest any product that is NOT in the list below.
        - You must only pick products from the available list.

        **Available Products (MUST CHOOSE FROM THIS LIST ONLY):**
        {json.dumps(product_data, indent=2)}

        **Here are three product suggestions:**

        **1️⃣ {alternative_products[0]['name']}**  
        - 💰 **Price:** ${alternative_products[0]['price']}  
        - 🏷️ **Brand:** {alternative_products[0]['brand']}  
        - 📂 **Category:** {alternative_products[0]['category']}  
        - 🎨 **Color:** {alternative_products[0]['color']}  
        - 📝 **Description:** {alternative_products[0]['short_description']}  


        **2️⃣ {alternative_products[1]['name']}**  
        - 💰 **Price:** ${alternative_products[1]['price']}  
        - 🏷️ **Brand:** {alternative_products[1]['brand']}  
        - 📂 **Category:** {alternative_products[1]['category']}  
        - 🎨 **Color:** {alternative_products[1]['color']}  
        - 📝 **Description:** {alternative_products[1]['short_description']}


        **3️⃣ {alternative_products[2]['name']}**  
        - 💰 **Price:** ${alternative_products[2]['price']}  
        - 🏷️ **Brand:** {alternative_products[2]['brand']}  
        - 📂 **Category:** {alternative_products[2]['category']}  
        - 🎨 **Color:** {alternative_products[2]['color']}  
        - 📝 **Description:** {alternative_products[2]['short_description']}  

        **Would you like one of these, or do you have something more specific in mind?**
        """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": ai_prompt},
            *conversation_history[user_id]["messages"]
        ]
    )


    ai_response = response["choices"][0]["message"]["content"]

    conversation_history[user_id]["recommended_products"] = recommended_products

    conversation_history[user_id]["messages"].append({"role": "assistant", "content": ai_response})

    return ai_response, user_profile.to_dict(), recommended_products
