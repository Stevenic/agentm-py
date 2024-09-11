import logging
import json
import os


class Logger:
    def __init__(self, settings_path="../config/settings.json"):
        self.settings = self.load_settings(settings_path)
        self.log_path = self.settings["log_path"]
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        logging.basicConfig(
            filename=self.log_path,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )

    def load_settings(self, settings_path):
        try:
            with open(settings_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            raise Exception(f"Settings file not found at {settings_path}")
        except KeyError as e:
            raise Exception(f"Missing key in settings: {e}")

    def info(self, message):
        logging.info(message)
        print(message)

    def error(self, message):
        logging.error(message)
        print(f"ERROR: {message}")
