# ftech_books
import requests , os, json, sys

from core.config import BASE_URL, TOKEN, LIST_ENDPOINT
from core.logger import logger
from modules.headers import headers


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# Get list of book 
def fetch_books_list():

    try:
        logger.info("Sending the request to retrieve the books from the API.")
        response = requests.get(LIST_ENDPOINT, headers=headers)
        response.raise_for_status()
        books_list = response.json().get("data", [])
        logger.info(f"{len(books_list)} Books retrieved successfully.")
        return books_list
    except requests.exceptions.RequestException as e:
        logger.error(f"Error while retrieving the books: {e}")
        return []
    

# filtre json data that content list of books
def filter_books_list(books_list):

    filtred_list = []

    for item in books_list :
        list_data = {
            "id": item.get("id"),
            "name" : item.get("name"),
            "created_at" : item.get("created_at"),
            "updated_at" : item.get("updated_at")
        }
        filtred_list.append(list_data)

    return filtred_list



