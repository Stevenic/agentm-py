import asyncio
import json
import jsonschema
from typing import Dict
from .openai_api import OpenAIClient

class GroundedAnswerAgent:
    def __init__(self, question: str, context: str, instructions: str = '', max_tokens: int = 1000):
        self.question = question
        self.context = context
        self.instructions = instructions
        self.max_tokens = max_tokens
        self.openai_client = OpenAIClient()

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

    async def answer(self) -> Dict:
        return await self.grounded_answer()

    async def grounded_answer(self) -> Dict:
        system_prompt = f"<CONTEXT>\n{self.context}\n\n<INSTRUCTIONS>\nBase your answer only on the information provided in the above <CONTEXT>.\nReturn your answer using the JSON <OUTPUT> below. \nDo not directly mention that you're using the context in your answer.\n\n<OUTPUT>\n{{\"explanation\": \"<explain your reasoning>\", \"answer\": \"<the answer>\"}}{self.instructions}"

        user_prompt = self.question

        response = await self.openai_client.complete_chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ], max_tokens=self.max_tokens)

        return await self.process_response(response)

    async def process_response(self, response: str) -> Dict:
        try:
            result = json.loads(response)
            jsonschema.validate(instance=result, schema=self.schema)
            return result
        except (json.JSONDecodeError, jsonschema.ValidationError) as e:
            return {"error": f"Failed to parse or validate response: {str(e)}", "response": response}
