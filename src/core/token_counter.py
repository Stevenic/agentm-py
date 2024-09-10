import tiktoken


class TokenCounter:
    def __init__(self, model="gpt-3.5-turbo"):
        self.encoder = tiktoken.get_encoding("cl100k_base")

    def count_tokens(self, messages):
        total_tokens = 0
        for message in messages:
            total_tokens += len(self.encoder.encode(message["content"]))
        return total_tokens
