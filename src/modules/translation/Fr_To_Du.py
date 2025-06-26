import os, requests, json
from core.config import URL, TOKEN, TRANSLATE_URL

# Configuration

BOOK_ID = 21  

HEADERS = {
    "Authorization": f"Token {TOKEN}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def translate(text, target_language="de"):
    """
    Translate the given text from French to target_language using LibreTranslate API.
    """
    payload = {
        "q": text,
        "source": "fr",
        "target": target_language,
        "format": "html"
    }
    try:
        response = requests.post(TRANSLATE_URL, json=payload, timeout=10)
        response.raise_for_status()
        return response.json().get("translatedText", text)
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def get_book(book_id):
    url = f"{URL}/api/books/{book_id}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def get_page(page_id):
    url = f"{URL}/api/pages/{page_id}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def create_book(name, description):
    url = f"{URL}/api/books"
    payload = {
        "name": name,
        "description": description
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()

def create_page(book_id, name, html, chapter_id=None):
    url = f"{URL}/api/pages"
    payload = {
        "book_id": book_id,
        "name": name,
        "html": html
    }
    if chapter_id:
        payload["chapter_id"] = chapter_id
    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()

def main():
    book = get_book(BOOK_ID)
    print(f"Original book: {book['name']}")

    translated_name = translate(book["name"], target_language="de")
    translated_description = translate(book["description_html"], target_language="de")

    new_book = create_book(translated_name, translated_description)
    new_book_id = new_book["id"]
    print(f"Translated book created: {translated_name} (ID {new_book_id})")

    for content in book.get("contents", []):
        if content["type"] == "page":
            page_id = content["id"]
            page = get_page(page_id)
            translated_page_name = translate(page["name"], target_language="de")
            translated_html = translate(page["html"], target_language="de")
            created_page = create_page(new_book_id, translated_page_name, translated_html)
            print(f"Translated page created: {translated_page_name} (ID {created_page['id']})")
        elif content["type"] == "chapter":
            pass

if __name__ == "__main__":
    main()
