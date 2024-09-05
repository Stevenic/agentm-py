from cancelled_error import CancelledError
from types import complete_prompt
import asyncio

# Function to log the results of the wrapped complete_prompt
async def log_complete_prompt(complete_prompt, log_details=False):
    async def wrapper(args):
        result = await complete_prompt(args)

        # Ignore cancellations
        if isinstance(result.error, CancelledError):
            return result

        # Log completion
        if result.completed:
            print(colorize_output(result.value))
        elif result.error:
            print(colorize_error(result.error))
        else:
            print(colorize_error('Prompt failed to complete.'))

        # Log details
        if log_details and result.details:
            print(colorize_value('Input Tokens', result.details.input_tokens))
            print(colorize_value('Output Tokens', result.details.output_tokens))
            print(colorize_value('Finish Reason', result.details.finish_reason))

        # Create separator
        print('=' * 80)
        return result

    return wrapper


def colorize_error(error):
    if isinstance(error, str):
        return f"\x1b[31;1m{error}\x1b[0m"
    else:
        return f"\x1b[31;1m{error.message}\x1b[0m"


def colorize_value(field, value, units=''):
    return f"{field}: {colorize_output(value, '"', units)}"


def colorize_output(output, quote='', units=''):
    if isinstance(output, str):
        return f"\x1b[32m{quote}{output}{quote}\x1b[0m"
    elif isinstance(output, dict):
        return colorize_output(json.dumps(output, indent=2))
    elif isinstance(output, (int, float)):
        return f"\x1b[34m{output}{units}\x1b[0m"
    else:
        return f"\x1b[34m{output}\x1b[0m"
