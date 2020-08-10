import logging
from datetime import datetime

class LogHelper:
    def __init__(self):
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(level = logging.INFO)
        today_date = datetime.today().strftime('%Y%m%d')
        handler = logging.FileHandler(f"logs/{today_date}_log.txt")
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.__logger.addHandler(handler)
    
    
    @property
    def logger(self):
        return self.__logger 