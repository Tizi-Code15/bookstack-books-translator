# ftech_books
import requests , os, json, sys

from core.config import BASE_URL, TOKEN, LIST_ENDPOINT
from core.logger import logger
from modules.headers import headers

# Add parent folder to sys.path to import core and modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Constants
SAVE_DIR = os.path.join("src", "data", "Books_Data")
SAVE_FILE = "filtered_books.json"

# Get list of book 
def fetch_books_list():

    try:
        logger.info("Sending request to retrieve books from API.")
        response = requests.get(LIST_ENDPOINT, headers=headers)
        response.raise_for_status()
        books_list = response.json().get("data", [])
        logger.info(f"{len(books_list)} Books retrieved successfully.")
        return books_list
    except requests.exceptions.RequestException as e:
        logger.error(f"Error while retrieving the books: {e}")
        return []
    

#filtration data
def filter_books_list(books_list):

    filtered_list = []

    for item in books_list :
        list_data = {
            "id": item.get("id"),
            "name" : item.get("name"),
            "created_at" : item.get("created_at"),
            "updated_at" : item.get("updated_at")
        }
        filtered_list.append(list_data)

    return filtered_list

# save filtred_list on data folder 

def save_filtered_list(data):

    file_path = os.path.join(SAVE_DIR,  SAVE_FILE)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent= 4, ensure_ascii=False)
        logger.info(f"filtred_list saved to {file_path}")
    except Exception as e:
        logger.error(f"Error saving filtred_list: {e}")

if __name__ == '__main__':
    books_list = fetch_books_list()
    filtered_list = filter_books_list(books_list)
    save_filtered_list(filtered_list)



