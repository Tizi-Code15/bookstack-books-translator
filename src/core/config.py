# Configuration
from dotenv import load_dotenv
import os

# Charger les variables d'environnement du fichier .env
load_dotenv()

# Obtenir les valeurs des variables d'environnement
URL = os.getenv('URL')
TOKEN = os.getenv('TOKEN')
TRANSLATE_URL = os.getenv('TRANSLATE_URL')

# Optionnel : Vérifier si les variables sont bien chargées
if not URL or not TOKEN or not TRANSLATE_URL:
    raise ValueError("URL, TOKEN, or TRANSLATE_URL environment variables are not set!")









