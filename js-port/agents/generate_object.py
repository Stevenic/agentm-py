from pydantic import BaseModel
from typing import Optional, TypeVar, Generic
import asyncio

# Assuming these are defined in other files and need to be imported
from ..types import JsonSchema, PromptCompletion, SystemMessage, UserMessage
from ..compose_prompt import compose_prompt

TObject = TypeVar('TObject')

class GenerateObjectArgs(BaseModel):
    goal: str
    json_schema: JsonSchema
    temperature: Optional[float] = 0.0
    max_tokens: Optional[int] = 1000
    context: Optional[str] = None
    instructions: Optional[str] = None

async def generate_object(args: GenerateObjectArgs) -> PromptCompletion[TObject]:
    goal = args.goal
    max_tokens = args.max_tokens
    json_schema = args.json_schema
    temperature = args.temperature

    # Compose system message
    context = f"<CONTEXT>\n{args.context}\n\n" if args.context else ''
    instructions = f"\n{args.instructions}" if args.instructions else ''
    system = SystemMessage(
        role='system',
        content=compose_prompt(system_prompt, {"context": context, "instructions": instructions})
    )

    # Complete the prompt
    prompt = UserMessage(
        role='user',
        content=goal
    )
    return await args.complete_prompt(prompt=prompt, system=system, json_schema=json_schema, temperature=temperature, max_tokens=max_tokens)

system_prompt = (
    "{{context}}<INSTRUCTIONS>\n"
    "Return a JSON object based on the users directions.{{instructions}}"
)
