import asyncio
from core.chain_of_thought_agent import ChainOfThoughtAgent

async def run_chain_of_thought_example():
    question = 'What is the square root of 144?'
    agent = ChainOfThoughtAgent(question=question)
    result = await agent.chain_of_thought()

    print("Question:", question)
    print("Chain of Thought Reasoning:", result)

if __name__ == "__main__":
    asyncio.run(run_chain_of_thought_example())