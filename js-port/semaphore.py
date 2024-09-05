import asyncio
from typing import Any, Callable, List

class Semaphore:
    def __init__(self, max_concurrent_requests: int = 1):
        self.current_requests: List[dict] = []
        self.running_requests: int = 0
        self.max_concurrent_requests: int = max_concurrent_requests

    async def call_function(self, fn_to_call: Callable[..., asyncio.Future], *args: Any) -> Any:
        loop = asyncio.get_event_loop()
        future = loop.create_future()
        self.current_requests.append({
            'future': future,
            'fn_to_call': fn_to_call,
            'args': args,
        })
        self.try_next()
        return await future

    def try_next(self) -> None:
        if not self.current_requests:
            return
        elif self.running_requests < self.max_concurrent_requests:
            request = self.current_requests.pop(0)
            future = request['future']
            fn_to_call = request['fn_to_call']
            args = request['args']
            self.running_requests += 1
            asyncio.ensure_future(self._execute_request(future, fn_to_call, *args))

    async def _execute_request(self, future: asyncio.Future, fn_to_call: Callable[..., asyncio.Future], *args: Any) -> None:
        try:
            result = await fn_to_call(*args)
            future.set_result(result)
        except Exception as e:
            future.set_exception(e)
        finally:
            self.running_requests -= 1
            self.try_next()
