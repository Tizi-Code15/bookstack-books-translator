import sys, json, time, os

from core.logger import logger

# Add the 'src' folder to sys.path so Python can find the modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import modules
from modules.user_management.users_id import get_users, save_users_to_json
from modules.user_management.create_users import create_user, save_created_users_to_json
from modules.role_management.roles_list import get_list_roles, save_list_roles_to_json
from modules.password_management.secure_password_input import ask_secure_password
from modules.recycle_management.recycle_bin import get_recycle, save_recycle_to_json
from modules.translation.English import run_translation as run_english_translation
from modules.translation.German import run_translation as run_german_translation
from modules.recycle_management.recycle_bin import save_recycle_to_json
from modules.book_management.getbooksid import get_books_id


def user_manag():
    
    # User management function.
    # Allows viewing roles, creating a user, and saving information.
    
    list_roles = get_list_roles()
    if not list_roles:
        logger.error("No roles available.")
        return

    save_list_roles_to_json(list_roles)

    logger.info("List of available roles:")
    for role in list_roles:
        logger.info(f"{role['id']} : {role['display_name']}")

    logger.info("Please enter profile information:")
    name = input("Name: ")
    email = input("Email: ")
    password = ask_secure_password()

    try:
        role_id = int(input("Choose the role: "))
    except ValueError:
        logger.error("Invalid role ID.")
        return

    users_info = create_user(name, email, password, roles=[role_id])
    if users_info:
        save_created_users_to_json(users_info)
    else:
        logger.error("No information to save.")

    users_data = get_users()
    if users_data:
        save_users_to_json(users_data)
    else:
        logger.error("No users to retrieve.")


def main():
    
    #Main function that directs the program according to the user's choice.
   
    logger.info("Welcome to Medulla Verse")
    time.sleep(2)

    logger.info("What would you like to do?")
    logger.info("- Translate")
    logger.info("- Manage users")
    logger.info("- Manage the recycle bin")
    time.sleep(2)

    logger.info("Press 'T' for Translation, 'U' for User Management, 'R' for Recycle Bin")
    choice = input("Enter your choice: ").strip().upper()

    if choice == "T":
        logger.info("You have chosen translation.")

        books = get_books_id()  # Calling the properly imported function
        if not books:
            logger.error("No books found.")
            return

        logger.info("List of available books:")
        for book in books:
            logger.info(f"{book['id']} : {book['name']}")

        try:
            selected_id = int(input("Enter the ID of the book to translate: "))
            if not any(b['id'] == selected_id for b in books):
                logger.error("Invalid ID.")
                return
        except ValueError:
            logger.error("Invalid input.")
            return

        logger.info("Choose a language:")
        logger.info("1 - English")
        logger.info("2 - German")
        lang_choice = input("Enter the number: ").strip()

        if lang_choice == "1":
            logger.info("Translating to English...")
            run_english_translation(selected_id)
        elif lang_choice == "2":
            logger.info("Translating to German...")
            run_german_translation(selected_id)
        else:
            logger.error("Invalid language selection.")

    elif choice == "U":
        logger.info("You have chosen user management.")
        user_manag()

    elif choice == "R":
        logger.info("You have chosen to manage the recycle bin.")
        recycle_data = get_recycle()
        if recycle_data:
            save_recycle_to_json(recycle_data)
        else:
            logger.error("No items found in the recycle bin.")

    else:
        logger.error("The choice does not correspond.")

if __name__ == "__main__":
    main()
