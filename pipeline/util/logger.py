import logging
from logging.handlers import RotatingFileHandler
import os
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env

LOG_PATH = os.getenv("LOG_HEAD") # top level logging directory
LOG_LEVEL = os.getenv("LOG_LEVEL")

def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger instance.
    """

    log_dir = LOG_PATH
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger(name)

    level = getattr(logging, LOG_LEVEL, logging.INFO)
    logger.setLevel(level)

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        # File handler (rotating)
        file_handler = RotatingFileHandler(
            f"{log_dir}/pipeline.log",
            maxBytes=10_000_000,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
