from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict, Union
import asyncio
import requests
import openai
import tiktoken

# Define data models using Pydantic
class OpenaiArgs(BaseModel):
    api_key: str
    model: str
    base_url: Optional[str] = None
    organization: Optional[str] = None
    project: Optional[str] = None
    temperature: Optional[float] = 0.0
    max_tokens: Optional[int] = 1000

class OpenAICompletionArgs(BaseModel):
    client: Any  # This would be the OpenAI client
    model: str
    prompt: str
    system: Optional[str] = None
    history: Optional[List[str]] = None
    temperature: Optional[float] = 0.0
    max_tokens: Optional[int] = 1000
    json_schema: Optional[Dict[str, Any]] = None

# Function to create a completion function for OpenAI chat models
async def openai(args: OpenaiArgs):
    client = openai.OpenAI(api_key=args.api_key, base_url=args.base_url, organization=args.organization, project=args.project)
    can_use_structured_outputs = args.model in ['gpt-4o-mini', 'gpt-4o-2024-08-06', 'gpt-4o-mini-2024-07-18']

    async def completion_function(args: OpenAICompletionArgs):
        if args.json_schema and can_use_structured_outputs:
            return await openai_structured_output_completion(args)
        elif args.json_schema:
            return await openai_json_chat_completion(args)
        else:
            return await openai_chat_completion(args)

    return completion_function

# Function to return a tokenizer for OpenAI models
class Tokenizer:
    def __init__(self, encoding: str = 'o200k_base'):
        self.encoding = encoding

    def encode_tokens(self, text: str) -> List[int]:
        if self.encoding == 'cl100k_base':
            return tiktoken.encode(text, model='gpt-3.5')
        else:
            return tiktoken.encode(text, model='gpt-4o')

    def decode_tokens(self, tokens: List[int]) -> str:
        if self.encoding == 'cl100k_base':
            return tiktoken.decode(tokens, model='gpt-3.5')
        else:
            return tiktoken.decode(tokens, model='gpt-4o')

# Function to perform a text completion using an OpenAI chat model
async def openai_chat_completion(args: OpenAICompletionArgs) -> Dict[str, Any]:
    try:
        messages = []
        if args.system:
            messages.append(args.system)
        if args.history:
            messages.extend(args.history)
        messages.append(args.prompt)

        response = await args.client.ChatCompletion.create(
            model=args.model,
            messages=messages,
            temperature=args.temperature,
            max_tokens=args.max_tokens
        )

        choice = response['choices'][0]
        finish_reason = get_finish_reason(choice)
        details = usage_to_details(response.get('usage'), finish_reason)

        value = choice.get('message', {}).get('content', '')
        return {'completed': True, 'value': value, 'details': details}
    except Exception as err:
        return {'completed': False, 'error': str(err)}

# Function to perform a JSON completion using an OpenAI chat model
async def openai_json_chat_completion(args: OpenAICompletionArgs) -> Dict[str, Any]:
    try:
        messages = []
        if args.system:
            messages.append(args.system)
        if args.history:
            messages.extend(args.history)
        messages.append(args.prompt)

        response = await args.client.ChatCompletion.create(
            model=args.model,
            messages=messages,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
            response_format={'type': 'json_object'}
        )

        choice = response['choices'][0]
        finish_reason = get_finish_reason(choice)
        details = usage_to_details(response.get('usage'), finish_reason)

        if choice.get('message', {}).get('refusal'):
            return {'completed': False, 'error': choice['message']['refusal'], 'details': details}

        if choice.get('finish_reason') == 'length':
            return {'completed': False, 'error': 'The conversation was too long for the context window.', 'details': details}

        if choice.get('finish_reason') == 'content_filter':
            return {'completed': False, 'error': "The model's output included restricted content.", 'details': details}

        if choice.get('finish_reason') == 'stop':
            value = response['choices'][0]['message']['content']
            return {'completed': True, 'value': value, 'details': details}
        else:
            return {'completed': False, 'error': 'The model did not properly complete the request.', 'details': details}
    except Exception as err:
        return {'completed': False, 'error': str(err)}

# Function to perform a completion that returns a structured output
async def openai_structured_output_completion(args: OpenAICompletionArgs) -> Dict[str, Any]:
    try:
        messages = []
        if args.system:
            messages.append(args.system)
        if args.history:
            messages.extend(args.history)
        messages.append(args.prompt)

        response = await args.client.ChatCompletion.create(
            model=args.model,
            messages=messages,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
            response_format={
                'type': 'json_schema',
                'json_schema': {
                    'name': args.json_schema['name'],
                    'description': args.json_schema['description'],
                    'schema': args.json_schema['schema'],
                    'strict': args.json_schema['strict'],
                }
            }
        )

        choice = response['choices'][0]
        finish_reason = get_finish_reason(choice)
        details = usage_to_details(response.get('usage'), finish_reason)

        if choice.get('message', {}).get('refusal'):
            return {'completed': False, 'error': choice['message']['refusal'], 'details': details}

        if choice.get('finish_reason') == 'length':
            return {'completed': False, 'error': 'The conversation was too long for the context window.', 'details': details}

        if choice.get('finish_reason') == 'content_filter':
            return {'completed': False, 'error': "The model's output included restricted content.", 'details': details}

        if choice.get('finish_reason') == 'stop':
            value = choice.get('message', {}).get('parsed', None)
            if not value:
                value = response['choices'][0]['message']['content']
            return {'completed': True, 'value': value, 'details': details}
        else:
            return {'completed': False, 'error': 'The model did not properly complete the request.', 'details': details}
    except Exception as err:
        return {'completed': False, 'error': str(err)}

# Helper functions

def usage_to_details(usage: Optional[Dict[str, Any]], finish_reason: str) -> Optional[Dict[str, Any]]:
    if usage:
        return {
            'inputTokens': usage.get('prompt_tokens'),
            'outputTokens': usage.get('completion_tokens'),
            'finishReason': finish_reason,
        }
    return None

def get_finish_reason(choice: Optional[Dict[str, Any]]) -> str:
    finish_reason_map = {
        'length': 'length',
        'stop': 'stop',
        'content_filter': 'filtered',
        'tool_calls': 'tool_call',
        'function_call': 'tool_call',
    }
    return finish_reason_map.get(choice.get('finish_reason'), 'unknown')
