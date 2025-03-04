import streamlit as st
from api_client import send_chat_message, get_recommendations

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "user_profile" not in st.session_state:
    st.session_state.user_profile = {}

if "recommendations" not in st.session_state:
    st.session_state.recommendations = []

# User ID (Simulated for now)
USER_ID = "user123"

with st.sidebar:
    st.sidebar.markdown('<h2 style="text-align: center;">🛍️ Recommended Products</h2>', unsafe_allow_html=True)
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)

    recommendations_flat = [
        item for sublist in st.session_state.recommendations 
        for item in (sublist if isinstance(sublist, list) else [sublist])
    ]

    if recommendations_flat:
        for product in recommendations_flat:
            if isinstance(product, dict) and "name" in product:
                with st.sidebar.container():
                    st.write(f"**{product.get('name', 'Unknown Product')}**")
                    st.write(f"💰 **Price:** ${product.get('price', 'N/A')}")
                    st.write(f"🏷️ **Brand:** {product.get('brand', 'N/A')}")
                    st.write(f"📂 **Category:** {product.get('category', 'N/A')}")
                    st.write(f"🎨 **Color:** {product.get('color', 'N/A')}")
                    st.write(f"📝 {product.get('short_description', 'No description available')}")
                    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    else:
        st.sidebar.write("No recommendations yet. Start a conversation to get suggestions!")

st.title("💬 AI Shopping Assistant")

chat_container = st.container()

with chat_container:
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.write(chat["content"])

user_input = st.chat_input("Ask me about products...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    st.session_state.chat_history.append({"role": "user", "content": user_input})

    data = send_chat_message(USER_ID, user_input)

    if "error" in data:
        st.error(data["error"])
    else:
        ai_response = data["response"]

        if "user_profile" in data and isinstance(data["user_profile"], dict):
            st.session_state.user_profile.update(data["user_profile"])

        if "recommendations" in data:
            st.session_state.recommendations = [
                item for sublist in data["recommendations"] 
                for item in (sublist if isinstance(sublist, list) else [sublist])
            ]

        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})

        with chat_container:
            for chat in st.session_state.chat_history:
                with st.chat_message(chat["role"]):
                    st.write(chat["content"])

        st.rerun()
