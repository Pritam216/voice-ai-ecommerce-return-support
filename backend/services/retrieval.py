import json

with open("data/orders.json") as f:
    orders = json.load(f)

with open("data/policies.json") as f:
    policies = json.load(f)


def find_order(order_id):
    for order in orders:
        if order["order_id"].lower() == order_id.lower():
            return order
    return None


def get_policy(keyword):
    keyword = keyword.lower()
    for key, value in policies.items():
        if keyword in key.lower():
            return {key: value}
    return None


# services/retrieval.py
# import json

# with open("data/orders.json") as f: ORDERS = json.load(f)
# with open("data/policies.json") as f: POLICIES = json.load(f)

# def get_order_info(user_id="U1"):
#     msgs = []
#     for o in ORDERS:
#         if o["user_id"]==user_id:
#             if o["status"]=="delivered":
#                 msgs.append(f"{o['item']} delivered on {o['delivery_date']}.")
#             elif o["status"]=="in_transit":
#                 msgs.append(f"{o['item']} in transit, expected {o.get('expected_delivery','soon')}.")
#     return "\n".join(msgs) if msgs else "No orders found."

# def get_policy_info(topic):
#     return POLICIES.get(topic, "Policy not found")