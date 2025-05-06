import logging
import os

# Define log folder paths
LOG_DIR = 'logs'
INFO_LOG_DIR = os.path.join(LOG_DIR, 'info')
ERROR_LOG_DIR = os.path.join(LOG_DIR, 'error')

# Create the log directories if they do not exist
os.makedirs(INFO_LOG_DIR, exist_ok=True)
os.makedirs(ERROR_LOG_DIR, exist_ok=True)

# Full paths for log files
INFO_LOG_FILE = os.path.join(INFO_LOG_DIR, 'info.log')
ERROR_LOG_FILE = os.path.join(ERROR_LOG_DIR, 'error.log')

# Create the logger
logger = logging.getLogger('medulla_logger')
logger.setLevel(logging.DEBUG)  # Log everything from DEBUG to CRITICAL (for files)

# Handler for INFO messages and above in log files (info.log and error.log)
file_handler = logging.FileHandler(INFO_LOG_FILE, mode='a', encoding='utf-8')
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Handler for ERROR messages and above in error log files (error.log)
error_handler = logging.FileHandler(ERROR_LOG_FILE, mode='a', encoding='utf-8')
error_handler.setLevel(logging.ERROR)  # Capture only errors
error_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
error_handler.setFormatter(error_formatter)

# Handler to display logs in the console without date/time
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Display logs from INFO level in the console
console_formatter = logging.Formatter('%(levelname)s - %(message)s')  # No date/time
console_handler.setFormatter(console_formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(error_handler)
logger.addHandler(console_handler)
