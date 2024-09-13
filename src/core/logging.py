import os
import json
import logging
from datetime import datetime

class Logger:
    def __init__(self, settings_path=None):
        if settings_path is None:
            settings_path = os.path.join(os.path.dirname(__file__), '../../config/settings.json')
        self.settings = self.load_settings(settings_path)
        log_file_path = self.settings.get('log_path', './var/logs/error.log')
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        logging.basicConfig(filename=log_file_path, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger()

    def load_settings(self, settings_path):
        if not os.path.exists(settings_path):
            raise FileNotFoundError(f"Settings file not found at {settings_path}")
        with open(settings_path, 'r') as f:
            return json.load(f)

    def info(self, message):
        print(message)
        self.logger.info(message)

    def error(self, message):
        print(message)
        self.logger.error(message)
