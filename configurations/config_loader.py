from yaml import safe_load
from utils.logger import Logger

class ConfigLoader:
    def __init__(self, logger) -> None:
        self.logger = Logger() if logger is None else logger
    
    def load(self, filename='./configurations/configuration.yaml'):
        with open(filename) as f:
            configuration = safe_load(f)
            self.logger.info("Configuration loaded.")
            return configuration