import asyncio
from core.filter_list_agent import FilterListAgent

async def run_filter_list_example():
    goal = "Remove items that are unhealthy snacks."
    items_to_filter = [
        "Apple",
        "Chocolate bar",
        "Carrot",
        "Chips",
        "Orange"
    ]

    agent = FilterListAgent(goal=goal, items_to_filter=items_to_filter)
    filtered_results = await agent.filter()

    print("Original list:", items_to_filter)
    print("Filtered results:")
    for result in filtered_results:
        print(result)

if __name__ == "__main__":
    asyncio.run(run_filter_list_example())
