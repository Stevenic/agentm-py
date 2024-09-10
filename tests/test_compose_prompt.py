import pytest
from core.compose_prompt import compose_prompt

def test_compose_prompt():
    template = "Hello, {{name}}!"
    variables = {'name': 'John'}
    
    result = compose_prompt(template, variables)
    
    assert result == "Hello, John!"
