from pydantic import BaseModel, Field
from typing import Any, List, Dict, Optional, Callable
import asyncio
from openai import OpenAI
from .types import AgentCompletion, WithExplanation, SystemMessage, UserMessage
from .compose_prompt import compose_prompt
from .cancelled_error import CancelledError


class ReduceListArgs(BaseModel):
    goal: str
    list: List[Any]
    initial_value: Dict[str, Any]
    json_schema: Optional[Dict[str, Any]] = None
    temperature: float = 0.0
    max_tokens: int = 1000
    max_history: int = 8
    instructions: Optional[str] = None
    should_continue: Optional[Callable[[], bool]] = lambda: True


async def reduce_list(args: ReduceListArgs) -> AgentCompletion:
    goal = args.goal
    item_list = args.list
    initial_value = args.initial_value
    json_schema = args.json_schema
    max_tokens = args.max_tokens
    complete_prompt = OpenAI.complete_prompt  # Assuming this is a method from OpenAI
    temperature = args.temperature
    max_history = max(2, args.max_history)
    should_continue = args.should_continue

    output: WithExplanation = {**initial_value, "explanation": explanation}
    instructions = f"\n{args.instructions}" if args.instructions else ''
    system = SystemMessage(
        role='system',
        content=compose_prompt(system_prompt, {'goal': goal, 'instructions': instructions, 'output': output})
    )

    json_mode = True
    length = len(item_list)
    history: List[Dict[str, Any]] = []

    for index in range(length):
        item = item_list[index]
        prompt = UserMessage(
            role='user',
            content=compose_prompt(item_prompt, {'index': index, 'length': length, 'item': item})
        )

        result: AgentCompletion = await complete_prompt(
            prompt=prompt,
            system=system,
            history=history,
            json_mode=json_mode,
            json_schema=json_schema,
            temperature=temperature,
            max_tokens=max_tokens
        )

        if not result.completed:
            return AgentCompletion(completed=False, error=result.error)
        elif not await should_continue():
            return AgentCompletion(completed=False, error=CancelledError())

        output = result.value
        history.append(prompt)
        history.append({'role': 'assistant', 'content': str(output)})

        if len(history) > max_history:
            history = history[-max_history:]

    if 'explanation' in output:
        del output['explanation']

    return AgentCompletion(completed=True, value=output)


explanation = "<explanation supporting your answer>"
system_prompt = (
    "You are an expert at combining and reducing items in a list.\n\n"
    "<GOAL>\n"
    "{{goal}} \n\n"
    "<INSTRUCTIONS>\n"
    "Given an <ITEM> return a new JSON <OUTPUT> object that combines the item with the current output to achieve the <GOAL>.{{instructions}}\n\n"
    "<OUTPUT>\n"
    "{{output}}"
)
item_prompt = (
    "<INDEX>\n"
    "{{index}} of {{length}}\n\n"
    "<ITEM>\n"
    "{{item}}"
)
