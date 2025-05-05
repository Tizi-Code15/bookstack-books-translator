import requests
import json
import os
import sys
from core.config import URL, TOKEN
from core.logger import logger  # Importation du logger

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configuration des en-têtes pour les requêtes API
headers = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json"
}

def create_user(name, email, password, roles=None):
    """Crée un utilisateur via l'API."""
    if roles is None:
        roles = []
    
    data = {
        "name": name,
        "email": email,
        "password": password,
        "roles": roles
    }
    
    try:
        # Log avant la requête
        logger.info(f"Envoi de la requête pour créer un utilisateur : {name} ({email})")
        response = requests.post(f"{URL}/api/users", headers=headers, json=data)
        response.raise_for_status()  # Vérifie le statut de la réponse
        
        # Extraction de l'utilisateur créé
        created_user = response.json()
        
        # Log de succès
        logger.info(f"Utilisateur créé avec succès : {created_user.get('name', 'Inconnu')} (ID: {created_user.get('id')})")
        return created_user
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Erreur lors de la création de l'utilisateur : {e}")  # Log d'erreur
        return None  # Retourne None en cas d'erreur

def save_created_users_to_json(users_info):
    """Sauvegarde les utilisateurs créés dans un fichier JSON."""
    if not users_info:
        logger.warning("Aucun utilisateur à sauvegarder.")  # Log si aucune donnée à sauvegarder
        return
    
    # Définir le répertoire de sauvegarde pour les utilisateurs créés
    # Correction ici pour enregistrer dans 'data/User_Data' sans ajouter 'src/'
    medulla_verse = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    data_dir = os.path.join(medulla_verse, 'data', 'User_Data')  # Ici, 'data' est directement sous le dossier du projet
    os.makedirs(data_dir, exist_ok=True)  # Créer le répertoire si nécessaire
    
    file_path = os.path.join(data_dir, 'users_info.json')
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(users_info, f, indent=4, ensure_ascii=False)
            
    except Exception as e:
        # Log d'erreur si la sauvegarde échoue
        logger.error(f"Erreur lors de la sauvegarde des utilisateurs créés : {e}")
