import tiktoken

class TokenCounter:
    """
    A class to count the number of tokens in a list of messages using the tiktoken library.

    Attributes:
        encoder (tiktoken.Encoding): An instance of the tiktoken encoder to encode messages.

    Methods:
        count_tokens(messages): Counts the total number of tokens in a list of messages.
    """

    def __init__(self, model="gpt-3.5-turbo"):
        """
        Constructs the TokenCounter object and initializes the encoder.

        Args:
            model (str): The model name to use for token encoding.
                        Note: tiktoken does not directly support "gpt-4o-mini" at the moment,
                        so "cl100k_base" is used as a workaround.
        """
        self.encoder = tiktoken.get_encoding("cl100k_base")

    def count_tokens(self, messages):
        """
        Counts the total number of tokens in a list of messages.

        Args:
            messages (list): A list of message dicts containing the "content" key.

        Returns:
            int: The total number of tokens in all the messages.
        """
        total_tokens = 0
        for message in messages:
            total_tokens += len(self.encoder.encode(message["content"]))
        return total_tokens

