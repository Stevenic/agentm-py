import os
import json
import argparse

# Function to create config/settings.json

def create_settings(ci_mode=False):
    if ci_mode:
        # Use default values for CI
        api_key = "sk-test-key"
        log_path = './var/logs/error.log'
    else:
        # Prompt user for settings
        api_key = input('Enter your OpenAI API key: ')
        log_path = input('Enter the log directory path [default: ./var/logs/error.log]: ') or './var/logs/error.log'

    # Save settings to JSON file
    settings = {
        'openai_api_key': api_key,
        'log_path': log_path
    }
    os.makedirs('./config', exist_ok=True)
    with open('./config/settings.json', 'w') as f:
        json.dump(settings, f, indent=4)
    print('Settings saved to config/settings.json')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Setup script for installation.')
    parser.add_argument('--ci', action='store_true', help='Use default values for CI without prompting.')
    args = parser.parse_args()

    create_settings(ci_mode=args.ci)
