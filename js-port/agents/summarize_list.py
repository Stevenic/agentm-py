from pydantic import BaseModel, Field
from typing import List, Generic, TypeVar, Any
import asyncio
from openai import OpenAI
from .types import AgentArgs, AgentCompletion, SystemMessage, UserMessage
from .compose_prompt import compose_prompt
from .parallel_complete_prompt import parallel_complete_prompt
from .variable_to_string import variable_to_string

TItem = TypeVar('TItem')

class SummarizeListArgs(BaseModel, Generic[TItem]):
    goal: str
    list: List[TItem]
    temperature: float = 0.0
    max_tokens: int = 1000
    instructions: str = ''

class SummarizedItem(BaseModel, Generic[TItem]):
    summary: str
    item: TItem

class Summarization(BaseModel):
    explanation: str
    summary: str

json_schema = {
    "name": "summarization",
    "schema": {
        "type": "object",
        "properties": {
            "explanation": {"type": "string"},
            "summary": {"type": "string"}
        },
        "required": ["explanation", "summary"],
        "additionalProperties": False
    },
    "strict": True
}

system_prompt = '''
You are an expert at summarizing text.

<GOAL>
{{goal}} 

<INSTRUCTIONS>
Given an <ITEM> summarize it using the directions in the provided <GOAL>.
Return your summary as a JSON <SUMMARIZATION> object.
Ensure that the summary portion is a string.{{instructions}}

<SUMMARIZATION>
{"explanation": "<explanation supporting your summarization>", "summary": "<item summary as text>"}'''

item_prompt = '''
<ITEM>
{{item}}'''

async def summarize_list(args: SummarizeListArgs[TItem]) -> AgentCompletion[List[SummarizedItem[TItem]]]:
    goal = args.goal
    list_items = args.list
    max_tokens = args.max_tokens
    temperature = args.temperature

    complete_prompt = parallel_complete_prompt[Summarization](args)

    instructions = f"\n{args.instructions}" if args.instructions else ''
    system = SystemMessage(
        role='system',
        content=compose_prompt(system_prompt, {'goal': goal, 'instructions': instructions})
    )

    length = len(list_items)
    tasks = []
    for index, item in enumerate(list_items):
        prompt = UserMessage(
            role='user',
            content=compose_prompt(item_prompt, {'index': index, 'length': length, 'item': item})
        )
        tasks.append(complete_prompt(prompt=prompt, system=system, json_schema=json_schema, temperature=temperature, max_tokens=max_tokens))

    results = await asyncio.gather(*tasks)
    errors = [result for result in results if not result.completed]
    if errors:
        return AgentCompletion(completed=False, error=errors[0].error)

    value = [SummarizedItem(summary=variable_to_string(result.value.summary), item=list_items[index]) for index, result in enumerate(results)]
    return AgentCompletion(completed=True, value=value)
