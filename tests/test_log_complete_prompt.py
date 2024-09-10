import pytest
import shutil
import os
from core.log_complete_prompt import LogCompletePrompt


@pytest.mark.anyio
async def test_logging():
    # Ensure the config folder exists in the test environment
    if not os.path.exists("../config"):
        os.makedirs("../config")

    # Copy the settings.json file if it doesn't exist in the test environment
    if not os.path.exists("../config/settings.json"):
        shutil.copyfile("./config/settings.json", "../config/settings.json")

    # Define a mock completion function
    async def mock_complete_prompt(*args, **kwargs):
        return {"completed": True, "value": "Success"}

    # Initialize LogCompletePrompt
    log_prompt = LogCompletePrompt(mock_complete_prompt)
    result = await log_prompt.complete_prompt()

    # Assert the completion result
    assert result["completed"] == True
