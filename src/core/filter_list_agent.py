from pydantic import BaseModel, Field
from functools import partial
from .concurrency import map_concurrent
import json
import jsonschema
from typing import List, Dict
from .openai_api import ClientOwner

class FilterListInput(BaseModel):
    goal: str = Field(..., description="The goal for filtering the list")
    items_to_filter: List[str] = Field(..., description="The list of items to filter")
    max_tokens: int = Field(500, description="The maximum number of tokens to generate")
    temperature: float = Field(0.0, description="Sampling temperature for the OpenAI model")

class FilterListAgent(ClientOwner):
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
        "required": ["explanation", "remove_item"],
        "additionalProperties": False
    }

    _validator = jsonschema.Draft202012Validator(schema)

    def __init__(self, data: FilterListInput, *, openai_client=None):
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
        super().__init__(openai_client)

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
            f"Filter items according to this goal: {self.goal}. "
            "Return JSON with a brief explanation and remove_item (boolean)."
        )

        tasks = []
        for index, item in enumerate(items):
            user_prompt = f"Item {index+1}: {item}. Should it be removed? Answer with explanation and 'remove_item': true/false."
            tasks.append(user_prompt)

        results = await map_concurrent(partial(self.filter_item, system_prompt), tasks, self.openai_client.max_concurrency)

        if any('error' in result for result in results):
            raise ValueError('Filtering failed: invalid model response')

        filtered_items = [items[i] for i, result in enumerate(results) if not result.get('remove_item', False)]
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
        ], max_tokens=self.max_tokens, temperature=self.temperature,
            response_format={"type": "json_schema", "json_schema": {
                "name": "filter_result", "strict": True, "schema": self.schema,
            }})

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
            self._validator.validate(result)
            return result
        except (json.JSONDecodeError, jsonschema.ValidationError) as e:
            if retry:
                response = await self.openai_client.complete_chat([
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ], max_tokens=self.max_tokens, temperature=self.temperature,
                    response_format={"type": "json_schema", "json_schema": {
                        "name": "filter_result", "strict": True, "schema": self.schema,
                    }})
                return await self.process_response(response, system_prompt, user_prompt, retry=False)
            else:
                return {"error": f"Failed to parse response after retry: {str(e)}", "response": response, "item": user_prompt}
