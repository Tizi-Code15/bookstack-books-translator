# id lister 
import requests, json

from core.config import BASE_URL
#from core.logger import logger
from modules.headers import auth_headers
 

def fetch_chapter_list():
    
    try:
        # logger after here 
        response = requests.get(f"{BASE_URL}/api/chapters", headers = auth_headers)
        response.raise_for_status()
        chapter_list = response.json()
        return chapter_list
    except requests.RequestException as e :
        # logger after 
        return None

def filter_chapter_list(chapter_list):
    
    filtered_chapter_list = []

    for item in chapter_list:
        chapter_list_data = {
            "id" : item.get("id")
        }
        filtered_chapter_list.append(chapter_list_data)
    return filtered_chapter_list

