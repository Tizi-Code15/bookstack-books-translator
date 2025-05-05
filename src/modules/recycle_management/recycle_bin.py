import requests
import json
import os
import sys
from core.config import URL, TOKEN
from core.logger import logger  # Importation du logger

# Ajouter le dossier parent au sys.path pour que Python puisse trouver les modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Définir les headers pour les requêtes HTTP
headers = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json"
}

def get_recycle():
    """ Récupère les éléments de la corbeille depuis l'API """
    try:
        logger.info("Envoi de la requête pour récupérer la corbeille depuis l'API.")  # Log avant la requête
        response = requests.get(f"{URL}/api/recycle-bin", headers=headers)
        response.raise_for_status()  # Vérification du succès de la réponse
        logger.info(f"Réponse de l'API réussie, statut : {response.status_code}")  # Log succès
        recycle = response.json().get("data", [])
        return recycle
    except requests.exceptions.RequestException as e:
        logger.error(f"Erreur lors de la récupération de la corbeille : {e}")  # Log erreur
        return []

def save_recycle_to_json(recycle_data):
    """
    Sauvegarde les éléments de la corbeille dans un fichier JSON.
    """
    if not recycle_data:
        logger.warning("Aucune donnée à sauvegarder.")
        return

    # Créer un dossier pour stocker les données de la corbeille (si nécessaire)
    medulla_verse = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    data_dir = os.path.join(medulla_verse, 'data', 'Recycle_Data') 
    os.makedirs(data_dir, exist_ok=True)

    # Le chemin du fichier JSON
    file_path = os.path.join(data_dir, 'recycle_data.json')

    try:
        logger.info(f"Sauvegarde de {len(recycle_data)} éléments dans 'recycle_data.json'.")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(recycle_data, f, indent=4, ensure_ascii=False)
        logger.info("Les données de la corbeille ont été sauvegardées avec succès.")
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde des données de la corbeille : {e}")