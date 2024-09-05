from pydantic import BaseModel, Field
from typing import List, Union, Dict, Any
import asyncio
from openai import OpenAI
from .types import AgentCompletion, JsonSchema, SystemMessage, UserMessage, WithExplanation
from .compose_prompt import compose_prompt
from .parallel_complete_prompt import parallel_complete_prompt


class BaseMapListArgs(BaseModel):
    goal: str
    list: List[Any]
    temperature: float = 0.0
    max_tokens: int = 1000
    instructions: str = ''


class ShapeBasedMapListArgs(BaseMapListArgs):
    json_shape: Dict[str, Any]


class SchemaBasedMapListArgs(BaseMapListArgs):
    json_schema: JsonSchema


async def map_list(args: Union[ShapeBasedMapListArgs, SchemaBasedMapListArgs]) -> AgentCompletion[List[Dict[str, Any]]]:
    goal = args.goal
    item_list = args.list
    max_tokens = args.max_tokens
    temperature = args.temperature

    complete_prompt = parallel_complete_prompt(args)

    json_schema = None
    instructions = f"\n{args.instructions}" if args.instructions else ''

    if isinstance(args, SchemaBasedMapListArgs):
        json_schema = args.json_schema.dict()
        json_schema['schema']['properties']['explanation'] = {'type': 'string', 'description': 'explanation supporting the mapping you did'}
        if 'required' in json_schema['schema'] and isinstance(json_schema['schema']['required'], list):
            json_schema['schema']['required'].append('explanation')
        else:
            json_schema['schema']['required'] = ['explanation']
        system = SystemMessage(
            role='system',
            content=compose_prompt(schema_system_prompt, {'goal': goal, 'instructions': instructions})
        )
    else:
        output_shape = {**args.json_shape, 'explanation': explanation}
        system = SystemMessage(
            role='system',
            content=compose_prompt(shape_system_prompt, {'goal': goal, 'instructions': instructions, 'outputShape': output_shape})
        )

    json_mode = True
    length = len(item_list)
    tasks = []
    for index, item in enumerate(item_list):
        prompt = UserMessage(
            role='user',
            content=compose_prompt(item_prompt, {'index': index, 'length': length, 'item': item})
        )
        tasks.append(complete_prompt(prompt=prompt, system=system, json_mode=json_mode, json_schema=json_schema, temperature=temperature, max_tokens=max_tokens))

    results = await asyncio.gather(*tasks)
    errors = [result for result in results if not result.completed]
    if errors:
        return AgentCompletion(completed=False, error=errors[0].error)

    value = [result.value for result in results if result.value]
    for item in value:
        item.pop('explanation', None)

    return AgentCompletion(completed=True, value=value)


explanation = "<explanation supporting the mapping you did>"
schema_system_prompt = (
    "You are an expert at mapping list items from one type to another.\n\n"
    "<GOAL>\n"
    "{{goal}} \n\n"
    "<INSTRUCTIONS>\n"
    "Given an <ITEM> map the item to the provided JSON shape using the instructions specified by the <GOAL>.{{instructions}}"
)
shape_system_prompt = (
    "You are an expert at mapping list items from one type to another.\n\n"
    "<GOAL>\n"
    "{{goal}} \n\n"
    "<INSTRUCTIONS>\n"
    "Given an <ITEM> return a new JSON <OUTPUT> object that maps the item to the shape specified by the <GOAL>.{{instructions}}\n\n"
    "<OUTPUT>\n"
    "{{outputShape}}"
)
item_prompt = (
    "<INDEX>\n"
    "{{index}} of {{length}}\n\n"
    "<ITEM>\n"
    "{{item}}"
)
