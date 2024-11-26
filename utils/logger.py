import logging
import logging.config
from config import Config

def setup_logger(name):
    """
    Set up and return a logger instance with the specified name
    
    Args:
        name (str): Name of the logger, typically __name__ of the module
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logging.config.dictConfig(Config.LOGGING_CONFIG)
    logger = logging.getLogger(name)
    return logger
