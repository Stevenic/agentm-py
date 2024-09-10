import pytest
from core.parallel_complete_prompt import ParallelCompletePrompt

@pytest.mark.anyio
async def test_parallel_completion():
    async def mock_complete_prompt(*args, **kwargs):
        return {'completed': True, 'value': 'Success'}

    parallel_prompt = ParallelCompletePrompt(mock_complete_prompt)
    result = await parallel_prompt.complete_prompt()

    assert result['completed'] == True
