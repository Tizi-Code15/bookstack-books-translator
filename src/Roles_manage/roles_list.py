import requests, json, os, sys
from core.config import URL, TOKEN
from core.logger import logger  # Importing the logger setup

# add parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# define HTTP headers
headers = {
    "authorization": f"Token {TOKEN}",
    "Content-Type": "application/json"
}

# Get list of roles from API
def get_list_roles():
    try:
        # Send GET request to the API endpoint
        logger.info("Sending GET request to retrieve roles from API.")  # Log the request
        response = requests.get(f"{URL}/api/roles", headers=headers)
        response.raise_for_status()  # Check if the response status code is OK
        list_roles = response.json().get("data", [])
        
        if list_roles:
            logger.info(f"Successfully retrieved {len(list_roles)} roles.")  # Log success
            print(f"Number of roles: {len(list_roles)}")
        else:
            logger.warning("No roles found in the response.")  # Log if no roles are found
            print("No list of roles created")
        
        return list_roles
    
    except requests.exceptions.RequestException as e:
        # Log the error if there's an issue with the request
        logger.error(f"Error retrieving list of roles: {e}")
        print(f"Error creating list: {e}")
        return []

# Save the list of roles to a JSON file
def save_list_roles_to_json(list_info):
    if not list_info:
        logger.warning("No roles to save.")  # Log if no data is passed to the function
        print("No list to save")
        return
    
    # Get absolute path from project root
    medulla_verse = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_dir = os.path.join(medulla_verse, 'data', 'Roles_Data')
    os.makedirs(data_dir, exist_ok=True)

    # Full path to the output JSON file
    file_path = os.path.join(data_dir, 'list_info.json')
    
    try:
        # Write the role data to the file
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(list_info, f, indent=4, ensure_ascii=False)
        logger.info(f"Roles data successfully saved to {file_path}")  # Log the successful save
        print("User data successfully saved to:")
    
    except Exception as e:
        # Log any error encountered while saving the file
        logger.error(f"Error creating the JSON file: {e}")
        print(f"Error creating the JSON file: {e}")
