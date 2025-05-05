# getbooksid.py
import requests, json, os, sys
from core.config import URL, TOKEN
#from logger.logger import logger

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



headers = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json"
}

def get_books_id():
    try:
        # log du début de l'appel d'api 
        print("Requête pour récupérer les livres depuis l'API envoyé")

        # Envoi de la requete GET
        response = requests.get(f"{URL}/api/books", headers=headers)
        # Récupération du code de statut et levée d'une exception s'il y a une erreur lors de la requête
        response.raise_for_status()
        books_id = response.json().get("data", [])
        # log quand l'opération de la récupération est réussi 
        print(f"{len(books_id)} Livres récupérés avec succés.")
        return books_id
    
    except requests.exceptions.RequestException as e:
        print(f"Erreur récupération des livres : {e}")
        #logger.error(f"Erreur de récupérations des livres : {e}")
        return []

def save_books_info_to_json(books_info):
    if not books_info:
        print("No books to save")
        return
    # Get absolute path from foolder root
    medulla_verse = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_dir = os.path.join(medulla_verse, 'data' 'Books_Data')
    os.makedirs(data_dir, exist_ok=True)
    try:
        # log de l'opération de sauvegarde 
        print(f"Sauvegarde de {len(books_info)} livres dabs 'books_ids.json '.'")
        # Sauvegarde des livres dans le fichier JSON
        with open("book_ids.json", "w", encoding="utf-8") as f:
            json.dump(books_info, f, indent=4, ensure_ascii=False)
        
        # log de réussite de la sauvegardes
        print("Les livre sont sauvegarder avec succés")
    except Exception as e:
        # log d'errer a la levé de l'exception 
        print(f"Erreru est servenue lors  de la sauvegarde des livres : {e}") 
    
     
