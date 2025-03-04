
def recommend_products(user_profile, product_data, ai_suggested_products=None):
    """Filter and return product recommendations based on user preferences when AI does not find enough."""

    preferred_category = user_profile.preferred_category
    preferred_brand = user_profile.brand_preference
    budget_range = user_profile.budget_range
    preferred_color = getattr(user_profile, "color", None)

    if ai_suggested_products is None:
        ai_suggested_products = []
    elif isinstance(ai_suggested_products, dict):
        ai_suggested_products = [ai_suggested_products]

    recommended_products = ai_suggested_products[:]

    # If no preferred category exists, return only AI suggestions
    if not preferred_category:
        return recommended_products

    # Filter products based on user profile
    filtered_products = [
        p for p in product_data
        if p["category"].lower() == preferred_category.lower()
        and (not preferred_brand or any(b.lower() in p["brand"].lower() for b in preferred_brand))
        and (not preferred_color or p["color"].lower() == preferred_color.lower())
        and (budget_range[0] <= p["price"] <= budget_range[1])
        and p not in recommended_products
    ]

    # If AI did not suggest enough, add more based on user preferences
    if len(recommended_products) < 3:
        additional_needed = 3 - len(recommended_products)
        recommended_products.extend(filtered_products[:additional_needed])

    return recommended_products
