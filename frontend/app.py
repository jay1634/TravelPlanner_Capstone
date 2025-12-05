import uuid
import streamlit as st
from datetime import date as dt_date

from api_client import api_chat, api_generate_itinerary


# =========================
# ✅ PAGE CONFIG
# =========================
st.set_page_config(page_title="Travel Planner Chatbot", layout="wide")


# =========================
# ✅ SESSION STATE
# =========================
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []   # list of {"role": "user"/"assistant", "content": str}

if "itinerary_text" not in st.session_state:
    st.session_state.itinerary_text = ""


# =========================
# ✅ TITLE
# =========================
st.title("🧳 Travel Planner Chatbot (Groq + RAG + Memory)")


# =========================
# ✅ SIDEBAR — ITINERARY
# =========================
with st.sidebar:
    st.header("Itinerary Parameters")

    destination = st.text_input("Destination city", value="Goa")
    days = st.number_input("Days", min_value=1, max_value=10, value=3)
    budget = st.number_input("Total budget", min_value=100.0, value=500.0)

    interests = st.multiselect(
        "Interests",
        ["beach", "culture", "history", "shopping", "nightlife", "food"],
        default=["food", "culture"],
    )

    food_pref = st.selectbox(
        "Food preference", ["no preference", "vegetarian", "non-veg"], index=0
    )

    if st.button("Generate Itinerary"):
        try:
            res = api_generate_itinerary(
                st.session_state.session_id,
                destination,
                int(days),
                float(budget),
                interests,
                food_pref,
            )
            st.session_state.itinerary_text = res["itinerary_text"]
            st.success("✅ Itinerary generated!")
        except Exception as e:
            st.error(f"❌ Error: {e}")

    st.markdown("---")
    if st.button("🔄 Clear Chat"):
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.success("Chat cleared!")


# =========================
# ✅ CHAT DISPLAY (LIKE CHATGPT)
# =========================
st.subheader("💬 Chat with the assistant")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# =========================
# ✅ CHAT INPUT (ENTER TO SEND)
# =========================
name = st.text_input("Your name", value="Traveler")

user_msg = st.chat_input("Type your message and press Enter...")

if user_msg:
    try:
        # ✅ Show user message instantly
        st.session_state.messages.append(
            {"role": "user", "content": user_msg}
        )

        # ✅ Send same session_id to backend (CRITICAL for memory)
        res = api_chat(
            st.session_state.session_id,
            user_msg,
            name if name.strip() else None,
        )

        # ✅ Store assistant reply
        st.session_state.messages.append(
            {"role": "assistant", "content": res["reply"]}
        )

        # ✅ Force UI refresh (prevents double messages)
        st.rerun()

    except Exception as e:
        st.error(f"❌ Error calling backend: {e}")


# =========================
# ✅ ITINERARY DISPLAY
# =========================
st.markdown("---")
st.subheader("🗺️ Generated Itinerary")

if st.session_state.itinerary_text:
    st.text_area("Itinerary", st.session_state.itinerary_text, height=300)
else:
    st.info("Use the sidebar to generate an itinerary.")
