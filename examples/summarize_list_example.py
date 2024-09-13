import asyncio
from core.summarize_list_agent import SummarizeListAgent

async def run_summarize_list_example():
    items_to_summarize = ['The quick brown fox jumps over the lazy dog.', 'Python is a popular programming language.']
    agent = SummarizeListAgent(list_to_summarize=items_to_summarize)
    summaries = await agent.summarize_list()

    print("Original list:", items_to_summarize)
    print("Summarized results:", summaries)

if __name__ == "__main__":
    asyncio.run(run_summarize_list_example())