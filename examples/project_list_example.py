import asyncio
from core.project_list_agent import ProjectListAgent, ProjectListInput

async def run_project_list_example():
    input_data = ProjectListInput(
        list_to_project=['Apple', 'Banana', 'Carrot'],
        projection_rule='Project these items as their vitamin content',
        max_tokens=1000
    )
    
    agent = ProjectListAgent(input_data)
    projected_items = await agent.project_list()

    print("Original list:", input_data.list_to_project)
    print("Projected results:", projected_items)

if __name__ == "__main__":
    asyncio.run(run_project_list_example())