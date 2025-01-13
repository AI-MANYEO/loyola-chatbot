import logging
import os

def setup_logger(name="app_logger", log_file="app.log", level=logging.INFO):
    """Set up a logger with a file and console handler."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Formatter 설정
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # File Handler
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


# 사용 예시
logger = setup_logger("loyola_chatbot")
logger.info("Logger initialized.")