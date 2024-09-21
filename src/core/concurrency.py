import asyncio

class Semaphore:
    """
    A class that implements an asynchronous semaphore for controlling access to a limited number of concurrent tasks.

    Attributes:
        semaphore (asyncio.Semaphore): An asyncio semaphore to limit concurrent tasks.

    Methods:
        __aenter__(): Acquires the semaphore.
        __aexit__(): Releases the semaphore.
        call_function(func, *args, **kwargs): Calls a function while respecting the semaphore limits.
    """

    def __init__(self, max_concurrent_tasks):
        """
        Constructs the Semaphore object with a maximum number of concurrent tasks.

        Args:
            max_concurrent_tasks (int): The maximum number of tasks that can run concurrently.
        """
        self.semaphore = asyncio.Semaphore(max_concurrent_tasks)

    async def __aenter__(self):
        """
        Acquires the semaphore to enter a protected code block.
        """
        await self.semaphore.acquire()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Releases the semaphore after leaving a protected code block.
        """
        self.semaphore.release()

    async def call_function(self, func, *args, **kwargs):
        """
        Calls a function while respecting the semaphore limits.

        Args:
            func (Callable): The function to call.
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.

        Returns:
            Any: The result of the function call.
        """
        async with self.semaphore:
            return await func(*args, **kwargs)
