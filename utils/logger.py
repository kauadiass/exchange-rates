
import logging
import os
from datetime import datetime


LOG_DIR = "logs"

LOG_FILE_NAME = datetime.now().strftime("app_%Y-%m-%d_%H-%M-%S.log")
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE_NAME)


os.makedirs(LOG_DIR, exist_ok=True)

def setup_logging():
    
    logger = logging.getLogger(__name__) 
    logger.setLevel(logging.DEBUG) 

    if not logger.handlers:
        
        console_handler = logging.StreamHandler()
        
        console_handler.setLevel(logging.INFO) 
        
        
        file_handler = logging.FileHandler(LOG_FILE_PATH, encoding='utf-8')
        
        file_handler.setLevel(logging.DEBUG) 

        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )

        
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(file_formatter)

        
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    return logger

logger = setup_logging()