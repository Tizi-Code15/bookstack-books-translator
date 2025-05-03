# user_id.py:
import requests, json, os, sys
from core.config import URL, TOKEN

# Add parent directory to system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Define HTTP headers for the API requests
headers = {
    "authorization": f"Token {TOKEN}",
    "Content-Type": "application/json"
}

# Retrieve the list of users from the API
def get_users():
    try:
        # Send a GET request to the API endpoint 
        response = requests.get(f"{URL}/api/users", headers=headers)
        response.raise_for_status()
        # Extract the "data" field from the JSON response
        users_list = response.json().get("data", [])
        print(f"Number of users retrieved: {len(users_list)}")
        return users_list
    except requests.exceptions.RequestException as e:
        # Handle connection or HTTP-related errors
        print(f"Error retrieving users: {e}")
        return []

# Save user data to a JSON file
def save_users_to_json(users):

    if not users:
        print("No users to save.")
        return
    
    # Get absolute path from project root folder
    medulla_verse = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_dir = os.path.join(medulla_verse, 'data', 'User_Data')
    os.makedirs(data_dir, exist_ok=True)

    # Full path to the output JSON file 
    file_path = os.path.join(data_dir, 'users_data.json')

    try:
        # Write the user data to a JSON file
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4, ensure_ascii=False)
        print("User data successfully saved to: data/User_Data")
    except Exception as e:
        print(f"Error creating the JSON file: {e}")
