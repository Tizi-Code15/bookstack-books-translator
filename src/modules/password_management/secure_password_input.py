import getpass
import re
from core.logger import logger  

def ask_secure_password():
    # Asks the user to enter and confirm their password.
    while True:
        password = getpass.getpass("Enter your password:")
        confirm = getpass.getpass("Confirm your password:")

        if password != confirm:
            log_and_print_error("The passwords do not match.")
            continue

        if not validate_password_caract(password):
            log_and_print_error("Password too weak. It must contain at least 8 characters, an uppercase letter, a lowercase letter, a number, and a symbol.")
            continue
        
        logger.info("Password set successfully.")
        return password

def validate_password_caract(pwd):
    # Validates the password by checking its length, uppercase letters, lowercase letters, numbers, and symbols.

    is_valid = (
        len(pwd) >= 8 and
        re.search(r"[A-Z]", pwd) and
        re.search(r"[a-z]", pwd) and
        re.search(r"\d", pwd) and
        re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", pwd)
    )
    
    if not is_valid:
        logger.warning("Le mot de passe ne respecte pas les critères requis.")
    return is_valid

# Logs an error message and displays it to the user.
def log_and_print_error(message):
    logger.warning(message)
    print(message)
