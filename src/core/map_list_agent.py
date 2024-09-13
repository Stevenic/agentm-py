import asyncio
from typing import List
from .openai_api import OpenAIClient

class MapListAgent:
    def __init__(self, list_to_map: List[str], transformation: str, max_tokens: int = 1000):
        self.list_to_map = list_to_map
        self.transformation = transformation
        self.max_tokens = max_tokens
        self.openai_client = OpenAIClient()

    async def map_list(self) -> List[str]:
        tasks = []
        for index, item in enumerate(self.list_to_map):
            user_prompt = f"Transform '{item}' as per the following rule: {self.transformation}."
            tasks.append(self.apply_transformation(user_prompt))

        # Run all tasks in parallel
        results = await asyncio.gather(*tasks)
        return results

    async def apply_transformation(self, user_prompt: str) -> str:
        system_prompt = f"You are an assistant tasked with transforming list items according to a rule."
        response = await self.openai_client.complete_chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ], max_tokens=self.max_tokens)

        return response.strip()
