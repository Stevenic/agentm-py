import asyncio
from core.project_list_agent import ProjectListAgent

async def run_project_list_example():
    items_to_project = ['Apple', 'Banana', 'Carrot']
    projection_rule = 'Project these items as their vitamin content'
    agent = ProjectListAgent(list_to_project=items_to_project, projection_rule=projection_rule)
    projected_items = await agent.project_list()

    print("Original list:", items_to_project)
    print("Projected results:", projected_items)

if __name__ == "__main__":
    asyncio.run(run_project_list_example())