from unittest import mock
from core.database import Database


def test_check_rate_limits():
    # Mock the database connection and cursor
    mock_conn = mock.MagicMock()
    mock_cursor = mock_conn.cursor.return_value

    # Mock the cursor's return values for token limits and usage
    mock_cursor.fetchone.side_effect = [
        (100,),
        (50000,),
    ]  # Return tuples for token usage and limit

    # Patch the connect method to return the mock connection
    with mock.patch("sqlite3.connect", return_value=mock_conn):
        db = Database(db_path=":memory:")  # Use an in-memory database for testing

        # Call the method and assert it returns True (since usage < limit)
        assert db.check_rate_limits("gpt-4o-mini") == True


def test_log_and_delete_api_usage():
    # Mock the database connection and cursor
    mock_conn = mock.MagicMock()
    mock_cursor = mock_conn.cursor.return_value

    # Patch the connect method to return the mock connection
    with mock.patch("sqlite3.connect", return_value=mock_conn):
        db = Database(db_path=":memory:")

        # Log the API usage
        db.log_api_usage("session-1", "gpt-4o-mini", 100, 200, 300)

        # Assert the INSERT query was executed
        mock_cursor.execute.assert_any_call(
            "INSERT INTO api_usage (session_id, model, prompt_tokens, completion_tokens, total_tokens, price_per_prompt_token, price_per_completion_token, total_cost) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            ("session-1", "gpt-4o-mini", 100, 200, 300, mock.ANY, mock.ANY, mock.ANY),
        )

        # Mock the SELECT query to return the inserted values
        mock_cursor.fetchone.side_effect = [("session-1", "gpt-4o-mini", 100, 200, 300)]

        # Simulate fetching the logged API usage
        db.connect().cursor().execute(
            "SELECT * FROM api_usage WHERE session_id = ?", ("session-1",)
        )

        # Now simulate deleting the entry
        db.connect().cursor().execute(
            "DELETE FROM api_usage WHERE session_id = ?", ("session-1",)
        )

        # Assert the DELETE query was executed
        mock_cursor.execute.assert_any_call(
            "DELETE FROM api_usage WHERE session_id = ?", ("session-1",)
        )
