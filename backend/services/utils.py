import json

orders = json.load(open("data/orders.json"))
policies = json.load(open("data/policies.json"))

def find_order_info(user_id, text):
    """Return order information matching user and keywords."""
    text_lower = text.lower()
    for o in orders:
        if o["user_id"] == user_id:
            if o["order_id"].lower() in text_lower or o["item"].lower() in text_lower:
                return o
    return None

def get_policy_response(text):
    """Return relevant policy text if keyword matches."""
    for key, info in policies.items():
        if key in text.lower():
            return f"{key} policy: {info}"
    return None