import requests
import json
import os
import sys
from core.config import URL, TOKEN
from core.logger import logger  # Importation du logger

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# En-têtes pour les requêtes API
headers = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json"
}

def get_users():
    """Récupère la liste des utilisateurs depuis l'API."""
    try:
        logger.info("Envoi de la requête pour récupérer les utilisateurs depuis l'API.")
        response = requests.get(f"{URL}/api/users", headers=headers)
        response.raise_for_status()  # Vérifie que la requête a réussi
        
        # Traitement des utilisateurs renvoyés par l'API
        users_list = response.json().get("data", [])
        logger.info(f"{len(users_list)} utilisateurs récupérés.")
        return users_list
    except requests.exceptions.RequestException as e:
        # Log détaillé de l'erreur
        logger.error(f"Erreur lors de la récupération des utilisateurs : {e}")
        return []

def save_users_to_json(users):
    """Sauvegarde les utilisateurs récupérés dans un fichier JSON."""
    if not users:
        logger.warning("Aucun utilisateur à sauvegarder.")
        return
    
    # Définir le répertoire et le chemin du fichier de sauvegarde
    medulla_verse = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    data_dir = os.path.join(medulla_verse, 'data', 'User_Data')
    os.makedirs(data_dir, exist_ok=True)  # Créer le répertoire si nécessaire
    
    file_path = os.path.join(data_dir, 'users_data.json')
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4, ensure_ascii=False)
        logger.info("Les données des utilisateurs ont été sauvegardées avec succès.")
    except Exception as e:
        # Log détaillé de l'erreur de sauvegarde
        logger.error(f"Erreur lors de la sauvegarde des utilisateurs dans le fichier {file_path}: {e}")

