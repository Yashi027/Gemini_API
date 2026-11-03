from google import genai
from dotenv import load_dotenv
import os
import time

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("Gemini api key not found")

client = genai.Client(
    api_key=API_KEY
)

history = []
MAX_HISTORY=20

system_prompt = """
You are a friendly AI assistant
1. Be profeesional
2. Keep answers clean and concise
3. Remember previous conversational context
"""

print("====Gemini Chatbot====")

while True:
    user_input = input("Prompt: ")
    if user_input.lower() in ["bye","exit","quit"]:
        break
    history.append(f"User: {user_input}")

    if len(history) > MAX_HISTORY:
        history = history[-MAX_HISTORY:]

    conversational_context = system_prompt+ "\n"
    conversational_context += "\n".join(history)

    start_time = time.time()
    fullResponse = ""

    try:
        stream = client.models.generate_content_stream(
            model="gemini-3.1-flash-lite",
            contents=conversational_context
        )

        for chunk in stream:
            if chunk.text:
                print(chunk.text, end="", flush=True)
                fullResponse += chunk.text

        endTime = time.time()
        total_time = endTime-start_time
        print(f"\n Response time: {total_time}")

        history.append(f"Assisstant: {fullResponse}")
    except Exception as ex:
        print("Error")
        print(ex)
        continue
    