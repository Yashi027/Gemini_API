from google import genai
from dotenv import load_dotenv
import os
import time
from datetime import datetime
import random

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

def get_current_time():
    return datetime.now().strftime("%I:%M:%S, %p")

def calculate(expression):
    try:
        return eval(expression)
    except Exception as ex:
        return "Invalid expression"

def motivational_quotes():
    quotes = [
        "Consistency is the key to success",
        "Hardwork beats Talent",
        "Action speaks more than words"
    ]
    return random.choice(quotes)

def route_tool():
    query=query.lower()
    if "time" in query:
        return "time"
    elif "quote" in query:
        return "quote"
    elif "calculator" in query:
        return "calculator"
    return "gemini"

while True:
    user_input = input("Prompt: ")
    if user_input.lower() in ["bye","exit","quit"]:
        break
    tool = route_tool(user_input)
    if tool == "time":
        result = get_current_time()
        print(f"Assistant: Current time is: {result}")
    elif tool == "calculator":
        expression = (user_input.replace("calculate","").strip())
        result = calculate(expression)
        print(f"Assistant: Result = {result}")
    elif tool == "quote":
        result = motivational_quotes()
        print(f"Assistant: Quote of the day is: {result}")
    else:
        response = client.models.generate_content_stream(
                    model="gemini-3.1-flash-lite",
                    contents=user_input
                )
        print(F"Assistant: {response.text}")

    