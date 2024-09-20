import asyncio
from typing import List, Dict
from .openai_api import OpenAIClient

class ClassifyListAgent:
    def __init__(self, list_to_classify: List[str], classification_criteria: str, max_tokens: int = 1000):
        self.list_to_classify = list_to_classify
        self.classification_criteria = classification_criteria
        self.max_tokens = max_tokens
        self.openai_client = OpenAIClient()

    async def classify_list(self) -> List[Dict]:
        tasks = []
        for item in self.list_to_classify:
            user_prompt = f"Classify the item '{item}' according to the following criteria: {self.classification_criteria}."
            tasks.append(self.classify_item(user_prompt))

        results = await asyncio.gather(*tasks)
        return results

    async def classify_item(self, user_prompt: str) -> Dict:
        system_prompt = f"You are an assistant tasked with classifying items based on the given criteria."
        response = await self.openai_client.complete_chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ], max_tokens=self.max_tokens)

        return {"item": user_prompt, "classification": response.strip()}
