from pydantic import BaseModel, Field
from typing import List, TypeVar, Generic, Optional
import asyncio
from openai import OpenAI
from compose_prompt import compose_prompt
from parallel_complete_prompt import parallel_complete_prompt

TItem = TypeVar('TItem')

class FilterListArgs(BaseModel, Generic[TItem]):
    goal: str
    list: List[TItem]
    temperature: Optional[float] = 0.0
    max_tokens: Optional[int] = 1000
    instructions: Optional[str] = None

class Decision(BaseModel):
    explanation: str
    remove_item: bool

json_schema = {
    "name": "decision",
    "schema": {
        "type": "object",
        "properties": {
            "explanation": {"type": "string"},
            "remove_item": {"type": "boolean"}
        },
        "required": ["explanation", "remove_item"],
        "additionalProperties": False
    },
    "strict": True
}

system_prompt = (
    "You are an expert at filtering items in a list.\n\n"
    "<GOAL>\n"
    "{{goal}} \n\n"
    "<INSTRUCTIONS>\n"
    "Determine if the <ITEM> should be removed from the list using provided <GOAL>.\n"
    "Use the <DECISION> schema below to return your decisions as a JSON object.{{instructions}}\n\n"
    "<DECISION>\n"
    "{"explanation": "<explanation supporting your decision to remove item>", "remove_item": <true or false>}"
)

item_prompt = (
    "<INDEX>\n"
    "{{index}} of {{length}}\n\n"
    "<ITEM>\n"
    "{{item}}"
)

async def filter_list(args: FilterListArgs[TItem]) -> List[TItem]:
    goal = args.goal
    list_items = args.list
    max_tokens = args.max_tokens
    temperature = args.temperature if args.temperature is not None else 0.0

    complete_prompt = parallel_complete_prompt(Decision, args)

    instructions = f"\n{args.instructions}" if args.instructions else ''
    system = {
        'role': 'system',
        'content': compose_prompt(system_prompt, {'goal': goal, 'instructions': instructions})
    }

    length = len(list_items)
    tasks = []
    for index, item in enumerate(list_items):
        prompt = {
            'role': 'user',
            'content': compose_prompt(item_prompt, {'index': index, 'length': length, 'item': item})
        }
        tasks.append(complete_prompt(prompt=prompt, system=system, json_schema=json_schema, temperature=temperature, max_tokens=max_tokens))

    results = await asyncio.gather(*tasks)
    errors = [result for result in results if not result.completed]
    if errors:
        return {'completed': False, 'error': errors[0].error}

    value = [list_items[i] for i, result in enumerate(results) if not result.value.remove_item]

    return {'completed': True, 'value': value}
