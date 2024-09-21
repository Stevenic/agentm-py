class PromptGenerator:
    """
    A class to manage and generate combined prompts.

    Attributes:
        prompts (list): A list to store individual prompts.

    Methods:
        add_prompt(prompt): Adds a prompt to the list.
        generate_combined_prompt(): Generates a combined prompt from all stored prompts.
    """

    def __init__(self):
        """
        Constructs the PromptGenerator object and initializes the prompt list.
        """
        self.prompts = []

    def add_prompt(self, prompt):
        """
        Adds a prompt to the list of prompts.

        Args:
            prompt (str): The prompt to add to the list.
        """
        self.prompts.append(prompt)

    def generate_combined_prompt(self):
        """
        Generates a combined prompt by joining all prompts with a newline separator.

        Returns:
            str: The combined prompt.
        """
        return "\n".join(self.prompts)
