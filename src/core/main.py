# src/core/main.py
import sys, os

# Ajouter le dossier 'src' au sys.path pour que Python puisse trouver les modules.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json, time, logging

from modules.user_management.users_id import get_users, save_users_to_json
from modules.user_management.create_users import create_users, save_created_users_to_json
from modules.role_management.roles_list import get_list_roles, save_list_roles_to_json
from modules.password_management.secure_password_input import ask_secure_password
from modules.recycle_management.recycle_bin import get_recycle, save_recycle_to_json

# Directly import the English and German translation modules
from modules.translation.English import run_translation as run_english_translation
from modules.translation.German import run_translation as run_german_translation
from modules.book_management.getbooksid import get_books_id, save_books_info_to_json

# Import the logging module you created
from core.logger import logger

def user_manag():
    list_roles = get_list_roles()
    if not list_roles:
        logger.error("No roles available.")  # Log error if no roles are available
        return

    save_list_roles_to_json(list_roles)

    logger.info("\nAvailable roles list:")  # Log the list of available roles
    for role in list_roles:
        logger.info(f"{role['id']} : {role['display_name']}")  # Log each role

    logger.info("\nPlease enter profile information:")
    name = input("Name: ")
    email = input("Email: ")
    password = ask_secure_password()
    role_id = int(input("Choose the role: "))

    users_info = create_users(name, email, password, roles=[role_id])
    if users_info:
        save_created_users_to_json(users_info)
    else:
        logger.error("No info to save.")  # Log error if there is no info to save

    users_data = get_users()
    if users_data:
        save_users_to_json(users_data)
    else:
        logger.error("No users to retrieve.")  # Log error if no users are retrieved

def main():
    logger.info("Welcome to Medulla Verse")  # Log the welcome message
    time.sleep(2)

    logger.info("\nWhat would you like to do?")  # Log available actions
    logger.info("- Translate")
    logger.info("- Manage users")
    logger.info("- Manage Recycle Bin")
    time.sleep(2)

    logger.info("\nPress 'T' to Translate, 'U' for User Manage, 'R' for Recycle Bin")
    choice = input("Enter your choice: ").strip().upper()

    if choice == "T":
        logger.info("\nYou have chosen translation")  # Log translation choice

        # Retrieve available books from the API
        books = get_books_id()
        if not books:
            logger.error("No books found.")  # Log error if no books are found
            return

        # Display the list of available books with their IDs
        logger.info("\nList of available books:")  # Log the list of books
        for book in books:
            logger.info(f"{book['id']} : {book['name']}")  # Log each book

        # Ask the user to choose a book by its ID
        try:
            selected_id = int(input("\nEnter the ID of the book to translate: "))
            if not any(b['id'] == selected_id for b in books):
                logger.error("Invalid ID.")  # Log error if the ID is invalid
                return
        except ValueError:
            logger.error("Invalid input.")  # Log error if the input is invalid
            return  

        # Choose the language
        logger.info("\nChoose a language:")  # Log the language selection prompt
        logger.info("1 - English")
        logger.info("2 - German")
        lang_choice = input("Enter the number: ").strip()

        if lang_choice == "1":
            logger.info("Translating to English...")  # Log language choice for English
            run_english_translation(selected_id)  # Call the English translation function
        elif lang_choice == "2":
            logger.info("Translating to German...")  # Log language choice for German
            run_german_translation(selected_id)   # Call the German translation function
        else:
            logger.error("Invalid language selection.")  # Log error for invalid language choice

    elif choice == "U":
        logger.info("\nYou have chosen user management.\n")  # Log user management choice
        user_manag()
    elif choice == "R":
        logger.info("\nYou have chosen to manage the Recycle Bin.")  # Log recycle bin choice

        # Retrieve and save items from the recycle bin
        recycle_data = get_recycle()
        if recycle_data:
            save_recycle_to_json(recycle_data)
        else:
            logger.error("No items found in the recycle bin.")  # Log if no items were found in the recycle bin

    else:
        logger.error("The choice does not correspond.")  # Log error if the choice does not match

if __name__ == "__main__":
    main()
