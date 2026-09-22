from pydantic import BaseModel, Field
from typing import Dict, Optional
from .openai_api import ClientOwner

class ObjectGenerationInput(BaseModel):
    object_description: str = Field(..., description="A description of the object to generate")
    goal: str = Field(..., description="The goal of the generation process")
    output_schema: Optional[Dict] = Field(None, description="Optional strict JSON output schema")
    max_tokens: int = Field(1000, description="The maximum number of tokens to generate")

class GenerateObjectAgent(ClientOwner):
    """
    A class to generate objects based on a given description and goal using the OpenAI API.

    Attributes:
        object_description (str): A description of the object to generate.
        goal (str): The goal of the generation process.
        max_tokens (int): The maximum number of tokens to generate.
        openai_client (OpenAIClient): An instance of OpenAIClient to interact with the API.

    Methods:
        generate_object(): Generates an object based on the description and goal.
    """

    def __init__(self, data: ObjectGenerationInput, *, openai_client=None):
        """
        Constructs all the necessary attributes for the GenerateObjectAgent object.

        Args:
            data (ObjectGenerationInput): An instance of ObjectGenerationInput containing 
            the object description, goal, and max_tokens.
        """
        self.object_description = data.object_description
        self.goal = data.goal
        self.max_tokens = data.max_tokens
        self.output_schema = data.output_schema
        super().__init__(openai_client)

    async def generate_object(self) -> Dict:
        """
        Generates an object based on the given description and goal.

        Returns:
            dict: A dictionary containing the original object description and the generated object.
        """
        system_prompt = f"You are an assistant tasked with generating objects based on a given description. The goal is: {self.goal}."
        user_prompt = f"Generate an object based on the following description: {self.object_description}."

        if self.output_schema is not None:
            result = await self.openai_client.complete_object([
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ], self.output_schema, max_tokens=self.max_tokens)
            return {"object_description": self.object_description, "generated_object": result}

        response = await self.openai_client.complete_chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ], max_tokens=self.max_tokens)

        return {"object_description": self.object_description, "generated_object": response.strip()}
