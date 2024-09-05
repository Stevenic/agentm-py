from asyncio import Semaphore
from typing import Callable, Any, Dict
from pydantic import BaseModel

from cancelled_error import CancelledError


class AgentArgs(BaseModel):
    complete_prompt: Callable[[Dict[str, Any]], Any]
    parallel_completions: int
    should_continue: Callable[[], bool] = lambda: True


def parallel_complete_prompt(args: AgentArgs) -> Callable[[Dict[str, Any]], Any]:
    complete_prompt = args.complete_prompt
    parallel_completions = args.parallel_completions
    should_continue = args.should_continue

    # Create a new semaphore to limit completions
    semaphore = Semaphore(parallel_completions)

    async def wrapper(args: Dict[str, Any]) -> Dict[str, Any]:
        # Wait for semaphore
        async with semaphore:
            # Check for cancellation
            if not should_continue():
                return {'completed': False, 'error': CancelledError()}

            # Call complete_prompt
            return await complete_prompt(args)

    return wrapper
