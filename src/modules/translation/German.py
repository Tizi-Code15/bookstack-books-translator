import os
import requests
import json
from core.config import URL, TOKEN, TRANSLATE_URL
from core.logger import logger  # Utilise le logger global existant

# Fonction de traduction
def translate(text, target_language="de"):
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
        return text  # Retourne le texte original en cas d'erreur

# Sauvegarde des logs de traduction dans un fichier JSON
def save_translation_log(log_data):
    """Sauvegarde des logs de traduction dans un fichier JSON."""
    if not log_data:
        logger.warning("Aucun log à sauvegarder.")  # Log d'avertissement si aucun log à sauvegarder
        return

    # Définir le répertoire de sauvegarde pour les logs de traduction
    medulla_verse = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    data_dir = os.path.join(medulla_verse, 'data', 'German_Data')  # Le répertoire de sauvegarde des logs
    os.makedirs(data_dir, exist_ok=True)  # Créer le répertoire si nécessaire

    file_path = os.path.join(data_dir, 'German_translation.json')

    try:
        # Sauvegarde des logs dans un fichier JSON
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(log_data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde des logs : {e}")

# Fonction principale
def run_translation(book_id):
    headers = {
        "Authorization": f"Token {TOKEN}",
        "Content-Type": "application/json"
    }

    log = []

    logger.info(f"Démarrage de la traduction du livre ID : {book_id}")

    try:
        # Récupération du livre
        book_resp = requests.get(f"{URL}/api/books/{book_id}", headers=headers)
        book_resp.raise_for_status()
        book = book_resp.json()

        # Traduction du titre et de la description
        translated_title = translate(book.get("name", ""))
        translated_desc = translate(book.get("description", ""))

        # Création du livre traduit
        book_payload = {
            "name": translated_title,
            "description": translated_desc
        }
        new_book_resp = requests.post(f"{URL}/api/books", headers=headers, json=book_payload)
        new_book_resp.raise_for_status()
        new_book_id = new_book_resp.json()["id"]
        log.append({"step": "book", "message": f"Nouveau livre créé : {new_book_id} - {translated_title}"})

        # Récupération et traduction des chapitres
        chapters_resp = requests.get(f"{URL}/api/chapters", headers=headers)
        chapters_resp.raise_for_status()
        chapters = [c for c in chapters_resp.json().get("data", []) if c.get("book_id") == book_id]

        for chapter in chapters:
            chapter_id = chapter["id"]
            translated_chapter_name = translate(chapter["name"])
            log.append({"step": "chapter", "message": f"Chapitre traduit : {translated_chapter_name}"})

            chapter_payload = {
                "book_id": new_book_id,
                "name": translated_chapter_name
            }
            new_chapter_resp = requests.post(f"{URL}/api/chapters", headers=headers, json=chapter_payload)
            new_chapter_resp.raise_for_status()
            new_chapter_id = new_chapter_resp.json()["id"]

            # Récupération et traduction des pages
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

        # Sauvegarde finale des logs
        save_translation_log(log)
        logger.info("Traduction vers l'allemand terminée avec succès.")

    except requests.exceptions.RequestException as e:
        logger.error(f"Erreur pendant la traduction : {e}")
        save_translation_log(log)  # Sauvegarder les logs partiels en cas d'erreur
