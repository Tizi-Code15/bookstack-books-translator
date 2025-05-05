# English.py

import os
import requests
import json
from core.config import URL, TOKEN, TRANSLATE_URL

# Translation function that sends a translation request to the API
def translate(text, target_language="en"):
    # Constructing a dictionary containing the data to be sent in the request
    payload = {
        "q": text,
        "source": "fr",
        "target": target_language,
        "format": "html"
    }
    try:
        # Sending the POST request to translate the text
        response = requests.post(TRANSLATE_URL, json=payload)
        response.raise_for_status() # Get the status code and raise an exception if needed
        # Retrieve the response in JSON format
        return response.json()['translatedText']
    except requests.exceptions.RequestException as e:
        print(f"Translation error: {e}")
        return text

# Function to save translation logs to a JSON file
def save_translation_log(log_data):
    if not log_data:
        print("No logs to save.")
        return
    
    # Get absolute path from the project root folder
    medulla_verse = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_dir = os.path.join(medulla_verse, 'data', 'English_Data')
    os.makedirs(data_dir, exist_ok=True)

    # Full path to the output JSON file
    file_path = os.path.join(data_dir, 'English_translation.json')

    try:
        # Write the log data
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(log_data, f, indent=4, ensure_ascii=False)
        print("Translation logs successfully saved.")
    except Exception as e:
        print(f"Error saving the translation log: {e}")

# Main function for translating the book
def run_translation(book_id):
    headers = {
        "Authorization": f"Token {TOKEN}",
        "Content-Type": "application/json"
    }
    
    log = []  # Create a list to store translation steps

    # Retrieve book details by making a request to the API
    book_response = requests.get(f"{URL}/api/books/{book_id}", headers=headers)
    # Store the details in JSON format
    book = book_response.json()
    translated_title = translate(book.get("name", ""))
    translated_desc = translate(book.get("description", ""))

    # Create a new translated book
    book_payload = {
        "name": translated_title,
        "description": translated_desc
    }
    create_book_response = requests.post(f"{URL}/api/books", headers=headers, json=book_payload)
    new_book = create_book_response.json()
    new_book_id = new_book["id"]
    log.append({"step": "book", "message": f"New book created: {new_book_id} - {translated_title}"})

    # Retrieve and translate the chapters
    chapters_response = requests.get(f"{URL}/api/chapters", headers=headers)
    chapters = [c for c in chapters_response.json().get("data", []) if c.get("book_id") == book_id]

    for chapter in chapters:
        chapter_id = chapter["id"]
        translated_chapter_name = translate(chapter["name"])
        log.append({"step": "chapter", "message": f"Chapter: {translated_chapter_name}"})

        # Create the chapter in the new book
        chapter_payload = {
            "book_id": new_book_id,
            "name": translated_chapter_name
        }
        chapter_create_response = requests.post(f"{URL}/api/chapters", headers=headers, json=chapter_payload)
        new_chapter = chapter_create_response.json()
        new_chapter_id = new_chapter["id"]

        # Retrieve and translate the pages related to the chapter
        pages_response = requests.get(f"{URL}/api/pages", headers=headers)
        pages = [p for p in pages_response.json().get("data", []) if p.get("chapter_id") == chapter_id]

        for page in pages:
            page_id = page["id"]
            page_detail_response = requests.get(f"{URL}/api/pages/{page_id}", headers=headers)
            page_data = page_detail_response.json()

            translated_page_title = translate(page_data.get("name", ""))
            translated_html = translate(page_data.get("html", ""))

            # Create the translated page in the new book
            page_payload = {
                "book_id": new_book_id,
                "chapter_id": new_chapter_id,
                "name": translated_page_title,
                "html": translated_html
            }
            create_page_response = requests.post(f"{URL}/api/pages", headers=headers, json=page_payload)
            created_page = create_page_response.json()
            log.append({"step": "page creation", "message": f"Page created: {created_page['id']}"})

    # Save the logs to a JSON file
    save_translation_log(log)

    print("Translation to English completed.")

# If the file is run directly
if __name__ == "__main__":
    run_translation(21)
