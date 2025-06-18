# core/logger.py

import logging
import os

def setup_logger():
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO"),
        format="%(asctime)s - %(levelname)s - %(module)s - %(message)s",
        handlers=[
            logging.FileHandler("logs/chatbot.log"),
            logging.StreamHandler()
        ]
    )