import re

def compose_prompt(template: str, variables: dict) -> str:
    return re.sub(r'{{\s*([^}\s]+)\s*}}', lambda match: str(variables.get(match.group(1), '')), template)
