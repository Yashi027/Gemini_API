from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("Gemini api key not found")

client = genai.Client(
    api_key=API_KEY
)

print("Gemini Chatbot for career skills")

def get_skills(role: str):
    """
    Returns required skills for a role
    Parameters: role(str) - Career role selected by user
    Return: dict: required skills
    """

    return {
        "role": role,
        "skills": ["Python", "ML", "DL", "LLM", "Prompt Engineering"]
    }

def get_certification(role: str):
    """
    Returns certification info
    Parameters: role(str): Career role
    Returns: dict
    """
    return {
        "role":role,
        "certifications":["AWS Cloud Certified Practitioner", "AWS Cloud Practitioner"]
    }

def get_salary(role: str):
    """
    Returns employee salary
    Parameter: role(str): Career role
    Return: dict
    """

    return {
        "role" : role,
        "salary_range": "15-20LPA"
    }

tools = [get_skills, get_certification, get_salary]

chat = client.chats.create(
    model="gemini-3.1-flash-lite",
    config=types.GenerateContentConfig(tools=tools)
)

query = input("Prompt:")
response = chat.send_message(query)
print(response.text)