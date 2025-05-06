import requests, json, os, sys

from core.config import URL, TOKEN
from core.logger import logger  

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Headers for API requests
headers = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json"
}

def get_users():
    # Fetches the list of users from the API.
    try:
        logger.info("Sending request to fetch users from the API.")
        response = requests.get(f"{URL}/api/users", headers=headers)
        response.raise_for_status()  # Check if the request was successful
        
        # Process the users returned by the API
        users_list = response.json().get("data", [])
        logger.info(f"{len(users_list)} users retrieved.")
        return users_list
    except requests.exceptions.RequestException as e:
        # Detailed error log
        logger.error(f"Error fetching users: {e}")
        return []

def save_users_to_json(users):
    #aves the fetched users to a JSON file.
    if not users:
        logger.warning("No users to save.")
        return
    
    # Define the directory and file path for saving
    medulla_verse = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    data_dir = os.path.join(medulla_verse, 'data', 'User_Data')
    os.makedirs(data_dir, exist_ok=True)  # Create the directory if necessary
    
    file_path = os.path.join(data_dir, 'users_data.json')
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4, ensure_ascii=False)
        logger.info("User data has been successfully saved.")
    except Exception as e:
        # Detailed error log for saving failure
        logger.error(f"Error saving users to file {file_path}: {e}")
