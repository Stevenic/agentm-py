from variable_to_string import variable_to_string


def compose_prompt(template: str, variables: dict) -> str:
    """
    Composes a prompt from a template and variables.
    
    Any {{variable}} in the template will be replaced with the value of the variable or an empty
    string.
    
    :param template: Template to compose.
    :param variables: Variables to replace in the template.
    :return: Composed prompt.
    """
    import re
    
    def replace_variable(match):
        name = match.group(1)
        return variable_to_string(variables.get(name, ''))

    return re.sub(r"{{\s*([^}\s]+)\s*}}", replace_variable, template)
