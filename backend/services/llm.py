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

#     prompt = f"""
# You are an e-commerce support assistant.
# User query: {query}
# Context: {context}
# Conversation history:
# {history_text}

# Answer clearly and briefly.
# """

#     try:
#         response = co.generate(
#             model="command-r-03-2025",  # Cohere's text generation model
#             prompt=prompt,
#             max_tokens=200,
#             temperature=0.6,
#             stop_sequences=["User:", "Assistant:"]
#         )
#         return response.generations[0].text.strip()
#     except Exception as e:
#         print(f"Error generating response from Cohere: {e}")
#         return "Sorry, I couldn't process your request."

# # import google.generativeai as genai
# # from dotenv import load_dotenv
# # import os

# # load_dotenv()

# # genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# # model = genai.GenerativeModel("gemini-2.5-flash-lite")

# import cohere
# from dotenv import load_dotenv
# import os

# load_dotenv()

# # COHERE_API_KEY = os.getenv("COHERE_API_KEY")
# # co = cohere.Client(COHERE_API_KEY)

# co = cohere.Client(os.getenv("COHERE_API_KEY"))

# def generate_response(prompt_text, context=None, history=None):
#     """
#     Generate a response using Cohere Chat API
#     """
#     # Build the chat messages
#     messages = [
#         {"role": "system", "content": "You are a helpful support assistant."},
#     ]

#     # Include previous conversation in history if needed
#     if history:
#         for h in history:
#             if "user" in h:
#                 messages.append({"role": "user", "content": h["user"]})
#             if "assistant" in h:
#                 messages.append({"role": "assistant", "content": h["assistant"]})

#     # Add current user prompt
#     messages.append({"role": "user", "content": prompt_text})

#     # Call Cohere Chat API
#     response = co.chat(
#         model="command-a-03-2025",  # new chat model
#         message=messages,
#         temperature=0.7,
#     )

#     # Extract text from response
#     reply_text = response['choices'][0]['message']['content']

#     return reply_text


# # llm.py
# import cohere
# from dotenv import load_dotenv
# import os

# # Load environment variables
# load_dotenv()

# COHERE_API_KEY = os.getenv("COHERE_API_KEY")
# if not COHERE_API_KEY:
#     raise ValueError("COHERE_API_KEY not set in .env")

# co = cohere.Client(COHERE_API_KEY)
# chat_history = []

# def generate_response(prompt_text, history=None):
#     """
#     Generate a response using Cohere Chat API
#     """
#     # Build chat_history for Cohere
#     if history:
#         for h in history:
#             if "user" in h:
#                 chat_history.append({"role": "USER", "message": h["user"]})
#             if "assistant" in h:
#                 chat_history.append({"role": "CHATBOT", "message": h["assistant"]})

#     # Call Cohere Chat API
#     response = co.chat(
#         model="command-a-03-2025",
#         message=prompt_text,        # single string
#         chat_history=chat_history   # optional previous conversation
#     )

#     # Extract assistant reply correctly from the object
#     reply_text = response.text
#     return reply_text


# # # Quick test
# # if __name__ == "__main__":
# #     prompt = "Hello! How are you?"
# #     print(generate_response(prompt))


# # services/llm.py
# import cohere
# from dotenv import load_dotenv
# import os

# # Load environment variables
# load_dotenv()

# COHERE_API_KEY = os.getenv("COHERE_API_KEY")
# co = cohere.Client(COHERE_API_KEY)

# def generate_response(user_query, chat_history=None):
#     """
#     user_query: str
#     chat_history: list of dicts [{'user': '...', 'assistant': '...'}]
#     """
#     # Build messages array for Cohere Chat
#     messages = []
#     if chat_history:
#         for msg in chat_history:
#             messages.append({"role": "user", "content": msg["user"]})
#             messages.append({"role": "assistant", "content": msg["assistant"]})
    
#     # Append current query
#     messages.append({"role": "user", "content": user_query})
    
#     # Call Cohere Chat API
#     response = co.chat(
#         model="command-a-03-2025",  # choose your model
#         message=messages,
#         max_tokens=150,
#         temperature=0.7
#     )
    
#     # Return assistant response text
#     return response.message.content