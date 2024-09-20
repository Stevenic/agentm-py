import asyncio
from core.grounded_answer_agent import GroundedAnswerAgent

async def run_grounded_answer_example():
    question = "What is the capital of France?"
    context = "France is a country in Western Europe. Paris is its capital and largest city."
    instructions = "Ensure the answer is grounded only in the provided context."
    agent = GroundedAnswerAgent(question=question, context=context, instructions=instructions)
    result = await agent.answer()

    print("Question:", question)
    print("Result:", result)

if __name__ == "__main__":
    asyncio.run(run_grounded_answer_example())