from pydantic import BaseModel, Field
from typing import List
from .openai_api import OpenAIClient

class ChainOfThoughtInput(BaseModel):
    question: str = Field(..., description="The question to solve using chain of thought reasoning")
    max_tokens: int = Field(1000, description="The maximum number of tokens to generate")
    temperature: float = Field(0.0, description="Sampling temperature for the OpenAI model")

class ChainOfThoughtAgent:
    """
    A class to solve problems using the 'chain of thought' reasoning process via the OpenAI API.

    Attributes:
        question (str): The question to solve.
        max_tokens (int): The maximum number of tokens to generate.
        temperature (float): Sampling temperature for the OpenAI model.
        openai_client (OpenAIClient): An instance of OpenAIClient to interact with the API.

    Methods:
        chain_of_thought(): Solves the question using chain of thought reasoning.
    """

    def __init__(self, data: ChainOfThoughtInput):
        """
        Constructs all the necessary attributes for the ChainOfThoughtAgent object.

        Args:
            data (ChainOfThoughtInput): An instance of ChainOfThoughtInput containing 
            the question, max_tokens, and temperature.
        """
        self.question = data.question
        self.max_tokens = data.max_tokens
        self.temperature = data.temperature
        self.openai_client = OpenAIClient()

    async def chain_of_thought(self) -> str:
        """
        Solves the question using chain of thought reasoning.

        Returns:
            str: The step-by-step reasoning process and solution.
        """
        system_prompt = "You are an assistant tasked with solving problems using the 'chain of thought' reasoning process."
        user_prompt = f"Solve the following problem step-by-step: {self.question}"

        response = await self.openai_client.complete_chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ], max_tokens=self.max_tokens)

        return response.strip()
