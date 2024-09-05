from pydantic import BaseModel, Field
from typing import List, TypeVar, Generic
import asyncio
from openai import OpenAI
from .compose_prompt import compose_prompt
from .parallel_complete_prompt import parallel_complete_prompt

TItem = TypeVar('TItem')

class SortListArgs(BaseModel, Generic[TItem]):
    goal: str
    list: List[TItem]
    temperature: float = 0.0
    max_tokens: int = 1000
    instructions: str = ""
    log_explanations: bool = False

class Decision(BaseModel):
    explanation: str
    sort_item_a: str = Field(..., regex="^(BEFORE|EQUAL|AFTER)$")

json_schema = {
    "name": "decision",
    "schema": {
        "type": "object",
        "properties": {
            "explanation": {"type": "string"},
            "sort_item_a": {"type": "string", "enum": ["BEFORE", "EQUAL", "AFTER"]}
        },
        "required": ["explanation", "sort_item_a"],
        "additionalProperties": False
    },
    "strict": True
}

system_prompt = '''
You are an expert in sorting a list of items.

<GOAL>
{{goal}} 

<INSTRUCTIONS>
Determine if <ITEM_A> should be sorted BEFORE, EQUAL, or AFTER <ITEM_B> based upon the stated <GOAL>.
Use the <DECISION> schema below to return your decisions as a JSON object.{{instructions}}

<DECISION>
{"explanation": "<explanation supporting your decision>", "sort_item_a": "<BEFORE, EQUAL, or AFTER>"}'''

item_prompt = '''
<ITEM_A>
{{a}}

<ITEM_B>
{{b}}'''

async def sort_list(args: SortListArgs[TItem]) -> List[TItem]:
    goal = args.goal
    list_items = args.list
    max_tokens = args.max_tokens
    temperature = args.temperature

    complete_prompt = parallel_complete_prompt(args)

    instructions = f"\n{args.instructions}" if args.instructions else ''
    system = {
        'role': 'system',
        'content': compose_prompt(system_prompt, {'goal': goal, 'instructions': instructions})
    }

    async def comparer(a: TItem, b: TItem) -> int:
        prompt = {
            'role': 'user',
            'content': compose_prompt(item_prompt, {'a': a, 'b': b})
        }

        result = await complete_prompt({
            'prompt': prompt,
            'system': system,
            'json_schema': json_schema,
            'temperature': temperature,
            'max_tokens': max_tokens
        })

        if not result['completed']:
            raise Exception(result['error'])

        if args.log_explanations:
            print(f"\x1b[32m{a}\x1b[0m is {result['value']['sort_item_a']} \x1b[32m{b}\x1b[0m because \x1b[32m{result['value']['explanation']}\x1b[0m\n")

        if result['value']['sort_item_a'] == 'BEFORE':
            return -1
        elif result['value']['sort_item_a'] == 'AFTER':
            return 1
        else:
            return 0

    try:
        sorted_list = await merge_sort(list_items, comparer)
    except Exception as err:
        return {'completed': False, 'error': err}

    return {'completed': True, 'value': sorted_list}

async def merge_sort(list_items: List[TItem], comparer) -> List[TItem]:
    if len(list_items) < 2:
        return list_items
    return await split(list_items, comparer)

async def split(list_items: List[TItem], comparer) -> List[TItem]:
    if len(list_items) < 2:
        return list_items

    mid = len(list_items) // 2
    left = list_items[:mid]
    right = list_items[mid:]

    left_list, right_list = await asyncio.gather(split(left, comparer), split(right, comparer))
    return await merge(left_list, right_list, comparer)

async def merge(left_list: List[TItem], right_list: List[TItem], comparer) -> List[TItem]:
    result = []
    left_index = 0
    right_index = 0

    while left_index < len(left_list) and right_index < len(right_list):
        comparison = await comparer(left_list[left_index], right_list[right_index])
        if comparison <= 0:
            result.append(left_list[left_index])
            left_index += 1
        else:
            result.append(right_list[right_index])
            right_index += 1

    result.extend(left_list[left_index:])
    result.extend(right_list[right_index:])
    return result
