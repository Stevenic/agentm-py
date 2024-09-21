import asyncio
from .concurrency import Semaphore

class ParallelCompletePrompt:
    """
    A class to handle parallel execution of prompt completion functions with concurrency control.

    Attributes:
        complete_prompt_func (Callable): The function to complete the prompt.
        parallel_completions (int): The number of prompts to complete in parallel.
        should_continue_func (Callable): A function to determine if the operation should continue.
        semaphore (Semaphore): A Semaphore to control concurrency.

    Methods:
        complete_prompt(*args, **kwargs): Executes the prompt completion function in parallel.
    """

    def __init__(
        self, complete_prompt_func, parallel_completions=1, should_continue_func=None
    ):
        """
        Constructs the ParallelCompletePrompt object and initializes concurrency control.

        Args:
            complete_prompt_func (Callable): The function to complete the prompt.
            parallel_completions (int): The number of prompts to complete in parallel.
            should_continue_func (Callable): A function to determine if the operation should continue.
        """
        self.complete_prompt_func = complete_prompt_func
        self.parallel_completions = parallel_completions
        self.should_continue_func = should_continue_func or (lambda: True)
        self.semaphore = Semaphore(parallel_completions)

    async def complete_prompt(self, *args, **kwargs):
        """
        Executes the prompt completion function in parallel, respecting concurrency limits.

        Raises:
            asyncio.CancelledError: If the operation is cancelled by the should_continue_func.

        Returns:
            Any: The result from the prompt completion function.
        """
        async with self.semaphore:
            if not self.should_continue_func():
                raise asyncio.CancelledError("Operation cancelled.")
            return await self.complete_prompt_func(*args, **kwargs)
