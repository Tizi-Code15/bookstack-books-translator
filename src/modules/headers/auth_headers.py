# headers
from core.config import TOKEN

api_auth_headers = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json"
}