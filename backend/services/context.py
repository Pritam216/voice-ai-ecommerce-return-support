import re
from services.retrieval import find_order, get_policy

def get_context(transcription):
    text = transcription.lower()

    # 1. Extract order ID
    match = re.search(r'ord\d+', text)
    if match:
        order = find_order(match.group().upper())
        if order:
            return {"order": order}

    # 2. Policy intents
    if "return" in text:
        return get_policy("returns")

    if "refund" in text:
        return get_policy("refunds")

    if "cancel" in text:
        return get_policy("cancellation")

    if "replace" in text or "exchange" in text:
        return get_policy("replacement")

    if "delivery" in text or "shipping" in text:
        return get_policy("shipping")

    return None


# services/context.py
# import streamlit as st

# def init_session():
#     if "history" not in st.session_state:
#         st.session_state.history = []

# def add_message(user_text, assistant_text):
#     st.session_state.history.append({"user": user_text, "assistant": assistant_text})

# def reset_history():
#     st.session_state.history = []