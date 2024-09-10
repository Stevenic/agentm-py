# Installation Guide for `agentm-py`

This guide walks you through setting up `agentm-py`, configuring it with your OpenAI API key, and setting up logging and the SQLite database.

## 1. Clone the Repository
First, clone the repository to your local machine:

```bash
# Clone the repository
git clone https://github.com/Stevedic/agentm-py.git
cd agentm-py
```

## 2. Set Up a Virtual Environment
Set up and activate a virtual environment using `pipenv` or `venv`:

### Using `pipenv`:
```bash
pipenv install
pipenv shell
```

### Using `venv`:
```bash
python -m venv venv-py312
source venv-py312/bin/activate  # On Windows: venv-py312\Scripts\activate
pip install -r requirements.txt
```

## 3. Run the `install.py` Script
The `install.py` script will prompt you for necessary configuration, such as the OpenAI API key and log locations. It will also create the database and logs directories.

Run the script:

```bash
python install.py
```

### During installation, you will be asked to provide:
1. **OpenAI API Key**: This key will be stored in the `config/settings.json` file.
2. **Log Directory**: By default, logs will be stored under `./var/logs`.
3. **Database Directory**: The SQLite database (`agents.db`) will be created in `./var/data`.

## 4. Directory Structure Before Running `install.py`

Before running the installation script, the project directory structure will look like this:

```
agentm-py/
├── README.md
├── requirements.txt
├── Pipfile
├── LICENSE
├── .gitignore
├── Pipfile.lock
├── install.py
├── config/
│   └── __init__.py
├── core/
│   ├── database.py
│   ├── openai_api.py
│   ├── logging.py
│   ├── token_counter.py
│   ├── concurrency.py
│   ├── prompt_generation.py
│   ├── parallel_complete_prompt.py
│   ├── log_complete_prompt.py
│   ├── compose_prompt.py
│   └── __init__.py
├── tests/
│   ├── test_openai_api.py
│   ├── test_token_counter.py
│   ├── test_prompt_generation.py
│   ├── test_parallel_complete_prompt.py
│   ├── test_compose_prompt.py
│   ├── test_log_complete_prompt.py
│   └── test_database.py
├── src/
│   └── __init__.py
├── docs/
│   └── __init__.py
└── .github/
    └── workflows/
        └── ci.yml
```

## 5. Directory Structure After Running `install.py`

Once the installation is complete, the project directory structure will be updated to include log files and the SQLite database:

```
agentm-py/
├── README.md
├── requirements.txt
├── Pipfile
├── LICENSE
├── .gitignore
├── Pipfile.lock
├── install.py
├── config/
│   ├── settings.json
│   └── __init__.py
├── core/
│   ├── database.py
│   ├── openai_api.py
│   ├── logging.py
│   ├── token_counter.py
│   ├── concurrency.py
│   ├── prompt_generation.py
│   ├── parallel_complete_prompt.py
│   ├── log_complete_prompt.py
│   ├── compose_prompt.py
│   └── __init__.py
├── var/
│   ├── data/
│   │   └── agents.db
│   └── logs/
│       └── error.log
├── tests/
│   ├── test_openai_api.py
│   ├── test_token_counter.py
│   ├── test_prompt_generation.py
│   ├── test_parallel_complete_prompt.py
│   ├── test_compose_prompt.py
│   ├── test_log_complete_prompt.py
│   └── test_database.py
├── src/
│   └── __init__.py
├── docs/
│   └── __init__.py
└── .github/
    └── workflows/
        └── ci.yml
```

## 6. Configurations
Once installation is complete, a `settings.json` file will be created in the `config/` folder, which will store your configurations (like the OpenAI API key and log locations).

Example `settings.json`:
```json
{
    "openai_api_key": "sk-...",
    "log_path": "./var/logs/error.log",
    "database_path": "./var/data/agents.db"
}
```

## 7. Running Tests
To run the tests, use `pytest`:

```bash
pytest
```

Make sure to configure the necessary API keys and paths in the `config/settings.json` before running tests that interact with the OpenAI API.
