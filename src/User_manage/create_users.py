import requests, json, os, sys
from core.config import URL, TOKEN

# Add parent directory to system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Define HTTP headers 
headers = {
    "authorization": f"Token {TOKEN}",
    "Content-Type": "application/json"
}

# Retrieve the list of users from the API 
def create_users(name, email, password, roles=None): # Don't forget to retrieve the role IDs to be sure
    if roles is None:
        roles = []
    data = {
        "name": name,
        "email": email,
        "password": password,
        "roles": roles
    }

    try:
        # Send POST request to the API endpoint to create a user
        response = requests.post(f"{URL}/api/users", headers=headers, json=data)
        response.raise_for_status()
        created_user = response.json()
        print(f"User created: {created_user.get('name', 'Unknown')}")
        return created_user
        
    except requests.exceptions.RequestException as e:
        print(f"Error creating user: {e}")
        return []

# Save user data to a JSON file
def save_created_users_to_json(users_info):

    if not users_info:
        print("No users to save.")
        return
    
    # Get absolute path from project root folder
    medulla_verse = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_dir = os.path.join(medulla_verse, 'data', 'User_Data')
    os.makedirs(data_dir, exist_ok=True)

    # Full path to the output JSON file
    file_path = os.path.join(data_dir, 'users_info.json')

    try:
        # Write the user data to a JSON file
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(users_info, f, indent=4, ensure_ascii=False)
        print("User data successfully saved.")
    except Exception as e:
        print(f"Error creating the JSON file: {e}")
