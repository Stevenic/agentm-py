import asyncio
from typing import List, Dict
from .openai_api import OpenAIClient
from .logging import Logger  # Using correct logging abstraction

class BinaryClassifyListAgent:
    def __init__(self, list_to_classify: List[str], criteria: str, max_tokens: int = 1000, temperature: float = 0.0):
        self.list_to_classify = list_to_classify
        self.criteria = criteria
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.openai_client = OpenAIClient()
        self.logger = Logger()

    async def classify_list(self) -> List[Dict]:
        tasks = []
        for item in self.list_to_classify:
            user_prompt = f"Based on the following criteria '{self.criteria}', classify the item '{item}' as true or false."
            tasks.append(self.classify_item(user_prompt))

        results = await asyncio.gather(*tasks)
        return results

    async def classify_item(self, user_prompt: str) -> Dict:
        system_prompt = "You are an assistant tasked with binary classification of items."

        self.logger.info(f"Classifying item: {user_prompt}")  # Logging the classification request

        response = await self.openai_client.complete_chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ], max_tokens=self.max_tokens)

        self.logger.info(f"Received response for item: {user_prompt} -> {response.strip()}")  # Logging the response

        return {"item": user_prompt, "classification": response.strip()}
