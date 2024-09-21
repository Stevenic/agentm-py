import asyncio  # <-- Import asyncio here
from pydantic import BaseModel, Field
from typing import List, Dict
from .openai_api import OpenAIClient

class SummarizeListInput(BaseModel):
    list_to_summarize: List[str] = Field(..., description="The list of items to summarize")
    max_tokens: int = Field(1000, description="The maximum number of tokens to generate")

class SummarizeListAgent:
    """
    A class to summarize items in a list using the OpenAI API.

    Attributes:
        list_to_summarize (List[str]): The list of items to summarize.
        max_tokens (int): The maximum number of tokens to generate.
        openai_client (OpenAIClient): An instance of OpenAIClient to interact with the API.

    Methods:
        summarize_list(): Summarizes the entire list of items.
        summarize_item(): Summarizes a single item.
    """

    def __init__(self, data: SummarizeListInput):
        """
        Constructs all the necessary attributes for the SummarizeListAgent object.

        Args:
            data (SummarizeListInput): An instance of SummarizeListInput containing 
            the list of items and max_tokens.
        """
        self.list_to_summarize = data.list_to_summarize
        self.max_tokens = data.max_tokens
        self.openai_client = OpenAIClient()

    async def summarize_list(self) -> List[Dict]:
        """
        Summarizes the entire list based on the provided items.

        Returns:
            List[Dict]: A list of dictionaries with the original items and their summaries.
        """
        tasks = []
        for item in self.list_to_summarize:
            user_prompt = f"Summarize the following: {item}."
            tasks.append(self.summarize_item(user_prompt))

        results = await asyncio.gather(*tasks)
        return results

    async def summarize_item(self, user_prompt: str) -> Dict:
        """
        Summarizes a single item.

        Args:
            user_prompt (str): The prompt to send to the OpenAI API.

        Returns:
            Dict: A dictionary with the original item and its summary.
        """
        system_prompt = "You are an assistant tasked with summarizing items."
        response = await self.openai_client.complete_chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ], max_tokens=self.max_tokens)

        return {"item": user_prompt, "summary": response.strip()}
