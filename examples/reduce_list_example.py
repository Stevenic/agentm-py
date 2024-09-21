import asyncio
from core.reduce_list_agent import ReduceListAgent, ReduceListInput

async def run_reduce_list_example():
    input_data = ReduceListInput(
        list_to_reduce=["Apple", "Banana", "Carrot"],
        reduction_goal="Reduce each item to its first letter.",
        max_tokens=1000
    )
    
    agent = ReduceListAgent(input_data)
    reduced_items = await agent.reduce_list()

    print("Original list:", input_data.list_to_reduce)
    print("Reduced results:", reduced_items)

if __name__ == "__main__":
    asyncio.run(run_reduce_list_example())
