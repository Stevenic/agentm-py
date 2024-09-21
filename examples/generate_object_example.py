import asyncio
from core.generate_object_agent import GenerateObjectAgent, ObjectGenerationInput

async def run_generate_object_example():
    input_data = ObjectGenerationInput(
        object_description="A machine that can sort fruits.",
        goal="Generate a high-level design of the machine.",
        max_tokens=1000
    )
    
    agent = GenerateObjectAgent(input_data)
    generated_object = await agent.generate_object()

    print("Object description:", input_data.object_description)
    print("Generated object:", generated_object)

if __name__ == "__main__":
    asyncio.run(run_generate_object_example())