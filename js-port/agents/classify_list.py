from pydantic import BaseModel, Field
from typing import List, Generic, TypeVar, Optional
import asyncio
from openai import OpenAI
from .types import AgentCompletion, SystemMessage, UserMessage
from .compose_prompt import compose_prompt
from .parallel_complete_prompt import parallel_complete_prompt

TItem = TypeVar('TItem')

class ClassifyListArgs(BaseModel, Generic[TItem]):
    goal: str
    list: List[TItem]
    categories: List[str]
    temperature: Optional[float] = 0.0
    max_tokens: Optional[int] = 1000
    instructions: Optional[str] = None

class ClassifiedItem(BaseModel, Generic[TItem]):
    category: str
    item: TItem

class Classification(BaseModel):
    explanation: str
    category: str

json_schema = {
    "name": "classification",
    "schema": {
        "type": "object",
        "properties": {
            "explanation": {"type": "string"},
            "category": {"type": "string"}
        },
        "required": ["explanation", "category"],
        "additionalProperties": False
    },
    "strict": True
}

system_prompt = '''
You are an expert at classifying items in a list.

<CATEGORIES>
{{categories}}

<GOAL>
{{goal}} 

<INSTRUCTIONS>
Given an <ITEM> classify the item using the above <CATEGORIES> based upon the provided <GOAL>.
Return your classification as a JSON <CLASSIFICATION> object.{{instructions}}

<CLASSIFICATION>
{"explanation": "<explanation supporting your classification>", "category": "<category assigned>"}'''

item_prompt = '''
<INDEX>
{{index}} of {{length}}

<ITEM>
{{item}}'''

async def classify_list(args: ClassifyListArgs[TItem]) -> AgentCompletion[List[ClassifiedItem[TItem]]]:
    goal, list_items, max_tokens = args.goal, args.list, args.max_tokens
    temperature = args.temperature if args.temperature is not None else 0.0

    complete_prompt = parallel_complete_prompt(Classification, args)

    categories = '\n'.join(f'* {category}' for category in args.categories)
    instructions = f"\n{args.instructions}" if args.instructions else ''
    system = SystemMessage(
        role='system',
        content=compose_prompt(system_prompt, {'goal': goal, 'categories': categories, 'instructions': instructions, 'maxTokens': max_tokens})
    )

    length = len(list_items)
    tasks = []
    for index, item in enumerate(list_items):
        prompt = UserMessage(
            role='user',
            content=compose_prompt(item_prompt, {'index': index, 'length': length, 'item': item})
        )
        tasks.append(complete_prompt(prompt=prompt, system=system, json_schema=json_schema, temperature=temperature))

    results = await asyncio.gather(*tasks)
    errors = [result for result in results if not result.completed]
    if errors:
        return AgentCompletion(completed=False, error=errors[0].error)

    value = [ClassifiedItem(category=result.value.category, item=list_items[index]) for index, result in enumerate(results)]
    return AgentCompletion(completed=True, value=value)
