import asyncio
from core.filter_list_agent import FilterListAgent, FilterListInput

async def run_filter_list_example():
    input_data = FilterListInput(
        goal="Remove items that are unhealthy snacks.",
        items_to_filter=[
            "Apple",
            "Chocolate bar",
            "Carrot",
            "Chips",
            "Orange"
        ],
        max_tokens=500,
        temperature=0.0
    )
    
    agent = FilterListAgent(input_data)
    filtered_results = await agent.filter()

    print("Original list:", input_data.items_to_filter)
    print("Filtered results:")
    for result in filtered_results:
        print(result)

if __name__ == "__main__":
    asyncio.run(run_filter_list_example())