import requests, json

from core.config import BASE_URL, TOKEN
#from core.logger import logger
from modules.headers import auth_headers
 

def fetch_chapter_byid(chapter_id):

    try: 
        # logger here after
        chapter_response =  requests.get(f"{BASE_URL}/api/chapter/{chapter_id}", headers = auth_headers)
        chapter_response.raise_for_status()
        chapter_data = chapter_response.json()
        # logger here after
        return chapter_data
    except requests.exceptions.RequestException as e:
        
        #logger here after 
        return None

# Need filter json data chapter to get only name chapter and description 
def filter_chapter(chapter_data):
    filtered_chapter_data = {
        "name": chapter_data.get("name"),
        "description" : chapter_data.get("description")
    }
    return filtered_chapter_data