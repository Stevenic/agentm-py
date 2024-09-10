class PromptGenerator:
    def __init__(self):
        self.prompts = []

    def add_prompt(self, prompt):
        self.prompts.append(prompt)

    def generate_combined_prompt(self):
        return "\n".join(self.prompts)
