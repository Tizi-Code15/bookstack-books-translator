import logging
import os

# Définir les chemins des dossiers de logs
LOG_DIR = 'logs'
INFO_LOG_DIR = os.path.join(LOG_DIR, 'info')
ERROR_LOG_DIR = os.path.join(LOG_DIR, 'error')

# Créer les répertoires de logs si ils n'existent pas
os.makedirs(INFO_LOG_DIR, exist_ok=True)
os.makedirs(ERROR_LOG_DIR, exist_ok=True)

# Chemins complets des fichiers de logs
INFO_LOG_FILE = os.path.join(INFO_LOG_DIR, 'info.log')
ERROR_LOG_FILE = os.path.join(ERROR_LOG_DIR, 'error.log')

# Création du logger
logger = logging.getLogger('medulla_logger')
logger.setLevel(logging.DEBUG)  # Enregistre tout de DEBUG à CRITICAL (pour les fichiers)

# Handler pour les messages INFO et plus dans les fichiers de logs (info.log et error.log)
file_handler = logging.FileHandler(INFO_LOG_FILE, mode='a', encoding='utf-8')
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Handler pour les messages ERROR et plus dans les fichiers d'erreurs (error.log)
error_handler = logging.FileHandler(ERROR_LOG_FILE, mode='a', encoding='utf-8')
error_handler.setLevel(logging.ERROR)  # Capture uniquement les erreurs
error_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
error_handler.setFormatter(error_formatter)

# Handler pour afficher dans la console sans la date/heure
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Affiche les logs à partir de INFO dans la console
console_formatter = logging.Formatter('%(levelname)s - %(message)s')  # Pas de date/heure
console_handler.setFormatter(console_formatter)

# Ajout des handlers au logger
logger.addHandler(file_handler)
logger.addHandler(error_handler)
logger.addHandler(console_handler)
