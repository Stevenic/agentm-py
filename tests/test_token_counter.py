import pytest
from core.token_counter import TokenCounter


def test_token_counting():
    counter = TokenCounter()

    messages = [{"role": "user", "content": "Hello!"}]
    token_count = counter.count_tokens(messages)

    assert token_count > 0
