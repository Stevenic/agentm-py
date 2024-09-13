import asyncio
from typing import List
from .openai_api import OpenAIClient

class ChainOfThoughtAgent:
    def __init__(self, question: str, max_tokens: int = 1000, temperature: float = 0.0):
        self.question = question
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.openai_client = OpenAIClient()

    async def chain_of_thought(self) -> str:
        system_prompt = "You are an assistant tasked with solving problems using the 'chain of thought' reasoning process."
        user_prompt = f"Solve the following problem step-by-step: {self.question}"

        response = await self.openai_client.complete_chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ], max_tokens=self.max_tokens)

        return response.strip()
