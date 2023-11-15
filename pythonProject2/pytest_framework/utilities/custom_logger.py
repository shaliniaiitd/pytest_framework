import logging
import os
from logging.handlers import RotatingFileHandler

class Logger:
    def __init__(self, log_file_path, log_level=logging.INFO):
        self.logger = logging.getLogger("test_logger")
        self.logger.setLevel(log_level)

        log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] - %(message)s")

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        self.logger.addHandler(console_handler)

        if log_file_path:
            os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
            log_file_handler = RotatingFileHandler(log_file_path, maxBytes=1024 * 1024, backupCount=3)
            log_file_handler.setFormatter(log_formatter)
            self.logger.addHandler(log_file_handler)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)

    def debug(self, message):
        self.logger.debug(message)