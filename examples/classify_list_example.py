import asyncio
from core.classify_list_agent import ClassifyListAgent, ClassifyListInput

async def run_classify_list_example():
    input_data = ClassifyListInput(
        list_to_classify=["Apple", "Banana", "Carrot"],
        classification_criteria="Classify each item as a fruit or vegetable.",
        max_tokens=1000
    )
    
    agent = ClassifyListAgent(input_data)
    classifications = await agent.classify_list()

    print("Original list:", input_data.list_to_classify)
    print("Classified results:", classifications)

if __name__ == "__main__":
    asyncio.run(run_classify_list_example())
