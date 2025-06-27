# Configuration
from dotenv import load_dotenv
import os

# Charger les variables d'environnement du fichier .env
load_dotenv()

# Obtenir les valeurs des variables d'environnement
TOKEN = os.getenv('TOKEN')
TRANSLATE_URL = os.getenv('TRANSLATE_URL')

# Endpoints Bookstack 
BASE_URL = os.getenv('URL')

### Books Endpoint
LIST_ENDPOINT = f"{BASE_URL}/api/books"
CREATE_ENDPOINT = f"{BASE_URL}/api/books"




chapterendoint = f"{BASE_URL}/api/chapters"

# Optionnel : Vérifier si les variables sont bien chargées
if not BASE_URL or not TOKEN or not TRANSLATE_URL:
    raise ValueError("URL, TOKEN, or TRANSLATE_URL environment variables are not set!")









