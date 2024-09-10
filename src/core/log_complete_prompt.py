from core.logging import Logger

class LogCompletePrompt:
    def __init__(self, complete_prompt_func):
        self.complete_prompt_func = complete_prompt_func
        self.logger = Logger()

    async def complete_prompt(self, *args, **kwargs):
        result = await self.complete_prompt_func(*args, **kwargs)

        if result['completed']:
            self.logger.info('Prompt completed successfully.')
        else:
            self.logger.error('Prompt completion failed.')

        return result
