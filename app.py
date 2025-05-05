# app.py

import sys
import os

# Ajouter le dossier 'src' au sys.path pour que Python puisse trouver les modules.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Maintenant, tu peux importer main depuis src/core.
from core.main import main

# Appeler la fonction main pour exécuter le programme
if __name__ == "__main__":
    main()
