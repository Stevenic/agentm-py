from openai import OpenAI, BadRequestError
from .logging import Logger  # Use the logger abstraction
import os

class OpenAIClient:
    """
    A client for interacting with the OpenAI API.

    Attributes:
        logger (Logger): An instance of Logger for logging API interactions and errors.
        client (OpenAI): An instance of the OpenAI API client.

    Methods:
        complete_chat(messages, model, max_tokens): Sends a chat completion request to the OpenAI API.
    """

    def __init__(self, settings_path=None):
        """
        Constructs the OpenAIClient object and initializes the API client.

        Args:
            settings_path (str): The path to the settings JSON file containing the API key.
        """
        if settings_path is None:
            settings_path = os.path.join(os.path.dirname(__file__), '../../config/settings.json')

        self.logger = Logger(settings_path)
        settings = self.logger.load_settings(settings_path)
        self.client = OpenAI(api_key=settings["openai_api_key"])

    async def complete_chat(self, messages, model="gpt-4o-mini", max_tokens=1500):
        """
        Sends a chat completion request to the OpenAI API.

        Args:
            messages (list): A list of message dicts for the chat completion.
            model (str): The model name to use for the completion.
            max_tokens (int): The maximum number of tokens to generate.

        Returns:
            str: The generated content from the chat completion.
        
        Raises:
            BadRequestError: If there is an issue with the request to the OpenAI API.
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except BadRequestError as e:
            self.logger.error(f"Error with OpenAI API: {str(e)}")
            raise
