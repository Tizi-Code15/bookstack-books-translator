import os, requests, json

from core.config import URL, TOKEN, TRANSLATE_URL
from core.logger import logger

# Translation of a given text using the LibreTranslate API
def translate(text, target_language="en"):
    payload = {
        "q": text,
        "source": "fr",
        "target": target_language,
        "format": "html"
    }
    try:
        logger.debug(f"Translation request sent for: {text[:30]}... (to {target_language})")  # Debug log
        response = requests.post(TRANSLATE_URL, json=payload)
        response.raise_for_status()
        translated_text = response.json().get("translatedText", "")
        logger.debug(f"Translation successful: {translated_text[:30]}...")  # Debug log
        return translated_text
    except requests.exceptions.RequestException as e:
        logger.error(f"Translation error: {e}")
        return text  # In case of error, return the original text

# Save translation logs to a JSON file
def save_translation_log(log_data):
    # Saves translation logs to a JSON file.
    if not log_data:
        logger.warning("No logs to save.")  # Log if there's nothing to save
        return

    # Define the save directory for translation logs
    # 'data' is directly under the project root, no need to include 'src/'
    
    medulla_verse = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    data_dir = os.path.join(medulla_verse, 'data', 'English_Data')  # Directory to save logs
    os.makedirs(data_dir, exist_ok=True)  # Create directory if needed

    file_path = os.path.join(data_dir, 'English_translation.json')

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(log_data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        # Log error if saving fails
        logger.error(f"Error while saving translation logs: {e}")

# Main function to translate a book by its ID
def run_translation(book_id):
    headers = {
        "Authorization": f"Token {TOKEN}",
        "Content-Type": "application/json"
    }

    log = []
    logger.info(f"Starting translation of book ID: {book_id}")

    try:
        # Retrieve the original book
        book_response = requests.get(f"{URL}/api/books/{book_id}", headers=headers)
        book_response.raise_for_status()
        book = book_response.json()
        logger.info(f"Book retrieved: {book.get('name', 'Unknown')}")

        # Translate title and description
        translated_title = translate(book.get("name", ""))
        translated_desc = translate(book.get("description", ""))

        # Create the new translated book
        book_payload = {
            "name": translated_title,
            "description": translated_desc
        }
        new_book_resp = requests.post(f"{URL}/api/books", headers=headers, json=book_payload)
        new_book_resp.raise_for_status()
        new_book = new_book_resp.json()
        new_book_id = new_book["id"]
        log.append({"step": "book", "message": f"Book created: {new_book_id} - {translated_title}"})

        # Retrieve and translate chapters
        chapters_resp = requests.get(f"{URL}/api/chapters", headers=headers)
        chapters_resp.raise_for_status()
        chapters = [c for c in chapters_resp.json().get("data", []) if c.get("book_id") == book_id]

        for chapter in chapters:
            chapter_id = chapter["id"]
            translated_chapter_name = translate(chapter["name"])
            log.append({"step": "chapter", "message": f"Chapter translated: {translated_chapter_name}"})

            # Create chapter in the new book
            chapter_payload = {
                "book_id": new_book_id,
                "name": translated_chapter_name
            }
            chapter_resp = requests.post(f"{URL}/api/chapters", headers=headers, json=chapter_payload)
            chapter_resp.raise_for_status()
            new_chapter_id = chapter_resp.json()["id"]

            # Retrieve and translate pages in the chapter
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
                log.append({"step": "page", "message": f"Page created: {created_page['id']}"})

        # Nouvelle partie : gérer les pages sans chapitre 
        pages_resp = requests.get(f"{URL}/api/pages", headers=headers)
        pages_resp.raise_for_status()
        pages_no_chapter = [p for p in pages_resp.json().get("data", []) if p.get("book_id") == book_id and not p.get("chapter_id")]

        for page in pages_no_chapter:
            page_id = page["id"]
            page_detail_resp = requests.get(f"{URL}/api/pages/{page_id}", headers=headers)
            page_detail_resp.raise_for_status()
            page_data = page_detail_resp.json()

            translated_title = translate(page_data.get("name", ""))
            translated_html = translate(page_data.get("html", ""))

            page_payload = {
                "book_id": new_book_id,
                "name": translated_title,
                "html": translated_html
            }

            created_page_resp = requests.post(f"{URL}/api/pages", headers=headers, json=page_payload)
            created_page_resp.raise_for_status()
            created_page = created_page_resp.json()
            log.append({"step": "page", "message": f"Page created: {created_page['id']}"})

        # Save logs
        save_translation_log(log)
        logger.info("Translation to English completed successfully.")

    except requests.exceptions.RequestException as e:
        logger.error(f"Error during translation: {e}")
        save_translation_log(log)  # Save partial logs in case of error
