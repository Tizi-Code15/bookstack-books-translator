# logger.py
import logging
import os

# Create directories for logs if they don't exist
log_dir = 'logs'
info_log_dir = os.path.join(log_dir, 'info')
error_log_dir = os.path.join(log_dir, 'error')
password_log_dir = os.path.join(log_dir, 'password_logs')  # New directory for password logs

os.makedirs(info_log_dir, exist_ok=True)
os.makedirs(error_log_dir, exist_ok=True)
os.makedirs(password_log_dir, exist_ok=True)  # Create password_logs directory

# Set up the logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Create an info log handler
info_file_path = os.path.join(info_log_dir, 'info.log')
info_handler = logging.FileHandler(info_file_path, mode='a', encoding='utf-8')
info_handler.setLevel(logging.INFO)
info_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
info_handler.setFormatter(info_formatter)

# Create an error log handler
error_file_path = os.path.join(error_log_dir, 'error.log')
error_handler = logging.FileHandler(error_file_path, mode='a', encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
error_handler.setFormatter(error_formatter)

# Create a password log handler
password_log_file_path = os.path.join(password_log_dir, 'password_log.txt')  # Log file for password activities
password_handler = logging.FileHandler(password_log_file_path, mode='a', encoding='utf-8')
password_handler.setLevel(logging.INFO)  # Set level to INFO for password activities
password_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
password_handler.setFormatter(password_formatter)

# Add handlers to the logger
logger.addHandler(info_handler)
logger.addHandler(error_handler)
logger.addHandler(password_handler)

# Create a console handler for real-time logs
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)
