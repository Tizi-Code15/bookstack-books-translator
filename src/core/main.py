import sys
import os
import json
import time

from core.logger import logger

# Ajouter le dossier 'src' au sys.path pour que Python puisse trouver les modules.
SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

# Imports des modules
from modules.user_management.users_id import get_users, save_users_to_json
from modules.user_management.create_users import create_user, save_created_users_to_json
from modules.role_management.roles_list import get_list_roles, save_list_roles_to_json
from modules.password_management.secure_password_input import ask_secure_password
from modules.recycle_management.recycle_bin import get_recycle, save_recycle_to_json
from modules.translation.English import run_translation as run_english_translation
from modules.translation.German import run_translation as run_german_translation
from modules.recycle_management.recycle_bin import save_recycle_to_json

# Importation de la fonction get_books_id
from modules.book_management.getbooksid import get_books_id


def user_manag():
    """
    Fonction de gestion des utilisateurs.
    Elle permet d'afficher les rôles, créer un utilisateur, et sauvegarder les infos.
    """
    list_roles = get_list_roles()
    if not list_roles:
        logger.error("No roles available.")
        return

    save_list_roles_to_json(list_roles)

    logger.info("Available roles list:")
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
        logger.error("No info to save.")

    users_data = get_users()
    if users_data:
        save_users_to_json(users_data)
    else:
        logger.error("No users to retrieve.")

def main():
    """
    Fonction principale qui dirige le programme selon le choix de l'utilisateur.
    """
    logger.info("Welcome to Medulla Verse")
    time.sleep(2)

    logger.info("What would you like to do?")
    logger.info("- Translate")
    logger.info("- Manage users")
    logger.info("- Manage Recycle Bin")
    time.sleep(2)

    logger.info("Press 'T' to Translate, 'U' for User Manage, 'R' for Recycle Bin")
    choice = input("Enter your choice: ").strip().upper()

    if choice == "T":
        logger.info("You have chosen translation.")

        books = get_books_id()  # Appel de la fonction correctement importée
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
        logger.info("You have chosen to manage the Recycle Bin.")
        recycle_data = get_recycle()
        if recycle_data:
            save_recycle_to_json(recycle_data)
        else:
            logger.error("No items found in the recycle bin.")

    else:
        logger.error("The choice does not correspond.")

if __name__ == "__main__":
    main()
