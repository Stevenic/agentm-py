import asyncio
from core.chain_of_thought_agent import ChainOfThoughtAgent, ChainOfThoughtInput

async def run_chain_of_thought_example():
    input_data = ChainOfThoughtInput(
        question='What is the square root of 144?',
        max_tokens=1000,
        temperature=0.0
    )
    
    agent = ChainOfThoughtAgent(input_data)
    result = await agent.chain_of_thought()

    print("Question:", input_data.question)
    print("Chain of Thought Reasoning:", result)

if __name__ == "__main__":
    asyncio.run(run_chain_of_thought_example())