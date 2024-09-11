from core.prompt_generation import PromptGenerator


def test_prompt_generation():
    generator = PromptGenerator()
    generator.add_prompt("This is prompt 1")
    generator.add_prompt("This is prompt 2")

    combined = generator.generate_combined_prompt()

    assert combined == "This is prompt 1\nThis is prompt 2"
