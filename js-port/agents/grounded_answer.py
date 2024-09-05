from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import asyncio
# Assuming compose_prompt and complete_prompt are defined in the same way as in the TypeScript version
from compose_prompt import compose_prompt


class GroundedAnswerArgs(BaseModel):
    question: str
    context: str
    temperature: Optional[float] = 0.0
    max_tokens: Optional[int] = 1000
    instructions: Optional[str] = None


class SystemMessage(BaseModel):
    role: str
    content: str


class UserMessage(BaseModel):
    role: str
    content: str


class JsonSchema(BaseModel):
    name: str
    schema: Dict[str, Any]
    strict: bool


async def grounded_answer(args: GroundedAnswerArgs) -> Dict[str, Any]:
    question = args.question
    context = args.context
    max_tokens = args.max_tokens
    temperature = args.temperature

    # Compose system message
    instructions = f"\n{args.instructions}" if args.instructions else ''
    system = SystemMessage(
        role='system',
        content=compose_prompt(system_prompt, {"context": context, "instructions": instructions})
    )

    # Complete the prompt
    prompt = UserMessage(
        role='user',
        content=question
    )
    return await complete_prompt(prompt=prompt, system=system, json_schema=json_schema, temperature=temperature, max_tokens=max_tokens)


json_schema = JsonSchema(
    name="answer",
    schema={
        "type": "object",
        "properties": {
            "explanation": {"type": "string"},
            "answer": {"type": "string"}
        },
        "required": ["explanation", "answer"],
        "additionalProperties": False
    },
    strict=True
)


system_prompt = (
    "<CONTEXT>\n"
    "{{context}}\n"
    "\n"
    "<INSTRUCTIONS>\n"
    "Base your answer only on the information provided in the above <CONTEXT>.\n"
    "Return your answer using the JSON <OUTPUT> below. \n"
    "Do not directly mention that you're using the context in your answer.{{instructions}}\n"
    "\n"
    "<OUTPUT>\n"
    "{"explanation": "<explain your reasoning>", "answer": "<the answer>"}"
)