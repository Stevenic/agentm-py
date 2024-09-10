import openai
import json
import sqlite3
from datetime import datetime
from .token_counter import TokenCounter
from .database import Database

class OpenAIClient:
    def __init__(self, settings_path='../config/settings.json'):
        settings = self.load_settings(settings_path)
        self.api_key = settings['openai_api_key']
        openai.api_key = self.api_key
        self.db = Database(settings['database_path'])
        self.token_counter = TokenCounter()

    def load_settings(self, settings_path):
        try:
            with open(settings_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise Exception(f'Settings file not found at {settings_path}')
        except KeyError as e:
            raise Exception(f'Missing key in settings: {e}')

    def complete_chat(self, messages, model='gpt-4o-mini', max_tokens=1500):
        # Check rate limits
        if not self.db.check_rate_limits(model):
            raise Exception(f"Rate limit exceeded for model {model}")
        
        prompt_tokens = self.token_counter.count_tokens(messages)
        
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens
            )
            
            completion_tokens = self.token_counter.count_tokens(response.choices[0].message['content'])
            total_tokens = prompt_tokens + completion_tokens

            # Log token usage and cost in the database
            self.db.log_api_usage('session-1', model, prompt_tokens, completion_tokens, total_tokens)

            return response.choices[0].message['content']
        except openai.error.OpenAIError as e:
            raise Exception(f'Error with OpenAI API: {str(e)}')