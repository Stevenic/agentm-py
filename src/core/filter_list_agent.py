from pydantic import BaseModel, Field
import asyncio
import json
import jsonschema
from typing import List, Dict
from .openai_api import OpenAIClient

class FilterListInput(BaseModel):
    goal: str = Field(..., description="The goal for filtering the list")
    items_to_filter: List[str] = Field(..., description="The list of items to filter")
    max_tokens: int = Field(500, description="The maximum number of tokens to generate")
    temperature: float = Field(0.0, description="Sampling temperature for the OpenAI model")

class FilterListAgent:
    """
    A class to filter items in a list based on a given goal using the OpenAI API.

    Attributes:
        goal (str): The goal for filtering the list.
        items (List[str]): The list of items to filter.
        max_tokens (int): The maximum number of tokens to generate.
        temperature (float): Sampling temperature for the OpenAI model.
        openai_client (OpenAIClient): An instance of OpenAIClient to interact with the API.
        schema (dict): JSON schema to validate the API's response format.

    Methods:
        filter(): Filters the entire list of items.
        filter_list(items): Filters a given list of items.
        filter_item(system_prompt, user_prompt): Filters a single item.
        process_response(response, system_prompt, user_prompt, retry): Processes and validates the API response.
    """

    schema = {
        "type": "object",
        "properties": {
            "explanation": {"type": "string"},
            "remove_item": {"type": "boolean"}
        },
        "required": ["explanation", "remove_item"]
    }

    def __init__(self, data: FilterListInput):
        """
        Constructs all the necessary attributes for the FilterListAgent object.

        Args:
            data (FilterListInput): An instance of FilterListInput containing 
            the goal, items to filter, max_tokens, and temperature.
        """
        self.goal = data.goal
        self.items = data.items_to_filter
        self.max_tokens = data.max_tokens
        self.temperature = data.temperature
        self.openai_client = OpenAIClient()

    async def filter(self) -> List[Dict]:
        """
        Filters the entire list based on the provided items and goal.

        Returns:
            List[Dict]: A list of dictionaries with the filtering results.
        """
        return await self.filter_list(self.items)

    async def filter_list(self, items: List[str]) -> List[Dict]:
        """
        Filters a given list of items based on the goal.

        Args:
            items (List[str]): The list of items to filter.

        Returns:
            List[Dict]: A list of dictionaries with the filtering results.
        """
        system_prompt = (
            "You are an assistant tasked with filtering a list of items. The goal is: "
            f"{self.goal}. For each item, decide if it should be removed based on whether it is a healthy snack.\n"
            "Respond in the following structured format:\n\n"
            "Example:\n"
            "{\"explanation\": \"The apple is a healthy snack option, as it is low in calories...\",\n"
            " \"remove_item\": false}\n\n"
            "Example:\n"
            "{\"explanation\": \"A chocolate bar is generally considered an unhealthy snack...\",\n"
            " \"remove_item\": true}\n\n"
        )

        tasks = []
        for index, item in enumerate(items):
            user_prompt = f"Item {index+1}: {item}. Should it be removed? Answer with explanation and 'remove_item': true/false."
            tasks.append(self.filter_item(system_prompt, user_prompt))

        results = await asyncio.gather(*tasks)

        filtered_items = [self.items[i] for i, result in enumerate(results) if not result.get('remove_item', False)]
        print("\nFinal Filtered List:", filtered_items)

        return results

    async def filter_item(self, system_prompt: str, user_prompt: str) -> Dict:
        """
        Filters a single item based on the goal.

        Args:
            system_prompt (str): The system prompt to guide the API.
            user_prompt (str): The user prompt to describe the item to be filtered.

        Returns:
            Dict: A dictionary with the filtering result.
        """
        response = await self.openai_client.complete_chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ], max_tokens=self.max_tokens)

        return await self.process_response(response, system_prompt, user_prompt)

    async def process_response(self, response: str, system_prompt: str, user_prompt: str, retry: bool = True) -> Dict:
        """
        Processes and validates the API response.

        Args:
            response (str): The API's response to process.
            system_prompt (str): The system prompt used for the API request.
            user_prompt (str): The user prompt used for the API request.
            retry (bool): Whether to retry the request if validation fails.

        Returns:
            Dict: A dictionary containing the validated response or an error.
        """
        try:
            result = json.loads(response)
            jsonschema.validate(instance=result, schema=self.schema)
            return result
        except (json.JSONDecodeError, jsonschema.ValidationError) as e:
            if retry:
                return await self.filter_item(system_prompt, user_prompt)
            else:
                return {"error": f"Failed to parse response after retry: {str(e)}", "response": response, "item": user_prompt}
