import requests, json, os, sys

from core.config import URL, TOKEN
from core.logger import logger  

# Add the parent folder to sys.path so that Python can find the modules

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Define the headers for HTTP requests
headers = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json"
}

def get_recycle():
    # Retrieves the trash items from the API
    try:
        logger.info("Sending the request to retrieve the trash from the API.")  # Log avant la requête
        response = requests.get(f"{URL}/api/recycle-bin", headers=headers)
        response.raise_for_status()  # Checking the success of the response
        logger.info(f"Réponse de l'API réussie, statut : {response.status_code}")  # Log succès
        recycle = response.json().get("data", [])
        return recycle
    except requests.exceptions.RequestException as e:
        logger.error(f"Error while retrieving the trash: {e}")  # Log erreur
        return []

def save_recycle_to_json(recycle_data):
    # Saves the trash items to a JSON file.
    if not recycle_data:
        logger.warning("No data to save.")
        return

    # Create a folder to store the trash data

    medulla_verse = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    data_dir = os.path.join(medulla_verse, 'data', 'Recycle_Data') 
    os.makedirs(data_dir, exist_ok=True)

    # The path of the JSON file

    file_path = os.path.join(data_dir, 'recycle_data.json')

    try:
        logger.info(f"Saving {len(recycle_data)} Saving items to 'recycle_data.json'.")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(recycle_data, f, indent=4, ensure_ascii=False)
        logger.info("The trash data has been successfully saved.")
    except Exception as e:
        logger.error(f"Error while saving the trash data: {e}")