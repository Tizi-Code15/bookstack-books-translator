import requests, json, os, sys

from core.config import URL, TOKEN
from core.logger import logger 
 
from modules.headers import auth_headers

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



def create_user(name, email, password, roles=None):
    # Creates a user via the API.
    if roles is None:
        roles = []
    
    data = {
        "name": name,
        "email": email,
        "password": password,
        "roles": roles
    }
    
    try:
        # Log before making the request
        logger.info(f"Sending request to create user: {name} ({email})")
        response = requests.post(f"{URL}/api/users", headers=auth_headers, json=data)
        response.raise_for_status()  # Check the response status
        
        # Extract the created user
        created_user = response.json()
        
        # Success log
        logger.info(f"User created successfully: {created_user.get('name', 'Unknown')} (ID: {created_user.get('id')})")
        return created_user
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error creating user: {e}")  # Error log
        return None  # Return None in case of error

def save_created_users_to_json(users_info):
    # Saves the created users to a JSON file.
    if not users_info:
        logger.warning("No users to save.")  # Log if there are no users to save
        return
    
    # Define the save directory for the created users
    # Corrected to save in 'data/User_Data' without adding 'src/'
    medulla_verse = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    data_dir = os.path.join(medulla_verse, 'data', 'User_Data')  # 'data' is directly under the project folder
    os.makedirs(data_dir, exist_ok=True)  # Create the directory if necessary
    
    file_path = os.path.join(data_dir, 'users_info.json')
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(users_info, f, indent=4, ensure_ascii=False)
            
    except Exception as e:
        # Error log if the save fails
        logger.error(f"Error saving created users: {e}")
