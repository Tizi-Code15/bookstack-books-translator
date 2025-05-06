import requests , os, json, sys

from core.config import URL, TOKEN
from core.logger import logger

# Determine the root folder of the project
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# Configure the headers for the BookStack API
HEADERS = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json"
}

def get_books_id():
  
  # Retrieves the list of books from the BookStack API.
  # Returns a list containing the book information.
    try:
        logger.info("Sending the request to retrieve the books from the API.")
        response = requests.get(f"{URL}/api/books", headers=HEADERS)
        response.raise_for_status()
        books_id = response.json().get("data", [])
        logger.info(f"{len(books_id)} Books retrieved successfully.")
        return books_id
    except requests.exceptions.RequestException as e:
        logger.error(f"Error while retrieving the books: {e}")
        return []

def save_books_info_to_json(books_info):
    if not books_info:
        logger.warning("No books to save.")
        return

    # Base projet : src/
    medulla_verse = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    data_dir = os.path.join(medulla_verse, 'data', 'Books_Data')
    os.makedirs(data_dir, exist_ok=True)

    file_path = os.path.join(data_dir, "book_ids.json")

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(books_info, f, indent=4, ensure_ascii=False)
        logger.info("Les livres ont été sauvegardés avec succès.")
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde des livres : {e}")

