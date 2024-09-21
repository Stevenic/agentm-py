from pydantic import BaseModel, Field
import asyncio
from typing import List, Dict
from .openai_api import OpenAIClient

class ClassifyListInput(BaseModel):
    list_to_classify: List[str] = Field(..., description="The list of items to classify")
    classification_criteria: str = Field(..., description="The criteria for classifying the items")
    max_tokens: int = Field(1000, description="The maximum number of tokens to generate")

class ClassifyListAgent:
    """
    A class to classify items in a list based on given criteria using the OpenAI API.

    Attributes:
        list_to_classify (List[str]): The list of items to classify.
        classification_criteria (str): The criteria for classifying the items.
        max_tokens (int): The maximum number of tokens to generate.
        openai_client (OpenAIClient): An instance of OpenAIClient to interact with the API.

    Methods:
        classify_list(): Classifies the entire list of items.
        classify_item(user_prompt): Classifies a single item based on the classification criteria.
    """

    def __init__(self, data: ClassifyListInput):
        """
        Constructs all the necessary attributes for the ClassifyListAgent object.

        Args:
            data (ClassifyListInput): An instance of ClassifyListInput containing 
            the list of items, classification criteria, and max_tokens.
        """
        self.list_to_classify = data.list_to_classify
        self.classification_criteria = data.classification_criteria
        self.max_tokens = data.max_tokens
        self.openai_client = OpenAIClient()

    async def classify_list(self) -> List[Dict]:
        """
        Classifies the entire list based on the provided items and classification criteria.

        Returns:
            List[Dict]: A list of dictionaries with the classification results.
        """
        tasks = []
        for item in self.list_to_classify:
            user_prompt = f"Classify the item '{item}' according to the following criteria: {self.classification_criteria}."
            tasks.append(self.classify_item(user_prompt))

        results = await asyncio.gather(*tasks)
        return results

    async def classify_item(self, user_prompt: str) -> Dict:
        """
        Classifies a single item based on the classification criteria.

        Args:
            user_prompt (str): The prompt describing the item and classification criteria.

        Returns:
            Dict: A dictionary with the classification result.
        """
        system_prompt = "You are an assistant tasked with classifying items based on the given criteria."
        response = await self.openai_client.complete_chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ], max_tokens=self.max_tokens)

        return {"item": user_prompt, "classification": response.strip()}
