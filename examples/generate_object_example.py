import asyncio
from core.generate_object_agent import GenerateObjectAgent

async def run_generate_object_example():
    description = "A machine that can sort fruits."
    goal = "Generate a high-level design of the machine."
    agent = GenerateObjectAgent(object_description=description, goal=goal)
    generated_object = await agent.generate_object()

    print("Object description:", description)
    print("Generated object:", generated_object)

if __name__ == "__main__":
    asyncio.run(run_generate_object_example())