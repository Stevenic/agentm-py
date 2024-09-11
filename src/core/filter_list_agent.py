import asyncio
import json
import jsonschema
from typing import List, Dict
from .openai_api import OpenAIClient

class FilterListAgent:
    def __init__(self, goal: str, items_to_filter: List[str], max_tokens: int = 500, temperature: float = 0.0):
        self.goal = goal
        self.items = items_to_filter
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.openai_client = OpenAIClient()

    # JSON schema for validation
    schema = {
        "type": "object",
        "properties": {
            "explanation": {"type": "string"},
            "remove_item": {"type": "boolean"}
        },
        "required": ["explanation", "remove_item"]
    }

    async def filter(self) -> List[Dict]:
        return await self.filter_list(self.items)

    async def filter_list(self, items: List[str]) -> List[Dict]:
        # System prompt with multi-shot examples to guide the model
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

        # Run all tasks in parallel
        results = await asyncio.gather(*tasks)

        # Show the final list of items that were kept
        filtered_items = [self.items[i] for i, result in enumerate(results) if not result.get('remove_item', False)]
        print("\nFinal Filtered List:", filtered_items)

        return results

    async def filter_item(self, system_prompt: str, user_prompt: str) -> Dict:
        response = await self.openai_client.complete_chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ], max_tokens=self.max_tokens)

        return await self.process_response(response, system_prompt, user_prompt)

    async def process_response(self, response: str, system_prompt: str, user_prompt: str, retry: bool = True) -> Dict:
        try:
            # Parse the response as JSON
            result = json.loads(response)
            # Validate against the schema
            jsonschema.validate(instance=result, schema=self.schema)
            return result
        except (json.JSONDecodeError, jsonschema.ValidationError) as e:
            if retry:
                # Retry once if validation fails
                return await self.filter_item(system_prompt, user_prompt)
            else:
                return {"error": f"Failed to parse response after retry: {str(e)}", "response": response, "item": user_prompt}
