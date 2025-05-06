import sys
import os
import traceback

# Add the 'src' folder to sys.path so that Python can find the modules

SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from core.main import main
from core.logger import logger

def run_application():
    
    # Main function to start the application.
    # It wraps the call to 'main' for better testability.

    try:
        logger.info("Lancement du programme")
        main()
        logger.info("Le programme principal a terminé avec succès.")
    except Exception as e:
        logger.error(f"Erreur lors de l'exécution de 'main' : {e}")
        logger.error("Traceback complet :")
        # Imprimer la trace de l'exception pour aider au débogage
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    run_application()
