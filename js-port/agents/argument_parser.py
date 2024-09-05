from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, TypeVar, Generic
import asyncio
# Assuming generate_object and variable_to_string are defined in the same relative path
from ..generate_object import generate_object
from ..variable_to_string import variable_to_string

TObject = TypeVar('TObject')

class ArgumentSchemaEntry(BaseModel):
    type: str
    required: Optional[bool] = False
    # Add other JSON schema properties as needed

class ArgumentSchema(BaseModel):
    __root__: Dict[str, ArgumentSchemaEntry]

class ArgumentParserArgs(BaseModel):
    goal: str
    argv: List[str]
    schema: ArgumentSchema
    instructions: Optional[str] = None
    complete_prompt: Optional[str] = None

class PromptCompletion(Generic[TObject], BaseModel):
    result: TObject

async def argument_parser(args: ArgumentParserArgs) -> PromptCompletion[TObject]:
    goal = args.goal
    schema = args.schema.__root__
    instructions = args.instructions
    complete_prompt = args.complete_prompt

    # Define JSON schema of output object.
    json_schema = {
        'name': 'ParsedArguments',
        'schema': {
            'type': 'object',
            'properties': {},
            'required': [],
            'additionalProperties': False
        },
        'strict': False
    }

    # Set properties and required fields
    enable_strict = True
    for name, entry in schema.items():
        # Clone the entry
        clone = entry.dict()

        # Add to JSON schema
        json_schema['schema']['properties'][name] = clone

        # Check for required field
        if 'required' in clone:
            # Add to required property list
            if clone['required']:
                json_schema['schema']['required'].append(name)
            else:
                enable_strict = False

            # Remove schema property since it's not part of the JSON schema
            del clone['required']
        else:
            enable_strict = False

    # Enable strict mode if all fields are required
    if enable_strict:
        json_schema['strict'] = True

    # Parse arguments
    context = f"ARGUMENTS: {variable_to_string(args.argv) or 'NONE'}"
    result = await generate_object(goal=goal, json_schema=json_schema, context=context, instructions=instructions, complete_prompt=complete_prompt)
    return PromptCompletion(result=result)