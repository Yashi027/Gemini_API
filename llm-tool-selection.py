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

def get_current_time(query=None):
    return datetime.now().strftime("%I:%M:%S, %p")

def calculate(expression):
    try:
        return eval(expression)
    except Exception as ex:
        return "Invalid expression"

def motivational_quotes(query=None):
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

TOOLS = {
    "TIME_TOOL": get_current_time,
    "CALCULATOR_TOOL": calculate,
    "QUOTE_TOOL": motivational_quotes
}

def select_tool(query):
    prompt = f"""
    You are a tool selector. 
    Available tools:
    1. TIME_TOOL
    2. CALCULATOR_TOOL
    3. QUOTE_TOOL

    RETURN ONLY TOOL NAME
    User Query: {query}
    """
    response = client.models.generate_content(
                        model="gemini-3.1-flash-lite",
                        contents=prompt
                    )
    return response.text.strip()
    

def execute_tool(tool_name, query):
    tool = TOOLS.get(tool_name)
    if not tool:
        return "Tool not found"
    return tool(query)


while True:
    query = input("\n You: ")
    if query.lower() == "exit":
        break
    tool = select_tool(query)
    print(f"\n Selected tool : {tool}")

    result = execute_tool(tool, query)
    print(f"\n Assistant result: {result}")