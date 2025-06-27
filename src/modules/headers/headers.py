import os
from core.config import TOKEN
from core.logger import logger  


headers = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json"
}