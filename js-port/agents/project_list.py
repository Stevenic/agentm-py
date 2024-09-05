from pydantic import BaseModel
from typing import List, Generic, TypeVar, Optional
import asyncio
from openai import OpenAI
from .compose_prompt import compose_prompt
from .parallel_complete_prompt import parallel_complete_prompt

TItem = TypeVar('TItem')

class ProjectListArgs(BaseModel, Generic[TItem]):
    goal: str
    list: List[TItem]
    template: str
    temperature: Optional[float] = 0.0
    max_tokens: Optional[int] = 1000
    instructions: Optional[str] = None

class ProjectedItem(BaseModel, Generic[TItem]):
    projection: str
    item: TItem

async def project_list(args: ProjectListArgs[TItem]) -> List[ProjectedItem[TItem]]:
    goal = args.goal
    item_list = args.list
    template = args.template
    max_tokens = args.max_tokens
    temperature = args.temperature if args.temperature is not None else 0.0

    complete_prompt = parallel_complete_prompt(args)

    instructions = f"\n{args.instructions}" if args.instructions else ''
    system_content = compose_prompt(system_prompt, {"template": template, "goal": goal, "instructions": instructions})
    system = {"role": "system", "content": system_content}

    length = len(item_list)
    tasks = []
    for index, item in enumerate(item_list):
        prompt_content = compose_prompt(item_prompt, {"index": index, "length": length, "item": item})
        prompt = {"role": "user", "content": prompt_content}
        tasks.append(complete_prompt(prompt=prompt, system=system, temperature=temperature, max_tokens=max_tokens))

    results = await asyncio.gather(*tasks)
    errors = [result for result in results if not result['completed']]
    if errors:
        return {"completed": False, "error": errors[0]['error']}

    value = [ProjectedItem(projection=result['value'], item=item_list[index]) for index, result in enumerate(results)]
    return {"completed": True, "value": value}

system_prompt = (
    "You are an expert at re-formatting a list of items using a template.\n\n"
    "<TEMPLATE>\n"
    "{{template}}\n\n"
    "<GOAL>\n"
    "{{goal}}\n\n"
    "<INSTRUCTIONS>\n"
    "Use the <TEMPLATE> above to reformat the <ITEM> using the directions in the provided <GOAL>.{{instructions}}"
)

item_prompt = "<ITEM>\n{{item}}"
