import asyncio
from core.binary_classify_list_agent import BinaryClassifyListAgent, BinaryClassifyListInput

async def run_binary_classify_list_example():
    input_data = BinaryClassifyListInput(
        list_to_classify=['Apple', 'Chocolate', 'Carrot'],
        criteria='Classify each item as either healthy (true) or unhealthy (false)',
        max_tokens=1000,
        temperature=0.0
    )
    
    agent = BinaryClassifyListAgent(input_data)
    classified_items = await agent.classify_list()

    print("Original list:", input_data.list_to_classify)
    print("Binary classified results:", classified_items)

if __name__ == "__main__":
    asyncio.run(run_binary_classify_list_example())