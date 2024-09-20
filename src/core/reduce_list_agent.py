import asyncio
from typing import List, Dict
from .openai_api import OpenAIClient

class ReduceListAgent:
    def __init__(self, list_to_reduce: List[str], reduction_goal: str, max_tokens: int = 1000):
        self.list_to_reduce = list_to_reduce
        self.reduction_goal = reduction_goal
        self.max_tokens = max_tokens
        self.openai_client = OpenAIClient()

    async def reduce_list(self) -> List[Dict]:
        tasks = []
        for item in self.list_to_reduce:
            user_prompt = f"Reduce the item '{item}' to achieve the goal: {self.reduction_goal}."
            tasks.append(self.reduce_item(user_prompt))

        results = await asyncio.gather(*tasks)
        return results

    async def reduce_item(self, user_prompt: str) -> Dict:
        system_prompt = "You are an assistant tasked with reducing items to achieve a specific goal."
        response = await self.openai_client.complete_chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ], max_tokens=self.max_tokens)

        return {"item": user_prompt, "reduced_item": response.strip()}
