import asyncio
from core.map_list_agent import MapListAgent, MapListInput

async def run_map_list_example():
    input_data = MapListInput(
        list_to_map=['Apple', 'Banana', 'Carrot'],
        transformation='Convert all items to uppercase',
        max_tokens=1000
    )
    
    agent = MapListAgent(input_data)
    transformed_items = await agent.map_list()

    print("Original list:", input_data.list_to_map)
    print("Transformed list:", transformed_items)

if __name__ == "__main__":
    asyncio.run(run_map_list_example())