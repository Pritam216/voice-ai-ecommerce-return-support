import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash-lite")


def generate_response(query, context, history):
    prompt = f"""
You are an e-commerce support assistant.
User query: {query}
Context: {context}
history : {history}

Answer clearly and briefly.
"""
    response = model.generate_content(prompt)
    return response.text.strip()




# import os
# from dotenv import load_dotenv
# import cohere

# load_dotenv()

# COHERE_API_KEY = os.getenv("COHERE_API_KEY")
# co = cohere.Client(COHERE_API_KEY)  # Initialize Cohere client

# def generate_response(query, context, history):
#     """
#     Generate a response from Cohere LLM for the e-commerce assistant.

#     Args:
#         query (str): User query text
#         context (str): Context from policies/orders
#         history (list): Conversation history

#     Returns:
#         str: Generated response
#     """
#     # Flatten history for context
#     history_text = ""
#     for msg in history:
#         if "user" in msg:
#             history_text += f"User: {msg['user']}\n"
#         else:
#             history_text += f"Assistant: {msg['assistant']}\n"

