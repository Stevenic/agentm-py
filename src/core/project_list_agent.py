import asyncio
from typing import List, Dict
from .openai_api import OpenAIClient

class ProjectListAgent:
    def __init__(self, list_to_project: List[str], projection_rule: str, max_tokens: int = 1000):
        self.list_to_project = list_to_project
        self.projection_rule = projection_rule
        self.max_tokens = max_tokens
        self.openai_client = OpenAIClient()

    async def project_list(self) -> List[Dict]:
        tasks = []
        for item in self.list_to_project:
            user_prompt = f"Project the following item based on the rule '{self.projection_rule}': {item}."
            tasks.append(self.project_item(user_prompt))

        results = await asyncio.gather(*tasks)
        return results

    async def project_item(self, user_prompt: str) -> Dict:
        system_prompt = "You are an assistant tasked with projecting items based on a specific rule."
        response = await self.openai_client.complete_chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ], max_tokens=self.max_tokens)

        return {"item": user_prompt, "projection": response.strip()}
