import requests
import json
import os
import sys
from core.config import URL, TOKEN
from core.logger import logger  # Importation du logger

# Ajouter le dossier parent au sys.path pour que Python puisse trouver les modules.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Définir les headers pour les requêtes HTTP
headers = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json"
}

def get_list_roles():
    try:
        logger.info("Envoi de la requête pour récupérer les rôles depuis l'API.")  # Log avant la requête
        # Envoi de la requête GET
        response = requests.get(f"{URL}/api/roles", headers=headers)
        response.raise_for_status()  # Vérifier si la réponse est valide (code 200)

        # Vérifier si la réponse contient des données sous la clé "data"
        list_roles = response.json().get("data", [])
        
        if not isinstance(list_roles, list):
            logger.warning("Format des rôles incorrect. Attendu une liste de rôles.")
            return []

        if list_roles:
            logger.info(f"{len(list_roles)} rôles récupérés avec succès.")  # Log succès
        else:
            logger.warning("Aucun rôle trouvé dans la réponse.")  # Log si aucun rôle trouvé

        return list_roles
    except requests.exceptions.RequestException as e:
        logger.error(f"Erreur lors de la récupération des rôles : {e}")  # Log erreur
        return []

def save_list_roles_to_json(list_info):
    if not list_info:
        logger.warning("Aucun rôle à sauvegarder.")  # Log si aucune donnée à sauvegarder
        return

    # Chemin vers le dossier "src/data/Role_Data"
    medulla_verse = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..'))
    data_dir = os.path.join(medulla_verse, 'data', 'Role_Data')

    # Créer le répertoire si nécessaire
    os.makedirs(data_dir, exist_ok=True)

    # Chemin complet vers le fichier JSON
    file_path = os.path.join(data_dir, 'list_info.json')

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(list_info, f, indent=4, ensure_ascii=False)
        logger.info("Les rôles ont été sauvegardés avec succès.")  # Log succès
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde des rôles : {e}")  # Log erreur
