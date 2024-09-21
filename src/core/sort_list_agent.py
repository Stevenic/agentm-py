from pydantic import BaseModel, Field
import asyncio
from typing import List
from .openai_api import OpenAIClient

class SortListInput(BaseModel):
    goal: str = Field(..., description="The goal for sorting the list")
    list_to_sort: List[str] = Field(..., description="The list of items to sort")
    max_tokens: int = Field(1000, description="The maximum number of tokens to generate")
    temperature: float = Field(0.0, description="Sampling temperature for the OpenAI model")
    log_explanations: bool = Field(False, description="Whether to log explanations of sorting decisions")

class SortListAgent:
    """
    A class to sort items in a list based on a given goal using the OpenAI API.

    Attributes:
        goal (str): The goal for sorting the list.
        list (List[str]): The list of items to sort.
        max_tokens (int): The maximum number of tokens to generate.
        temperature (float): Sampling temperature for the OpenAI model.
        log_explanations (bool): Whether to log explanations of sorting decisions.
        openai_client (OpenAIClient): An instance of OpenAIClient to interact with the API.

    Methods:
        sort(): Sorts the entire list of items.
        batch_compare(pairs): Sends multiple comparison pairs to the API in one request to reduce API calls.
        merge_sort(items): Recursively sorts the items using merge sort.
        merge(left, right): Merges two sorted lists into one.
    """

    def __init__(self, data: SortListInput):
        """
        Constructs all the necessary attributes for the SortListAgent object.

        Args:
            data (SortListInput): An instance of SortListInput containing 
            the goal, list of items, max_tokens, temperature, and log_explanations.
        """
        self.goal = data.goal
        self.list = data.list_to_sort
        self.max_tokens = data.max_tokens
        self.temperature = data.temperature
        self.log_explanations = data.log_explanations
        self.openai_client = OpenAIClient()

    async def sort(self):
        """
        Sorts the entire list based on the provided items and goal.

        Returns:
            List[str]: The sorted list of items.
        """
        return await self.merge_sort(self.list)

    async def batch_compare(self, pairs):
        """
        Sends multiple comparison pairs to the API in one request to reduce API calls.

        Args:
            pairs (List[Tuple[str, str]]): A list of pairs of items to compare.

        Returns:
            List[str]: A list of results for each comparison.
        """
        batch_prompt = "\n".join([f"Compare {a} and {b} and return the items in the correct order as 'item1,item2'." for a, b in pairs])
        system_prompt = f"You are tasked with sorting items. Goal: {self.goal}.\nCompare the following pairs and return the correct order."

        if self.log_explanations:
            self.openai_client.logger.info(f"Sending batch comparison request with prompt: {batch_prompt}")

        response = await self.openai_client.complete_chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": batch_prompt}
        ], max_tokens=self.max_tokens)

        if self.log_explanations:
            self.openai_client.logger.info(f"Received response: {response}")

        comparisons = response.split("\n")

        if not comparisons:
            self.openai_client.logger.error("Empty response received from API.")

        parsed_comparisons = []
        for comparison in comparisons:
            individual_comparisons = comparison.split(" ")
            for comp in individual_comparisons:
                comp = comp.strip()
                if not comp:
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
        """
        Recursively sorts the items using merge sort.

        Args:
            items (List[str]): The list of items to sort.

        Returns:
            List[str]: The sorted list of items.
        """
        if len(items) < 2:
            return items

        mid = len(items) // 2
        left_half, right_half = await asyncio.gather(self.merge_sort(items[:mid]), self.merge_sort(items[mid:]))
        return await self.merge(left_half, right_half)

    async def merge(self, left, right):
        """
        Merges two sorted lists into one.

        Args:
            left (List[str]): The left half of the list.
            right (List[str]): The right half of the list.

        Returns:
            List[str]: The merged and sorted list of items.
        """
        result = []
        i, j = 0, 0
        comparisons_to_make = []

        while i < len(left) and j < len(right):
            comparisons_to_make.append((left[i], right[j]))
            i += 1
            j += 1

        comparison_results = await self.batch_compare(comparisons_to_make)

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
