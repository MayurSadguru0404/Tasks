import os
import google.generativeai as genai
from realtime_search import google_search

GEMINI_API_KEY = os.getenv("Your_key")
if not GEMINI_API_KEY:
    raise Exception("GEMINI_API_KEY not found. Set it in environment variables.")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

chat_history = []  


def generate_reply(query):
    """
    Uses Gemini + Google Search (realtime) + chat memory
    """

    search_info = google_search(query)

    conversation = ""
    for msg in chat_history[-12:]:
        conversation += f"User: {msg['user']}\nAI: {msg['assistant']}\n"

    prompt = f"""
You are an intelligent AI assistant with access to real-time web information.

Conversation History (last messages):
{conversation}

User Query:
{query}

Relevant Google Search Data:
{search_info}

Respond naturally, short and helpful.
"""

    response = model.generate_content(prompt).text

    chat_history.append({"user": query, "assistant": response})

    return response

if __name__ == "__main__":
    print("\n🤖 Gemini AI Chatbot Online!")
    print("Type 'exit' to stop.\n")

    while True:
        user_input = input("User: ")

        if user_input.lower().strip() in ["exit", "quit"]:
            print("\nChat Ended. Thank you! 👋")
            break

        bot_reply = generate_reply(user_input)
        print("AI:", bot_reply)

