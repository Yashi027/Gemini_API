from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("Gemini api key not found")

client = genai.Client(
    api_key=API_KEY
)

history = []

system_prompt = """
You are a friendly AI assistant
1. Be profeesional
2. Keep answers clean and concise
3. Remember previous conversational context
"""

print("====Gemini Chatbot====")

while True:
    user_input = input("Prompt: ")
    if user_input.lower in ["bye","exit","quit"]:
        break
    history.append(f"User: {user_input}")
    conversational_context = system_prompt+ "\n"
    conversational_context += "\n".join(history)

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=conversational_context
        )

        bot_response = response.text

        print("Gemini: {bot_response}")

        history.append(f"Assisstant: {bot_response}")
    except Exception as ex:
        print("Gemini service temporarily unavailable")
        continue
    