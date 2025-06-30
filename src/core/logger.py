# logger
import logging
import os

# logs folder
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
LOG_DIR = os.path.join(PROJECT_ROOT, 'logs')
ERROR_LOG_DIR = os.path.join(LOG_DIR, 'error')

# Create the error log directory if it does not exist
os.makedirs(ERROR_LOG_DIR, exist_ok=True)

# Full path for error log file
ERROR_LOG_FILE = os.path.join(ERROR_LOG_DIR, 'error.log')

# Create the logger
logger = logging.getLogger('applogger')
logger.setLevel(logging.DEBUG)

# Handler for ERROR messages and above in error log files (error.log)
error_handler = logging.FileHandler(ERROR_LOG_FILE, mode='a', encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
error_handler.setFormatter(error_formatter)

# Handler to display logs in the console without date/time
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

# Add handlers to the logger
if not logger.hasHandlers():
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)
