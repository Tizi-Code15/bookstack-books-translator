import requests, json, os, sys

from core.config import URL, TOKEN
from core.logger import logger  #

# Add the parent folder to sys.path so that Python can find the modules.

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Define the headers for HTTP requests

headers = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json"
}

def get_list_roles():
    try:
        logger.info("Sending the request to retrieve the roles from the API.")  
        # Sending the GET request
        response = requests.get(f"{URL}/api/roles", headers=headers)
        response.raise_for_status()  # Check if the response is valid (status code 200)

        # Check if the response contains data under the "data" key
        list_roles = response.json().get("data", [])
        
        if not isinstance(list_roles, list):
            logger.warning("Incorrect roles format. Expected a list of roles.")
            return []

        if list_roles:
            logger.info(f"{len(list_roles)} Roles retrieved successfully.")  # Log succès
        else:
            logger.warning("No roles found in the response.")  

        return list_roles
    except requests.exceptions.RequestException as e:
        logger.error(f"Error while retrieving the roles: {e}")  # Log erreur
        return []

def save_list_roles_to_json(list_info):
    if not list_info:
        logger.warning("No roles to save.")  # Log si aucune donnée à sauvegarder
        return

    # Path to the "src/data/Role_Data" folder
    medulla_verse = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..'))
    data_dir = os.path.join(medulla_verse, 'data', 'Role_Data')

    # Créer le répertoire si nécessaire
    os.makedirs(data_dir, exist_ok=True)

    # Chemin complet vers le fichier JSON
    file_path = os.path.join(data_dir, 'list_info.json')

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(list_info, f, indent=4, ensure_ascii=False)
        logger.info("The roles have been successfully saved.")  # Log succès
    except Exception as e:
        logger.error(f"Error while saving the roles: {e}")  # Log erreur
