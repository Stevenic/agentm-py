import asyncio
import os

import json
import jsonschema
from openai import AsyncOpenAI, BadRequestError
from .logging import Logger


class OpenAIClient:
    """Reusable async transport. Share one instance across agents in an event loop.

    Use ``async with OpenAIClient(...)`` to close its connection pool. Settings
    remain compatible with the existing config file; keyword options override it.
    """

    def __init__(self, settings_path=None, *, api_key=None, base_url=None,
                 model=None, max_concurrency=8, timeout=60.0, max_retries=2,
                 reasoning_effort=None, token_limit_parameter="max_tokens"):
        if isinstance(max_concurrency, bool) or not isinstance(max_concurrency, int) or max_concurrency < 1:
            raise ValueError("max_concurrency must be a positive integer")
        if settings_path is None:
            settings_path = os.path.join(os.path.dirname(__file__), '../../config/settings.json')
        self.logger = Logger(settings_path, allow_missing=True)
        settings = self.logger.settings
        self.model = model or settings.get('model', 'gpt-4o-mini')
        if token_limit_parameter not in ("max_tokens", "max_completion_tokens"):
            raise ValueError("Unsupported token limit parameter")
        self.token_limit_parameter = token_limit_parameter
        self.reasoning_effort = reasoning_effort
        self.max_concurrency = max_concurrency
        self._semaphore = asyncio.Semaphore(max_concurrency)
        self.client = AsyncOpenAI(
            api_key=api_key or os.environ.get('OPENAI_API_KEY') or settings.get('openai_api_key'),
            base_url=base_url or settings.get('base_url'),
            timeout=timeout,
            max_retries=max_retries,
        )

    async def complete_chat(self, messages, model=None, max_tokens=1500, *,
                            temperature=None, response_format=None):
        options = {'model': model or self.model, 'messages': messages, self.token_limit_parameter: max_tokens}
        if self.reasoning_effort is not None:
            options['reasoning_effort'] = self.reasoning_effort
        if temperature is not None:
            options['temperature'] = temperature
        if response_format is not None:
            options['response_format'] = response_format
        try:
            async with self._semaphore:
                response = await self.client.chat.completions.create(**options)
            choice = response.choices[0]
            if choice.message.refusal:
                raise ValueError('Model refused the requested completion')
            if choice.finish_reason != 'stop' or choice.message.content is None:
                raise ValueError('Model did not return a complete text response')
            return choice.message.content
        except BadRequestError:
            self.logger.error('Completion request was rejected by the provider')
            raise

    async def complete_object(self, messages, schema, *, max_tokens=1500, temperature=None):
        """Generate and validate an object using a provider-supported strict schema."""
        jsonschema.Draft202012Validator.check_schema(schema)
        response = await self.complete_chat(
            messages, max_tokens=max_tokens, temperature=temperature,
            response_format={'type': 'json_schema', 'json_schema': {
                'name': 'agent_result', 'strict': True, 'schema': schema,
            }},
        )
        result = json.loads(response)
        jsonschema.Draft202012Validator(schema).validate(result)
        return result

    async def aclose(self):
        await self.client.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        await self.aclose()


class ClientOwner:
    """Agent lifecycle; an injected client remains owned by its caller."""

    def __init__(self, openai_client=None):
        self._owns_client = openai_client is None
        self.openai_client = openai_client if openai_client is not None else OpenAIClient()

    async def aclose(self):
        if self._owns_client:
            await self.openai_client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        await self.aclose()
