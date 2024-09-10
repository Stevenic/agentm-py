import sqlite3
import os
import json
import argparse

# Function to create config/settings.json

def create_settings(ci_mode=False):
    if ci_mode:
        # Use default values for CI
        api_key = "sk-test-key"
        tier = "tier-4"
        log_path = './var/logs/error.log'
        database_path = './var/data/agents.db'
    else:
        # Prompt user for settings
        api_key = input('Enter your OpenAI API key: ')
        tier = input('Enter your OpenAI tier level (e.g., tier-1): ')
        log_path = input('Enter the log directory path [default: ./var/logs/error.log]: ') or './var/logs/error.log'
        database_path = input('Enter the database path [default: ./var/data/agents.db]: ') or './var/data/agents.db'

    # Save settings to JSON file
    settings = {
        'openai_api_key': api_key,
        'tier': tier,
        'log_path': log_path,
        'database_path': database_path
    }
    os.makedirs('./config', exist_ok=True)
    with open('./config/settings.json', 'w') as f:
        json.dump(settings, f, indent=4)
    print('Settings saved to config/settings.json')


# Function to create the database structure

def create_database(db_path):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS models (
                    id INTEGER PRIMARY KEY,
                    model TEXT NOT NULL,
                    price_per_prompt_token REAL NOT NULL,
                    price_per_completion_token REAL NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS rate_limits (
                    id INTEGER PRIMARY KEY,
                    model TEXT NOT NULL,
                    tier TEXT NOT NULL,
                    rpm_limit INTEGER NOT NULL,
                    tpm_limit INTEGER NOT NULL,
                    rpd_limit INTEGER NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS api_usage (
                    id INTEGER PRIMARY KEY,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    session_id TEXT NOT NULL,
                    model TEXT NOT NULL,
                    prompt_tokens INTEGER NOT NULL,
                    completion_tokens INTEGER NOT NULL,
                    total_tokens INTEGER NOT NULL,
                    price_per_prompt_token REAL NOT NULL,
                    price_per_completion_token REAL NOT NULL,
                    total_cost REAL NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS chat_sessions (
                    id INTEGER PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                    end_time DATETIME)''')

    c.execute('''CREATE TABLE IF NOT EXISTS chats (
                    id INTEGER PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    chat_id TEXT NOT NULL,
                    message TEXT NOT NULL,
                    role TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

    # Insert default models and rate limits
    c.execute("INSERT INTO models (model, price_per_prompt_token, price_per_completion_token) VALUES ('gpt-4o-mini', 0.03, 0.06)")
    c.execute("INSERT INTO rate_limits (model, tier, rpm_limit, tpm_limit, rpd_limit) VALUES ('gpt-4o-mini', 'tier-1', 60, 50000, 1000)")

    conn.commit()
    conn.close()
    print(f"Database created at {db_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Setup script for installation.')
    parser.add_argument('--ci', action='store_true', help='Use default values for CI without prompting.')
    args = parser.parse_args()

    create_settings(ci_mode=args.ci)

    with open('./config/settings.json', 'r') as f:
        settings = json.load(f)

    create_database(settings['database_path'])
