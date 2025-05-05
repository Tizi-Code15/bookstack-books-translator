import requests
import json
from core.config import URL, TOKEN
import sys
import os

# Add the 'src' folder to sys.path so Python can find the modules.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Define headers for the API request
headers = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json"
}

# Retrieve recycle bin data
def get_recycle():
    try:
        response = requests.get(f"{URL}/api/recycle-bin", headers=headers)
        response.raise_for_status()  # Check if the request was successful (status code 200)
        print(f"API response successful, status: {response.status_code}")  # Print the response status for diagnostic
        recycle = response.json().get("data", [])
        return recycle
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving recycle bin: {e}")
        return []

# Save recycle bin data to a JSON file
def save_recycle_to_json(recycle):
    if not recycle:
        print("No items found in the recycle bin.")
        return

    # Get the absolute path to the project root folder
    medulla_verse = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_dir = os.path.join(medulla_verse, 'data', 'Recycle_Data')
    
    # Check and create the directory if necessary
    if not os.path.exists(data_dir):
        print(f"Creating directory: {data_dir}")
    os.makedirs(data_dir, exist_ok=True)

    # Full path to the output JSON file
    file_path = os.path.join(data_dir, 'Recycle_Bin_info.json')

    # Print the file path to verify
    print(f"Saving JSON file to: {file_path}")

    try:
        # Save the data to the JSON file
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(recycle, f, indent=4, ensure_ascii=False)
        print("The recycle bin has been successfully saved.")
    except Exception as e:
        print(f"Error creating the JSON file: {e}")

