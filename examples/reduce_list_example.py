import asyncio
from core.reduce_list_agent import ReduceListAgent

async def run_reduce_list_example():
    items_to_reduce = ['Banana', 'Apple', 'Carrot']
    reduction_goal = 'Reduce these items to a single word representing their nutritional value'
    agent = ReduceListAgent(list_to_reduce=items_to_reduce, reduction_goal=reduction_goal)
    reduced_items = await agent.reduce_list()

    print("Original list:", items_to_reduce)
    print("Reduced results:", reduced_items)

if __name__ == "__main__":
    asyncio.run(run_reduce_list_example())