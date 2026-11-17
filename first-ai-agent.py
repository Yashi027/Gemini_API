from google import genai
from dotenv import load_dotenv
import os
import time

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

class RoadMapAgent:
    def __init__(self,goal):
        self.goal=goal

    def reason(self):
        print("Agent understanding the goal...")
        prompt = f"""
                    User Goal: {self.goal}
                    Identify all required skills.
                    Return only the skills.
                """
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt
        )
        return response.text

    def planning(self, skills):
            print("Agent creating plan...")
            prompt = f"""
                        User Goal: {self.goal}
                        Skills: {skills}
Arrange these skills in the best learning order
                    """
            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt
            )
            return response.text

    def execute(self, plan):
            print("Agent executing the plan...")
            prompt = f"""
                        User Goal: {self.goal}
                        Learning Plan: {plan}
                        Create a detailed roadmap.
                    """
            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt
            )
            return response.text

    def run(self):
          skills = self.reason()
          time.sleep(1)

          plan = self.planning(skills)
          time.sleep(1)

          roadmap = self.execute(plan)

          print("Final roadmap \n")
          print(roadmap)

print("Welcome to roadmap agent \n")
goal = input("Enter your goal: ")
agent = RoadMapAgent(goal)
agent.run()