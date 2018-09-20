import logging
import os 

class Logger:

    def __init__(self):
        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(format=format)
        self.ch = logging.StreamHandler()

    def get_logger(self, clazz):
        logger = logging.getLogger(clazz)
        logger.setLevel(os.getenv("LOG_LEVEL", logging.INFO))
        return logger
