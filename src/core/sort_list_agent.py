import asyncio
from typing import List
from .openai_api import OpenAIClient

class SortListAgent:
    def __init__(self, goal: str, list_to_sort: List[str], max_tokens: int = 1000, temperature: float = 0.0, log_explanations: bool = False):
        self.goal = goal
        self.list = list_to_sort
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.log_explanations = log_explanations
        self.openai_client = OpenAIClient()

    async def sort(self):
        return await self.merge_sort(self.list)

    async def batch_compare(self, pairs):
        """
        Send multiple comparison pairs to the API in one request to reduce API calls.
        """
        batch_prompt = "\n".join([f"Compare {a} and {b} and return the items in the correct order as 'item1,item2'." for a, b in pairs])
        system_prompt = f"You are tasked with sorting items. Goal: {self.goal}.\nCompare the following pairs and return the correct order."

        # Log the request we're sending
        self.openai_client.logger.info(f"Sending batch comparison request with prompt: {batch_prompt}")
        
        response = await self.openai_client.complete_chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": batch_prompt}
        ], max_tokens=self.max_tokens)
        
        # Log the response we receive
        self.openai_client.logger.info(f"Received response: {response}")

        comparisons = response.split("\n")  # Assuming API returns comparisons in batch order
        
        # Check for empty response and log an error
        if not comparisons:
            self.openai_client.logger.error("Empty response received from API.")
        
        # Parse responses and filter out empty or malformed comparisons
        parsed_comparisons = []
        for comparison in comparisons:
            individual_comparisons = comparison.split(" ")  # Split individual results
            for comp in individual_comparisons:
                comp = comp.strip()
                if not comp:  # Ignore empty results
                    continue
                try:
                    first, second = comp.split(",")
                    if first.strip() == pairs[0][0]:
                        parsed_comparisons.append("BEFORE")
                    else:
                        parsed_comparisons.append("AFTER")
                except ValueError:
                    self.openai_client.logger.info(f"Ignoring unexpected comparison result: {comp}")
        
        return parsed_comparisons

    async def merge_sort(self, items):
        if len(items) < 2:
            return items

        mid = len(items) // 2
        left_half, right_half = await asyncio.gather(self.merge_sort(items[:mid]), self.merge_sort(items[mid:]))
        return await self.merge(left_half, right_half)

    async def merge(self, left, right):
        result = []
        i, j = 0, 0
        comparisons_to_make = []

        while i < len(left) and j < len(right):
            comparisons_to_make.append((left[i], right[j]))
            i += 1
            j += 1

        # Batch process comparisons
        comparison_results = await self.batch_compare(comparisons_to_make)

        # Safely ignore last comparison if there are no more results
        if not comparison_results:
            self.openai_client.logger.info("Final comparison complete.")
            result.extend(left[i:])
            result.extend(right[j:])
            return result

        i = 0
        j = 0
        while i < len(left) and j < len(right) and comparison_results:
            if comparison_results.pop(0) == "BEFORE":
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result
