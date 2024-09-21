from pydantic import BaseModel, Field
import asyncio
from typing import List, Dict
from .openai_api import OpenAIClient

class ReduceListInput(BaseModel):
    list_to_reduce: List[str] = Field(..., description="The list of items to reduce")
    reduction_goal: str = Field(..., description="The goal for reducing the items")
    max_tokens: int = Field(1000, description="The maximum number of tokens to generate")

class ReduceListAgent:
    """
    A class to reduce items in a list based on a given goal using the OpenAI API.

    Attributes:
        list_to_reduce (List[str]): The list of items to reduce.
        reduction_goal (str): The goal for reducing the items.
        max_tokens (int): The maximum number of tokens to generate.
        openai_client (OpenAIClient): An instance of OpenAIClient to interact with the API.

    Methods:
        reduce_list(): Reduces the entire list of items.
        reduce_item(user_prompt): Reduces a single item based on the reduction goal.
    """

    def __init__(self, data: ReduceListInput):
        """
        Constructs all the necessary attributes for the ReduceListAgent object.

        Args:
            data (ReduceListInput): An instance of ReduceListInput containing 
            the list of items, reduction goal, and max_tokens.
        """
        self.list_to_reduce = data.list_to_reduce
        self.reduction_goal = data.reduction_goal
        self.max_tokens = data.max_tokens
        self.openai_client = OpenAIClient()

    async def reduce_list(self) -> List[Dict]:
        """
        Reduces the entire list based on the provided items and reduction goal.

        Returns:
            List[Dict]: A list of dictionaries with the reduction results.
        """
        tasks = []
        for item in self.list_to_reduce:
            user_prompt = f"Reduce the item '{item}' to achieve the goal: {self.reduction_goal}."
            tasks.append(self.reduce_item(user_prompt))

        results = await asyncio.gather(*tasks)
        return results

    async def reduce_item(self, user_prompt: str) -> Dict:
        """
        Reduces a single item based on the reduction goal.

        Args:
            user_prompt (str): The prompt describing the item and reduction goal.

        Returns:
            Dict: A dictionary with the reduced item.
        """
        system_prompt = "You are an assistant tasked with reducing items to achieve a specific goal."
        response = await self.openai_client.complete_chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ], max_tokens=self.max_tokens)

        return {"item": user_prompt, "reduced_item": response.strip()}
