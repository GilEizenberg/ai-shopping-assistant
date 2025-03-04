import json
import difflib
import re
from backend.config import DATA_PATH

try:
    with open(DATA_PATH, "r") as file:
        product_data = json.load(file)
except FileNotFoundError:
    raise FileNotFoundError(f"⚠️ Cannot find 'products.json' at {DATA_PATH}. Ensure the file exists.")

ALL_CATEGORIES = {p["category"].lower() for p in product_data}
ALL_BRANDS = {p["brand"].lower() for p in product_data}
ALL_COLORS = {p["color"].lower() for p in product_data}

class UserProfile:
    """Stores and updates user preferences dynamically."""

    def __init__(self):
        self.preferred_category = None
        self.budget_range = [0, 1_000_000]  
        self.brand_preference = []
        self.color = None  

    def update(self, message, inferred_category=None, inferred_budget=None, inferred_brand=None, inferred_color=None):
        """Dynamically update user preferences based on AI-inferred input and user message."""
        message_lower = message.lower()

        # Detect category
        if inferred_category and inferred_category.lower() in ALL_CATEGORIES:
            self.preferred_category = inferred_category.lower()
        else:
            matched_category = difflib.get_close_matches(message_lower, ALL_CATEGORIES, n=1, cutoff=0.8)
            if matched_category:
                self.preferred_category = matched_category[0]

        # Detect budget
        if inferred_budget:
            self.budget_range = inferred_budget
        else:
            extracted_prices = [int(s) for s in re.findall(r'\d+', message_lower)]
            if extracted_prices:
                self.budget_range = [0, max(extracted_prices)]

        # Detect brand
        if inferred_brand and inferred_brand.lower() in ALL_BRANDS:
            if inferred_brand.lower() not in self.brand_preference:
                self.brand_preference.append(inferred_brand.lower())
        else:
            matched_brand = difflib.get_close_matches(message_lower, ALL_BRANDS, n=1, cutoff=0.7)
            if matched_brand and matched_brand[0] not in self.brand_preference:
                self.brand_preference.append(matched_brand[0])

        # Detect color
        if inferred_color and inferred_color.lower() in ALL_COLORS:
            self.color = inferred_color.lower()
        else:
            matched_color = difflib.get_close_matches(message_lower, ALL_COLORS, n=1, cutoff=0.7)
            if matched_color:
                self.color = matched_color[0]

        print(f"🔍 Updated User Profile: {self.to_dict()}")

    def to_dict(self):
        """Convert user profile to dictionary for frontend display."""
        return {
            "preferred_category": self.preferred_category,
            "budget_range": self.budget_range,
            "brand_preference": self.brand_preference,
            "color": self.color
        }

user_profiles = {}

def get_user_profile(user_id):
    """Retrieve or create a user profile."""
    if user_id not in user_profiles:
        user_profiles[user_id] = UserProfile()
    return user_profiles[user_id]
