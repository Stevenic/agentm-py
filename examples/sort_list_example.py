import asyncio
from core.sort_list_agent import SortListAgent 

async def run_sort_list_example():
    # Sample input list
    items_to_sort = [
        "Apple", "Orange", "Banana", "Grape", "Pineapple"
    ]
    
    # Define a goal for sorting (this will influence the OpenAI model's decision)
    goal = "Sort the fruits alphabetically."
    
    # Create the sorting agent
    agent = SortListAgent(goal=goal, list_to_sort=items_to_sort, log_explanations=True)
    
    # Execute the sorting process
    sorted_list = await agent.sort()
    
    # Output the result
    print("Original list:", items_to_sort)
    print("Sorted list:", sorted_list)

# Run the example
if __name__ == "__main__":
    asyncio.run(run_sort_list_example())