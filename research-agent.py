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

class Research_Agent:
    def __init__(self, role):
        self.role = role
        self.observation = []
        self.plan = []
        self.evidence = []
    # Create Plan
    def create_research_plan(self):
        print("[Research] Planner Agent is creating a plan...")
        prompt = f"""
            You are a Research Planner Agent.
            User Role: {self.role}

            Available tools: 
            CERTIFICATION_TOOL
            SKILL_TOOL
            PROJECT_TOOL
            SALARY_TOOL

            Your task: Create the best research plan.

            Strict Rules:
            1. Use only required tools. 
            2. Do not use unnecessary tools.
            3. Return only one tool per line.
            4. Return only tool names.
            5. Treat collected tool observations as the ONLY source of verified information.
            6. Never invent facts, skills, certifications, projects or salary figures.
            7. If information is missing, explicitly write "Information not provided by the tools".
            8. You may use your general knowledge to provide additional learning recommendations, but clearly label them as "AI Recommendations".
            9. Do not modify or change any values returned by the tools.

            Previous Observation: {self.observation}
            Think Carefully. Decide what information you still need.
            Return Only One: 
                SKILL_TOOL
                PROJECT_TOOL
                CERTIFICATION_TOOL
                SALARY_TOOL
        """
        try:
            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt
            )
            plan = []
            for line in response.text.split("\n"):
                tool = line.strip()
                if tool in TOOL_REGISTRY:
                    plan.append(tool)
            return plan


        except Exception as e:
            print("Gemini API Error:", e)
            return "EXIT"

    # Gather Evidence
    def gathering_evidence(self):
        print("Gathering evidence...")
        step = 1
        for tool_name in self.plan:
            print(f"========== Step - {step} ==========")
            tool = TOOL_REGISTRY.get(tool_name)
            result = tool(self.role)
            print(f"========= {tool_name} =========")
            print(result)
            self.evidence.append(f"{tool_name} \n {result}")
            step += 1

    # Analyzing Evidence
    def analyze_evidence(self):
        print("Analyzing Evidence...")
        prompt = f"""
            You are an AI Career Analyst.
            Role: {self.role}
            Evidence: {self.evidence}
            Generate:
            1. Key Findings
            2. Opportunities
            3. Challanges

            Return analyis
        """
        response = client.models.generate_content(
                        model="gemini-3.1-flash-lite",
                        contents=prompt
                    )
        return response.text

    def generate_recommendation(self, analysis):
        print("Generating recommendation...")
        prompt = f"""
            User Role: {self.role}
            Analysis: {analysis}
            Generate: 
            1. Executive summary
            2. Recommendations
            3. Learning Path
            4. Final Verdict
        """
        response = client.models.generate_content(
                            model="gemini-3.1-flash-lite",
                            contents=prompt
                    )
        print("======Final Plan=====")
        print(response.text)


    # Run Agent
    def run(self):
        self.plan = self.create_research_plan()
        print("========== Research Plan ==========")

        for index,tool in enumerate(self.plan, start=1):
            print(f"{index}, {tool}")

        self.gathering_evidence()
        analysis = self.analyze_evidence()
        print("Analysis")
        print(analysis)

        self.generate_recommendation(analysis)


role = input("Enter your career goal: ")
agent = Research_Agent(role)
agent.run()