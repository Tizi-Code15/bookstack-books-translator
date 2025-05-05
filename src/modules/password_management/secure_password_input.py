import getpass
import re
from core.logger import logger  # Import the logger setup from logger.py

def ask_secure_password():
    while True:
        password = getpass.getpass("Enter your password: ")
        confirm = getpass.getpass("Confirm your password: ")

        # Check if passwords match
        if password != confirm:
            logger.warning("Passwords do not match. User tried again.")  # Log the warning when passwords don't match
            print("Passwords do not match. Try again.")
            continue 

        # Check password strength
        if not validate_password_caract(password):
            logger.warning("Password too weak. User tried again.")  # Log the warning when the password is too weak
            print("Password too weak. Must be at least 8 characters, with uppercase, lowercase, number, and symbol.")
            continue
        
        logger.info("Password set successfully.")  # Log the successful password setting
        return password

def validate_password_caract(pwd):
    is_valid = (
        len(pwd) >= 8 and
        re.search(r"[A-Z]", pwd) and
        re.search(r"[a-z]", pwd) and
        re.search(r"\d", pwd) and
        re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", pwd)
    )
    if not is_valid:
        logger.warning("Password does not meet the required criteria.")  # Log invalid password if it doesn't meet criteria
    return is_valid
