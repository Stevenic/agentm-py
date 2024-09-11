from openai import OpenAI, BadRequestError
from .logging import Logger  # Use the logger abstraction
import os

class OpenAIClient:
    def __init__(self, settings_path=None):
        if settings_path is None:
            settings_path = os.path.join(os.path.dirname(__file__), '../../config/settings.json')

        self.logger = Logger(settings_path)
        settings = self.logger.load_settings(settings_path)
        self.client = OpenAI(api_key=settings["openai_api_key"])

    async def complete_chat(self, messages, model="gpt-4o-mini", max_tokens=1500):
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
