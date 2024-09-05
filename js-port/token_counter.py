from typing import Callable, Optional
from tiktoken import encode_tokens

class TokenCounterArgs:
    def __init__(self, encode_tokens: Callable[[str], list], max_expected_tokens: Optional[int] = None):
        self.encode_tokens = encode_tokens
        self.max_expected_tokens = max_expected_tokens


def token_counter(args: TokenCounterArgs) -> Callable[[str], int]:
    encode_tokens = args.encode_tokens
    max_expected_tokens = args.max_expected_tokens
    length_threshold = max_expected_tokens * 8 if max_expected_tokens else float('inf')

    def count_tokens(text: str) -> int:
        if len(text) < length_threshold:
            return len(encode_tokens(text))
        else:
            return len(text) // 4

    return count_tokens
