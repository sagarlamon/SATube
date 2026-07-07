import logging
from logging.handlers import RotatingFileHandler
from satube.config import LOG_DIR

def _setup_logger(name: str = "satube") -> logging.Logger:
    """
    Configures and returns a logger that writes to a rotating file.
    Prevents logs from polluting the terminal UI.
    """
    logger = logging.getLogger(name)
    
    # Prevent adding multiple handlers if initialized more than once
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)
        
        # Define log file path
        log_file = LOG_DIR / "satube.log"
        
        # Use a rotating file handler: max 5MB per file, keeping up to 3 backups
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=5 * 1024 * 1024, 
            backupCount=3, 
            encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        
        # Create a professional format for the logs
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(module)s:%(lineno)d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        
    return logger

# Global logger instance to be imported across the application
logger = _setup_logger()