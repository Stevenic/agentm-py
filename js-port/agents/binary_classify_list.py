from pydantic import BaseModel, Field
from typing import List, TypeVar, Generic, Optional, Any
import asyncio
from .types import AgentArgs, AgentCompletion, SystemMessage, UserMessage
from .compose_prompt import compose_prompt
from .parallel_complete_prompt import parallel_complete_prompt

TItem = TypeVar('TItem')

class BinaryClassifyListArgs(BaseModel, Generic[TItem]):
    goal: str
    list: List[TItem]
    temperature: Optional[float] = 0.0
    max_tokens: Optional[int] = 1000
    instructions: Optional[str] = None

class BinaryClassifiedItem(BaseModel, Generic[TItem]):
    matches: bool
    item: TItem

class Classification(BaseModel):
    explanation: str
    matches: bool

json_schema = {
    "name": "classification",
    "schema": {
        "type": "object",
        "properties": {
            "explanation": {"type": "string"},
            "matches": {"type": "boolean"}
        },
        "required": ["explanation", "matches"],
        "additionalProperties": False
    },
    "strict": True
}

system_prompt = (
    "You are an expert at classifying items in a list.\n\n"
    "<GOAL>\n"
    "{{goal}} \n\n"
    "<INSTRUCTIONS>\n"
    "Given an <ITEM> determine if it matches the provided <GOAL>.\n"
    "Return your classification as a JSON <CLASSIFICATION> object.{{instructions}}\n\n"
    "<CLASSIFICATION>\n"
    "{\"explanation\": \"<explanation supporting your classification>\", \"matches\": <true or false>}"
)

item_prompt = (
    "<INDEX>\n"
    "{{index}} of {{length}}\n\n"
    "<ITEM>\n"
    "{{item}}"
)

async def binary_classify_list(args: BinaryClassifyListArgs[TItem]) -> AgentCompletion[List[BinaryClassifiedItem[TItem]]]:
    goal = args.goal
    list_items = args.list
    max_tokens = args.max_tokens
    temperature = args.temperature if args.temperature is not None else 0.0

    complete_prompt = parallel_complete_prompt[Classification](args)

    instructions = f"\n{args.instructions}" if args.instructions else ''
    system = SystemMessage(
        role='system',
        content=compose_prompt(system_prompt, {"goal": goal, "instructions": instructions})
    )

    length = len(list_items)
    tasks = []
    for index, item in enumerate(list_items):
        prompt = UserMessage(
            role='user',
            content=compose_prompt(item_prompt, {"index": index, "length": length, "item": item})
        )
        tasks.append(complete_prompt(prompt=prompt, system=system, json_schema=json_schema, temperature=temperature, max_tokens=max_tokens))

    results = await asyncio.gather(*tasks)
    errors = [result for result in results if not result.completed]
    if errors:
        return AgentCompletion(completed=False, error=errors[0].error)

    value = [BinaryClassifiedItem(matches=result.value.matches, item=list_items[index]) for index, result in enumerate(results)]
    return AgentCompletion(completed=True, value=value)
