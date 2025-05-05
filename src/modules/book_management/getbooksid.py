import requests
import json
import os
import sys

from core.config import URL, TOKEN
from core.logger import logger

# Déterminer le dossier racine du projet
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, '..', '..'))  # <- pour aller jusqu'à 'src'

# S'assurer que 'src' est dans le sys.path
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# Configuration des headers pour l'API BookStack
HEADERS = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json"
}

def get_books_id():
    """
    Récupère la liste des livres depuis l'API BookStack.
    Retourne une liste contenant les informations des livres.
    """
    try:
        logger.info("Envoi de la requête pour récupérer les livres depuis l'API.")
        response = requests.get(f"{URL}/api/books", headers=HEADERS)
        response.raise_for_status()
        books_id = response.json().get("data", [])
        logger.info(f"{len(books_id)} livres récupérés avec succès.")
        return books_id
    except requests.exceptions.RequestException as e:
        logger.error(f"Erreur lors de la récupération des livres : {e}")
        return []

def save_books_info_to_json(books_info):
    """
    Sauvegarde les données des livres dans un fichier JSON
    dans le dossier 'src/data/Books_Data/'.
    """
    if not books_info:
        logger.warning("Aucun livre à sauvegarder.")
        return

    # Dossier cible pour la sauvegarde
    data_dir = os.path.join(PROJECT_ROOT, 'data', 'Books_Data')
    os.makedirs(data_dir, exist_ok=True)

    file_path = os.path.join(data_dir, "book_ids.json")

    try:
        logger.info(f"Sauvegarde de {len(books_info)} livres dans 'book_ids.json'.")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(books_info, f, indent=4, ensure_ascii=False)
        logger.info("Les livres ont été sauvegardés avec succès.")
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde des livres : {e}")
