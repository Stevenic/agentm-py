import re

def compose_prompt(template: str, variables: dict) -> str:
    """
    Composes a prompt by substituting variables in a template string.

    Args:
        template (str): The template string containing placeholders in the form of {{variable_name}}.
        variables (dict): A dictionary where keys are variable names and values are the replacements.

    Returns:
        str: The composed string with all placeholders replaced by their corresponding values.
    """
    return re.sub(
        r"{{\s*([^}\s]+)\s*}}",
        lambda match: str(variables.get(match.group(1), "")),
        template,
    )
