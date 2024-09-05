import json
from typing import Any


def variable_to_string(variable: Any) -> str:
    if variable is None:
        return ''
    if isinstance(variable, str):
        return variable
    if isinstance(variable, dict):
        return json.dumps(variable)
    return str(variable)
