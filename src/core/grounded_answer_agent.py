from pydantic import BaseModel, Field
import asyncio
import json
import jsonschema
from typing import Dict
from .openai_api import OpenAIClient

class GroundedAnswerInput(BaseModel):
    question: str = Field(..., description="The question to answer based on the provided context")
    context: str = Field(..., description="The context information to base the answer on")
    instructions: str = Field('', description="Additional instructions for answering the question")
    max_tokens: int = Field(1000, description="The maximum number of tokens to generate")

class GroundedAnswerAgent:
    """
    A class to provide grounded answers based on a given context using the OpenAI API.

    Attributes:
        question (str): The question to answer based on the provided context.
        context (str): The context information to base the answer on.
        instructions (str): Additional instructions for answering the question.
        max_tokens (int): The maximum number of tokens to generate.
        openai_client (OpenAIClient): An instance of OpenAIClient to interact with the API.
        schema (dict): JSON schema to validate the API's response format.

    Methods:
        answer(): Provides a grounded answer based on the context.
        grounded_answer(): Generates the grounded answer using the API.
        process_response(response): Processes and validates the API response.
    """

    # JSON schema for validation
    schema = {
        "type": "object",
        "properties": {
            "explanation": {"type": "string"},
            "answer": {"type": "string"}
        },
        "required": ["explanation", "answer"],
        "additionalProperties": False
    }

    def __init__(self, data: GroundedAnswerInput):
        """
        Constructs all the necessary attributes for the GroundedAnswerAgent object.

        Args:
            data (GroundedAnswerInput): An instance of GroundedAnswerInput containing 
            the question, context, instructions, and max_tokens.
        """
        self.question = data.question
        self.context = data.context
        self.instructions = data.instructions
        self.max_tokens = data.max_tokens
        self.openai_client = OpenAIClient()

    async def answer(self) -> Dict:
        """
        Provides a grounded answer based on the provided context.

        Returns:
            Dict: The grounded answer and explanation.
        """
        return await self.grounded_answer()

    async def grounded_answer(self) -> Dict:
        """
        Generates the grounded answer using the API.

        Returns:
            Dict: The grounded answer and explanation.
        """
        system_prompt = (
            f"<CONTEXT>\n{self.context}\n\n"
            "<INSTRUCTIONS>\nBase your answer only on the information provided in the above <CONTEXT>.\n"
            "Return your answer using the JSON <OUTPUT> below.\n"
            "Do not directly mention that you're using the context in your answer.\n\n"
            f"<OUTPUT>\n{{\"explanation\": \"<explain your reasoning>\", \"answer\": \"<the answer>\"}}{self.instructions}"
        )

        user_prompt = self.question

        response = await self.openai_client.complete_chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ], max_tokens=self.max_tokens)

        return await self.process_response(response)

    async def process_response(self, response: str) -> Dict:
        """
        Processes and validates the API response.

        Args:
            response (str): The API's response to process.

        Returns:
            Dict: The validated response or an error.
        """
        try:
            result = json.loads(response)
            jsonschema.validate(instance=result, schema=self.schema)
            return result
        except (json.JSONDecodeError, jsonschema.ValidationError) as e:
            return {"error": f"Failed to parse or validate response: {str(e)}", "response": response}
