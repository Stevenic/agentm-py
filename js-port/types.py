from pydantic import BaseModel, Field
from typing import List, Optional, Union, Callable, Any
import asyncio

# Agent Arguments

class AgentArgs(BaseModel):
    """
    Common arguments supported by all agents.
    """
    complete_prompt: Callable[..., asyncio.Future]  # Function to complete prompts
    should_continue: Optional[Callable[[], Union[bool, asyncio.Future]]] = None  # Optional cancellation function
    parallel_completions: Optional[int] = Field(default=1, description="Maximum number of parallel completions allowed.")


# Common result fields returned by all agents.
class AgentCompletion(BaseModel):
    completed: bool  # Indicates whether the agent completed successfully
    value: Optional[Any] = None  # The value returned by the agent if it successfully completed
    error: Optional[Exception] = None  # Error returned by the agent if it did not complete successfully


# Adds an "explanation" field to an object to create a chain-of-thought.
class WithExplanation(BaseModel):
    explanation: Optional[str] = None


# Function that agents can call to check for cancellation.
ShouldContinue = Callable[[], Union[bool, asyncio.Future]]


# Function that completes a prompt.
class PromptCompletionArgs(BaseModel):
    prompt: 'UserMessage'  # The prompt to complete formatted as a "user" message
    system: Optional['SystemMessage'] = None  # Optional system message to send with the prompt
    history: Optional[List['Message']] = None  # Optional history of messages leading up to the prompt
    temperature: Optional[float] = None  # Optional temperature the model should use for sampling completions
    max_tokens: Optional[int] = None  # Optional maximum number of tokens the model should return
    json_mode: Optional[bool] = None  # Optional indicates whether the model should always return JSON as its output
    json_schema: Optional['JsonSchema'] = None  # Optional JSON schema used to enforce the models output


class PromptCompletion(BaseModel):
    completed: bool
    value: Optional[Any] = None
    error: Optional[Exception] = None
    details: Optional['PromptCompletionDetails'] = None  # Optional details about the usage of the model for this completion


class PromptCompletionDetails(BaseModel):
    input_tokens: int  # Number of tokens sent to the model
    output_tokens: int  # Number of tokens returned by the model
    finish_reason: str  # Reason the completion finished


class JsonSchema(BaseModel):
    name: str  # The name of the schema
    schema: dict  # The schema definition
    description: Optional[str] = None  # Optional description of when the schema should be used
    strict: Optional[bool] = None  # Optional indicates whether the schema should be strictly enforced


# Message Types
class Message(BaseModel):
    role: str  # Role of the message
    content: str  # Content of the message
    name: Optional[str] = None  # Optional name of the user sending the message


class SystemMessage(Message):
    role: str = 'system'


class UserMessage(Message):
    role: str = 'user'


class AssistantMessage(Message):
    role: str = 'assistant'


# Tokenizers
class Tokenizer(BaseModel):
    encode_tokens: Callable[[str], List[int]]  # Converts a string of text into tokens
    decode_tokens: Callable[[List[int]], str]  # Converts an array of tokens into a string of text


class ExplainedAnswer(BaseModel):
    explanation: str  # Explanation of the models reasoning for the answer
    answer: str  # Answer to the question
