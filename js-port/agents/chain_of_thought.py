from pydantic import BaseModel
from typing import Optional, Dict, Any
import asyncio
# Assuming compose_prompt and complete_prompt are defined in the same folder
from compose_prompt import compose_prompt

class ChainOfThoughtArgs(BaseModel):
    question: str
    temperature: Optional[float] = 0.0
    max_tokens: Optional[int] = 1000
    instructions: Optional[str] = None

class ExplainedAnswer(BaseModel):
    explanation: str
    answer: str

async def chain_of_thought(args: ChainOfThoughtArgs) -> Dict[str, Any]:
    question = args.question
    max_tokens = args.max_tokens
    temperature = args.temperature
    instructions = f"\n{args.instructions}" if args.instructions else ''

    # Compose system message
    system_content = compose_prompt(system_prompt, {"instructions": instructions})
    system = {
        "role": "system",
        "content": system_content
    }

    # Complete the prompt
    prompt = {
        "role": "user",
        "content": question
    }

    # Assuming complete_prompt is an async function that returns a dictionary
    return await complete_prompt({"prompt": prompt, "system": system, "json_schema": json_schema, "temperature": temperature, "max_tokens": max_tokens})

json_schema = {
    "name": "answer",
    "schema": {
        "type": "object",
        "properties": {
            "explanation": {"type": "string"},
            "answer": {"type": "string"}
        },
        "required": ["explanation", "answer"],
        "additionalProperties": False
    },
    "strict": True
}

system_prompt = '''<INSTRUCTIONS>
Answer the users question using the JSON <OUTPUT> structure below.{{instructions}}

<OUTPUT>
{"explanation": "<explain your reasoning>", "answer": "<the answer>"}'''
