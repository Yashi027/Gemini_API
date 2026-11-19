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

print("Career Agent")

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
        "certifications":["AWS Cloud Certified Practitioner", "AWS Cloud Associate"]
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

def get_projects(role: str):
    """
    Return project recommendations
    """
    return {
        "role": role,
        "projects": ["AI Chatbot", "PDF Rag Assistant", "Research Agent", "Career Coach Agent"]
    }

TOOL_REGISTRY = {
    "SKILL_TOOL": get_skills,
    "CERTIFICATION_TOOL":get_certification,
    "PROJECT_TOOL": get_projects,
    "SALARY_TOOL":get_salary
}

class CarrerCoachAgent:
    def __init__(self, role):
        self.role = role
        self.observation = []

    def think(self):
        prompt = f"""
            You are an AI career Coach Agent.
            User Role: {self.role}

            Available tools: 
            CERTIFICATION_TOOL
            SKILL_TOOL
            PROJECT_TOOL
            SALARY_TOOL

            Previous Observation: {self.observation}
            Think Carefully. Decide what information you still need.
            Return Only One: 
                SKILL_TOOL
                PROJECT_TOOL
                CERTIFICATION_TOOL
                SALARY_TOOL
                EXIT
        """
        try:
            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt
            )

            return response.text.strip().upper()

        except Exception as e:
            print("Gemini API Error:", e)
            return "EXIT"

    def execute_action(self,action):
        tool = TOOL_REGISTRY.get(action)
        if tool:
            return tool(self.role)
        return None

    def generate_final_plan(self):
        prompt = f"""
            User Role: {self.role}
            Collected Info: {self.observation}
            Generate: 
            1. Career summary
            2. Skills required
            3. Projects
            4. Certifications Required
            5. Salary
            6. 90 Day Learning roadmap
        """
        response = client.models.generate_content(
                            model="gemini-3.1-flash-lite",
                            contents=prompt
                    )
        print("======Final Plan=====")
        print(response.text)


    # ReAct
    def run(self):
        step = 1
        while True:
            print("="*6)
            print(f"Step: {step}")
            print("="*6)

            # Thought
            action = self.think()
            print("Thought")
            print(action)

            # finish
            if(action == "EXIT"):
                print("Done")
                break

            # Action
            print("Action")
            result = self.execute_action(action)
            print(result)

            #Observation
            print("Observation")

            self.observation.append(result)
            step += 1

        self.generate_final_plan()


role = input("Enter your career goal: ")
agent = CarrerCoachAgent(role)
agent.run()