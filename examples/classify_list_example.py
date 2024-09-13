import asyncio
from core.classify_list_agent import ClassifyListAgent

async def run_classify_list_example():
    items_to_classify = ['Apple', 'Chocolate', 'Carrot']
    classification_criteria = 'Classify each item as healthy or unhealthy snack'
    agent = ClassifyListAgent(list_to_classify=items_to_classify, classification_criteria=classification_criteria)
    classified_items = await agent.classify_list()

    print("Original list:", items_to_classify)
    print("Classified results:", classified_items)

if __name__ == "__main__":
    asyncio.run(run_classify_list_example())