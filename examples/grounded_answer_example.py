import asyncio
from core.grounded_answer_agent import GroundedAnswerAgent, GroundedAnswerInput

async def run_grounded_answer_example():
    input_data = GroundedAnswerInput(
        question="What is the capital of France?",
        context="France is a country in Western Europe known for its wine and cuisine. The capital is a major global center for art, fashion, and culture.",
        instructions="",
        max_tokens=1000
    )
    
    agent = GroundedAnswerAgent(input_data)
    answer = await agent.answer()

    print("Question:", input_data.question)
    print("Answer:", answer)

if __name__ == "__main__":
    asyncio.run(run_grounded_answer_example())
