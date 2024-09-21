from core.logging import Logger

class LogCompletePrompt:
    """
    A class that logs the completion status of a prompt.

    Attributes:
        complete_prompt_func (Callable): The function that completes the prompt.
        logger (Logger): An instance of Logger to handle logging.

    Methods:
        complete_prompt(): Executes the prompt completion and logs the result.
    """

    def __init__(self, complete_prompt_func):
        """
        Constructs all the necessary attributes for the LogCompletePrompt object.

        Args:
            complete_prompt_func (Callable): The function that completes the prompt.
        """
        self.complete_prompt_func = complete_prompt_func
        self.logger = Logger()

    async def complete_prompt(self, *args, **kwargs):
        """
        Executes the prompt completion and logs whether it was successful or not.

        Returns:
            dict: The result from the prompt completion function.
        """
        result = await self.complete_prompt_func(*args, **kwargs)

        if result["completed"]:
            self.logger.info("Prompt completed successfully.")
        else:
            self.logger.error("Prompt completion failed.")

        return result
