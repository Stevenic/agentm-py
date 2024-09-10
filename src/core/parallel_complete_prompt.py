import asyncio
from .concurrency import Semaphore


class ParallelCompletePrompt:
    def __init__(
        self, complete_prompt_func, parallel_completions=1, should_continue_func=None
    ):
        self.complete_prompt_func = complete_prompt_func
        self.parallel_completions = parallel_completions
        self.should_continue_func = should_continue_func or (lambda: True)
        self.semaphore = Semaphore(parallel_completions)

    async def complete_prompt(self, *args, **kwargs):
        async with self.semaphore:
            if not self.should_continue_func():
                raise asyncio.CancelledError("Operation cancelled.")
            return await self.complete_prompt_func(*args, **kwargs)
