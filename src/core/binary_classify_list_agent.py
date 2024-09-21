from pydantic import BaseModel, Field
import asyncio
from typing import List, Dict
from .openai_api import OpenAIClient
from .logging import Logger  # Using correct logging abstraction

class BinaryClassifyListInput(BaseModel):
    list_to_classify: List[str] = Field(..., description="The list of items to classify")
    criteria: str = Field(..., description="The criteria for binary classification")
    max_tokens: int = Field(1000, description="The maximum number of tokens to generate")
    temperature: float = Field(0.0, description="Sampling temperature for the OpenAI model")

class BinaryClassifyListAgent:
    """
    A class to classify items in a list based on binary criteria using the OpenAI API.

    Attributes:
        list_to_classify (List[str]): The list of items to classify.
        criteria (str): The criteria for binary classification.
        max_tokens (int): The maximum number of tokens to generate.
        temperature (float): Sampling temperature for the OpenAI model.
        openai_client (OpenAIClient): An instance of OpenAIClient to interact with the API.
        logger (Logger): An instance of Logger to log classification requests and responses.

    Methods:
        classify_list(): Classifies the entire list of items.
        classify_item(user_prompt): Classifies a single item based on the criteria.
    """

    def __init__(self, data: BinaryClassifyListInput):
        """
        Constructs all the necessary attributes for the BinaryClassifyListAgent object.

        Args:
            data (BinaryClassifyListInput): An instance of BinaryClassifyListInput containing 
            the list of items, criteria, max_tokens, and temperature.
        """
        self.list_to_classify = data.list_to_classify
        self.criteria = data.criteria
        self.max_tokens = data.max_tokens
        self.temperature = data.temperature
        self.openai_client = OpenAIClient()
        self.logger = Logger()

    async def classify_list(self) -> List[Dict]:
        """
        Classifies the entire list based on the provided items and criteria.

        Returns:
            List[Dict]: A list of dictionaries with the classification results.
        """
        tasks = []
        for item in self.list_to_classify:
            user_prompt = f"Based on the following criteria '{self.criteria}', classify the item '{item}' as true or false."
            tasks.append(self.classify_item(user_prompt))

        results = await asyncio.gather(*tasks)
        return results

    async def classify_item(self, user_prompt: str) -> Dict:
        """
        Classifies a single item based on the criteria.

        Args:
            user_prompt (str): The prompt describing the classification criteria and item.

        Returns:
            Dict: A dictionary with the classification result.
        """
        system_prompt = "You are an assistant tasked with binary classification of items."

        self.logger.info(f"Classifying item: {user_prompt}")  # Logging the classification request

        response = await self.openai_client.complete_chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ], max_tokens=self.max_tokens)

        self.logger.info(f"Received response for item: {user_prompt} -> {response.strip()}")  # Logging the response

        return {"item": user_prompt, "classification": response.strip()}
