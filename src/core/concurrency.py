import asyncio


class Semaphore:
    def __init__(self, max_concurrent_tasks):
        self.semaphore = asyncio.Semaphore(max_concurrent_tasks)

    async def __aenter__(self):
        await self.semaphore.acquire()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.semaphore.release()

    async def call_function(self, func, *args, **kwargs):
        async with self.semaphore:
            return await func(*args, **kwargs)
