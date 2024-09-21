import asyncio
from core.summarize_list_agent import SummarizeListAgent, SummarizeListInput

async def run_summarize_list_example():
    input_data = SummarizeListInput(
        list_to_summarize=[
            'The quick brown fox jumps over the lazy dog.',
            'Python is a popular programming language.'
        ],
        max_tokens=1000
    )
    
    agent = SummarizeListAgent(input_data)
    summaries = await agent.summarize_list()

    print("Original list:", input_data.list_to_summarize)
    print("Summarized results:", summaries)

if __name__ == "__main__":
    asyncio.run(run_summarize_list_example())