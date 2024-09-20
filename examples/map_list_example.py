import asyncio
from core.map_list_agent import MapListAgent

async def run_map_list_example():
    items_to_map = ['Apple', 'Banana', 'Carrot']
    transformation = 'Convert all items to uppercase'
    agent = MapListAgent(list_to_map=items_to_map, transformation=transformation)
    transformed_items = await agent.map_list()

    print("Original list:", items_to_map)
    print("Transformed list:", transformed_items)

if __name__ == "__main__":
    asyncio.run(run_map_list_example())