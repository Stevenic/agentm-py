from pydantic import BaseModel, Field
import asyncio
from typing import List
from .openai_api import OpenAIClient

class MapListInput(BaseModel):
    list_to_map: List[str] = Field(..., description="The list of items to transform")
    transformation: str = Field(..., description="The transformation rule to apply to each item")
    max_tokens: int = Field(1000, description="The maximum number of tokens to generate")

class MapListAgent:
    """
    A class to apply a transformation to each item in a list using the OpenAI API.

    Attributes:
        list_to_map (List[str]): The list of items to transform.
        transformation (str): The transformation rule to apply.
        max_tokens (int): The maximum number of tokens to generate.
        openai_client (OpenAIClient): An instance of OpenAIClient to interact with the API.

    Methods:
        map_list(): Transforms the entire list based on the transformation rule.
        apply_transformation(user_prompt): Applies the transformation to a single item.
    """

    def __init__(self, data: MapListInput):
        """
        Constructs all the necessary attributes for the MapListAgent object.

        Args:
            data (MapListInput): An instance of MapListInput containing 
            the list of items, transformation rule, and max_tokens.
        """
        self.list_to_map = data.list_to_map
        self.transformation = data.transformation
        self.max_tokens = data.max_tokens
        self.openai_client = OpenAIClient()

    async def map_list(self) -> List[str]:
        """
        Transforms the entire list based on the provided items and transformation rule.

        Returns:
            List[str]: A list of transformed items.
        """
        tasks = []
        for index, item in enumerate(self.list_to_map):
            user_prompt = f"Transform '{item}' as per the following rule: {self.transformation}."
            tasks.append(self.apply_transformation(user_prompt))

        results = await asyncio.gather(*tasks)
        return results

    async def apply_transformation(self, user_prompt: str) -> str:
        """
        Applies the transformation to a single item.

        Args:
            user_prompt (str): The prompt describing the transformation rule and item.

        Returns:
            str: The transformed item.
        """
        system_prompt = "You are an assistant tasked with transforming list items according to a rule."
        response = await self.openai_client.complete_chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ], max_tokens=self.max_tokens)

        return response.strip()
