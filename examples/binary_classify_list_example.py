import asyncio
from core.binary_classify_list_agent import BinaryClassifyListAgent

async def run_binary_classify_list_example():
    items_to_classify = ['Apple', 'Chocolate', 'Carrot']
    criteria = 'Classify each item as either healthy (true) or unhealthy (false)'
    agent = BinaryClassifyListAgent(list_to_classify=items_to_classify, criteria=criteria)
    classified_items = await agent.classify_list()

    print("Original list:", items_to_classify)
    print("Binary classified results:", classified_items)

if __name__ == "__main__":
    asyncio.run(run_binary_classify_list_example())