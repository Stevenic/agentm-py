import os
import json
import logging
from datetime import datetime

class Logger:
    """
    A logger class that handles logging messages to a file and the console.

    Attributes:
        settings (dict): A dictionary containing settings loaded from a JSON file.
        logger (logging.Logger): An instance of Python's standard logging.Logger.

    Methods:
        load_settings(settings_path): Loads settings from a specified JSON file.
        info(message): Logs an informational message.
        error(message): Logs an error message.
    """

    def __init__(self, settings_path=None):
        """
        Constructs the Logger object and initializes the logging configuration.

        Args:
            settings_path (str): The path to the settings JSON file.
        """
        if settings_path is None:
            settings_path = os.path.join(os.path.dirname(__file__), '../../config/settings.json')
        self.settings = self.load_settings(settings_path)
        log_file_path = self.settings.get('log_path', './var/logs/error.log')
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        logging.basicConfig(filename=log_file_path, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger()

    def load_settings(self, settings_path):
        """
        Loads settings from a JSON file.

        Args:
            settings_path (str): The path to the settings JSON file.

        Returns:
            dict: A dictionary containing the settings.
        """
        if not os.path.exists(settings_path):
            raise FileNotFoundError(f"Settings file not found at {settings_path}")
        with open(settings_path, 'r') as f:
            return json.load(f)

    def info(self, message):
        """
        Logs an informational message.

        Args:
            message (str): The message to log.
        """
        print(message)
        self.logger.info(message)

    def error(self, message):
        """
        Logs an error message.

        Args:
            message (str): The message to log.
        """
        print(message)
        self.logger.error(message)
