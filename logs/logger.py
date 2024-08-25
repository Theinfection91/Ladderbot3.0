import logging
from logging.handlers import RotatingFileHandler
import os

# Directory for logs
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Log file path
log_file = os.path.join(log_dir, 'ladderbot.log')

# Create a logger instance
logger = logging.getLogger('LadderLogs')

# Set the desired log level
logger.setLevel(logging.DEBUG) 

# Remove all existing handlers
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# Create a RotatingFileHandler
rotating_handler = RotatingFileHandler(
    log_file,                # Log file path
    maxBytes=5*1024*1024,    # Max file size in bytes (5 MB)
    backupCount=5            # Number of backup files to keep
)

# Set the handler level
rotating_handler.setLevel(logging.DEBUG)

# Create a formatter and set it for the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
rotating_handler.setFormatter(formatter)

# Add the rotating file handler to the logger
logger.addHandler(rotating_handler)