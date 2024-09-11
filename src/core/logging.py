import logging
import http.client
import json
import os

class Logger:
    def __init__(self, settings_path="../config/settings.json"):
        self.settings = self.load_settings(settings_path)
        self.log_path = self.settings["log_path"]
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        
        # Create a logger instance
        self.logger = logging.getLogger("AgentMLogger")
        self.logger.setLevel(logging.DEBUG if self.settings.get("debug", False) else logging.INFO)
        
        # File handler for logging to a file
        file_handler = logging.FileHandler(self.log_path)
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(file_handler)
        
        # Console handler for output to the console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(console_handler)
        
        # Enable HTTP-level logging if debug is enabled
        if self.settings.get("debug", False):
            self.enable_http_debug()

    def load_settings(self, settings_path):
        if not os.path.exists(settings_path):
            raise FileNotFoundError(f"Settings file not found at {settings_path}")
        with open(settings_path, "r") as f:
            return json.load(f)

    def enable_http_debug(self):
        """Enable HTTP-level logging for API communication."""
        http.client.HTTPConnection.debuglevel = 1
        logging.getLogger("http.client").setLevel(logging.DEBUG)
        logging.getLogger("http.client").propagate = True

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)
        print(f"ERROR: {message}")
