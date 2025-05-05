import os
import requests
import json

from core.config import URL, TOKEN, TRANSLATE_URL
from core.logger import logger

# Traduction d'un texte donné via l'API LibreTranslate
def translate(text, target_language="en"):
    payload = {
        "q": text,
        "source": "fr",
        "target": target_language,
        "format": "html"
    }
    try:
        logger.debug(f"Demande de traduction envoyée pour : {text[:30]}... (vers {target_language})")  # Changer en debug
        response = requests.post(TRANSLATE_URL, json=payload)
        response.raise_for_status()
        translated_text = response.json().get("translatedText", "")
        logger.debug(f"Traduction réussie : {translated_text[:30]}...")  # Changer en debug
        return translated_text
    except requests.exceptions.RequestException as e:
        logger.error(f"Erreur de traduction : {e}")
        return text  # En cas d’erreur, on retourne le texte original

# Sauvegarde des logs de traduction dans un fichier JSON
def save_translation_log(log_data):
    """Sauvegarde les logs de traduction dans un fichier JSON."""
    if not log_data:
        logger.warning("Aucun log à sauvegarder.")  # Log si aucun log à sauvegarder
        return
    
    # Définir le répertoire de sauvegarde pour les logs de traduction
    # Ici, 'data' est directement sous le dossier du projet, pas besoin d'ajouter 'src/'
    medulla_verse = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    data_dir = os.path.join(medulla_verse, 'data', 'English_Data')  # Le répertoire de sauvegarde des logs
    os.makedirs(data_dir, exist_ok=True)  # Créer le répertoire si nécessaire
    
    file_path = os.path.join(data_dir, 'English_translation.json')
    
    try:
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(log_data, f, indent=4, ensure_ascii=False)
            
    except Exception as e:
        # Log d'erreur si la sauvegarde échoue
        logger.error(f"Erreur lors de la sauvegarde des logs de traduction : {e}")

# Fonction principale de traduction d’un livre par ID
def run_translation(book_id):
    headers = {
        "Authorization": f"Token {TOKEN}",
        "Content-Type": "application/json"
    }

    log = []
    logger.info(f"Début de la traduction du livre ID : {book_id}")

    try:
        # Récupération du livre original
        book_response = requests.get(f"{URL}/api/books/{book_id}", headers=headers)
        book_response.raise_for_status()
        book = book_response.json()
        logger.info(f"Livre récupéré : {book.get('name', 'Inconnu')}")

        # Traduction du titre et de la description
        translated_title = translate(book.get("name", ""))
        translated_desc = translate(book.get("description", ""))

        # Création du nouveau livre traduit
        book_payload = {
            "name": translated_title,
            "description": translated_desc
        }
        new_book_resp = requests.post(f"{URL}/api/books", headers=headers, json=book_payload)
        new_book_resp.raise_for_status()
        new_book = new_book_resp.json()
        new_book_id = new_book["id"]
        log.append({"step": "book", "message": f"Livre créé : {new_book_id} - {translated_title}"})

        # Récupération et traduction des chapitres
        chapters_resp = requests.get(f"{URL}/api/chapters", headers=headers)
        chapters_resp.raise_for_status()
        chapters = [c for c in chapters_resp.json().get("data", []) if c.get("book_id") == book_id]

        for chapter in chapters:
            chapter_id = chapter["id"]
            translated_chapter_name = translate(chapter["name"])
            log.append({"step": "chapter", "message": f"Chapitre traduit : {translated_chapter_name}"})

            # Création du chapitre dans le nouveau livre
            chapter_payload = {
                "book_id": new_book_id,
                "name": translated_chapter_name
            }
            chapter_resp = requests.post(f"{URL}/api/chapters", headers=headers, json=chapter_payload)
            chapter_resp.raise_for_status()
            new_chapter_id = chapter_resp.json()["id"]

            # Récupération et traduction des pages du chapitre
            pages_resp = requests.get(f"{URL}/api/pages", headers=headers)
            pages_resp.raise_for_status()
            pages = [p for p in pages_resp.json().get("data", []) if p.get("chapter_id") == chapter_id]

            for page in pages:
                page_id = page["id"]
                page_detail_resp = requests.get(f"{URL}/api/pages/{page_id}", headers=headers)
                page_detail_resp.raise_for_status()
                page_data = page_detail_resp.json()

                translated_title = translate(page_data.get("name", ""))
                translated_html = translate(page_data.get("html", ""))

                page_payload = {
                    "book_id": new_book_id,
                    "chapter_id": new_chapter_id,
                    "name": translated_title,
                    "html": translated_html
                }

                created_page_resp = requests.post(f"{URL}/api/pages", headers=headers, json=page_payload)
                created_page_resp.raise_for_status()
                created_page = created_page_resp.json()
                log.append({"step": "page", "message": f"Page créée : {created_page['id']}"})

        # Sauvegarde des logs
        save_translation_log(log)
        logger.info("Traduction vers l'anglais terminée avec succès.")

    except requests.exceptions.RequestException as e:
        logger.error(f"Erreur pendant la traduction : {e}")
        save_translation_log(log)  # Sauvegarder les logs partiels en cas d'erreur)
