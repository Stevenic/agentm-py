import asyncio
from typing import Dict
from .openai_api import OpenAIClient

class GenerateObjectAgent:
    def __init__(self, object_description: str, goal: str, max_tokens: int = 1000):
        self.object_description = object_description
        self.goal = goal
        self.max_tokens = max_tokens
        self.openai_client = OpenAIClient()

    async def generate_object(self) -> Dict:
        system_prompt = f"You are an assistant tasked with generating objects based on a given description. The goal is: {self.goal}."
        user_prompt = f"Generate an object based on the following description: {self.object_description}."

        response = await self.openai_client.complete_chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ], max_tokens=self.max_tokens)

        return {"object_description": self.object_description, "generated_object": response.strip()}
