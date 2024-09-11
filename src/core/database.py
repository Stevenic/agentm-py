import sqlite3


class Database:
    def __init__(self, db_path):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def check_rate_limits(self, model):
        conn = self.connect()
        c = conn.cursor()

        # Check current API usage (RPM, TPM, RPD)
        c.execute(
            "SELECT SUM(total_tokens) FROM api_usage WHERE model = ? AND timestamp >= datetime('now', '-1 minute')",
            (model,),
        )
        tokens_last_minute = c.fetchone()[0] or 0

        c.execute("SELECT tpm_limit FROM rate_limits WHERE model = ?", (model,))
        tpm_limit = c.fetchone()[0]

        conn.close()
        return tokens_last_minute < tpm_limit

    def log_api_usage(
        self, session_id, model, prompt_tokens, completion_tokens, total_tokens
    ):
        conn = self.connect()
        c = conn.cursor()

        # Fetch token prices
        c.execute(
            "SELECT price_per_prompt_token, price_per_completion_token FROM models WHERE model = ?",
            (model,),
        )
        prices = c.fetchone()
        prompt_price = prices[0]
        completion_price = prices[1]
        total_cost = (prompt_tokens * prompt_price) + (
            completion_tokens * completion_price
        )

        c.execute(
            "INSERT INTO api_usage (session_id, model, prompt_tokens, completion_tokens, total_tokens, price_per_prompt_token, price_per_completion_token, total_cost) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                session_id,
                model,
                prompt_tokens,
                completion_tokens,
                total_tokens,
                prompt_price,
                completion_price,
                total_cost,
            ),
        )

        conn.commit()
        conn.close()
