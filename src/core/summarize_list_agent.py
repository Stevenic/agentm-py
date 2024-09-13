import asyncio
from typing import List, Dict
from .openai_api import OpenAIClient

class SummarizeListAgent:
    def __init__(self, list_to_summarize: List[str], max_tokens: int = 1000):
        self.list_to_summarize = list_to_summarize
        self.max_tokens = max_tokens
        self.openai_client = OpenAIClient()

    async def summarize_list(self) -> List[Dict]:
        tasks = []
        for item in self.list_to_summarize:
            user_prompt = f"Summarize the following: {item}."
            tasks.append(self.summarize_item(user_prompt))

        results = await asyncio.gather(*tasks)
        return results

    async def summarize_item(self, user_prompt: str) -> Dict:
        system_prompt = "You are an assistant tasked with summarizing items."
        response = await self.openai_client.complete_chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ], max_tokens=self.max_tokens)

        return {"item": user_prompt, "summary": response.strip()}
