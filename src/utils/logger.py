import logging
import datetime
from pathlib import Path
from src.utils.exception import CustomException


class CustomLogger:
    def __init__(self, name):
        self.name = name
        self.formatter = logging.Formatter(
            "[%(asctime)s] %(name)s - %(levelname)s - %(message)s"
        )
        
        log_dir = Path(__file__).resolve().parent.parent.parent / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file_name = f"{datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.log"
        log_file_path = log_dir / log_file_name

        self.file_handler = logging.FileHandler(log_file_path)
        self.file_handler.setFormatter(self.formatter)

        # Create the logger instance
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(self.file_handler)

    def info(self, message):
        self.logger.info(message)
    
    def error(self, message):
        self.logger.error(message)

    def log_custom_exception(self, error_message, error_details):
        custom_exception = CustomException(error_message, error_details)
        self.logger.error(custom_exception)