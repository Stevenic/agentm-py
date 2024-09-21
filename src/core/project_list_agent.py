import asyncio  # <-- Import asyncio here
from pydantic import BaseModel, Field
from typing import List, Dict
from .openai_api import OpenAIClient

class ProjectListInput(BaseModel):
    list_to_project: List[str] = Field(..., description="The list of items to project")
    projection_rule: str = Field(..., description="The rule to apply for projection")
    max_tokens: int = Field(1000, description="The maximum number of tokens to generate")

class ProjectListAgent:
    """
    A class to project items in a list based on a given rule using the OpenAI API.

    Attributes:
        list_to_project (List[str]): The list of items to project.
        projection_rule (str): The rule to apply for projection.
        max_tokens (int): The maximum number of tokens to generate.
        openai_client (OpenAIClient): An instance of OpenAIClient to interact with the API.

    Methods:
        project_list(): Projects the entire list based on the projection rule.
        project_item(): Projects a single item based on the projection rule.
    """

    def __init__(self, data: ProjectListInput):
        """
        Constructs all the necessary attributes for the ProjectListAgent object.

        Args:
            data (ProjectListInput): An instance of ProjectListInput containing 
            the list of items, projection rule, and max_tokens.
        """
        self.list_to_project = data.list_to_project
        self.projection_rule = data.projection_rule
        self.max_tokens = data.max_tokens
        self.openai_client = OpenAIClient()

    async def project_list(self) -> List[Dict]:
        """
        Projects the entire list based on the given projection rule.

        Returns:
            List[Dict]: A list of dictionaries with the original items and their projections.
        """
        tasks = []
        for item in self.list_to_project:
            user_prompt = f"Project the following item based on the rule '{self.projection_rule}': {item}."
            tasks.append(self.project_item(user_prompt))

        results = await asyncio.gather(*tasks)
        return results

    async def project_item(self, user_prompt: str) -> Dict:
        """
        Projects a single item based on the given rule.

        Args:
            user_prompt (str): The prompt to send to the OpenAI API.

        Returns:
            Dict: A dictionary with the original item and its projection.
        """
        system_prompt = "You are an assistant tasked with projecting items based on a specific rule."
        response = await self.openai_client.complete_chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ], max_tokens=self.max_tokens)

        return {"item": user_prompt, "projection": response.strip()}
