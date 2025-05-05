import getpass
import re
from core.logger import logger  # Importation du logger

def ask_secure_password():
    """Demande à l'utilisateur de saisir et confirmer son mot de passe."""
    while True:
        password = getpass.getpass("Entrez votre mot de passe : ")
        confirm = getpass.getpass("Confirmez votre mot de passe : ")

        if password != confirm:
            log_and_print_error("Les mots de passe ne correspondent pas.")
            continue

        if not validate_password_caract(password):
            log_and_print_error("Mot de passe trop faible. Il doit contenir au moins 8 caractères, une majuscule, une minuscule, un chiffre et un symbole.")
            continue
        
        logger.info("Mot de passe défini avec succès.")
        return password

def validate_password_caract(pwd):
    """Valide le mot de passe en vérifiant sa longueur, majuscules, minuscules, chiffres et symboles."""
    is_valid = (
        len(pwd) >= 8 and
        re.search(r"[A-Z]", pwd) and
        re.search(r"[a-z]", pwd) and
        re.search(r"\d", pwd) and
        re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", pwd)
    )
    
    if not is_valid:
        logger.warning("Le mot de passe ne respecte pas les critères requis.")
    return is_valid

 #Enregistre un message d'erreur dans les logs et l'affiche à l'utilisateur.
def log_and_print_error(message):
    """Logge et affiche un message d'erreur."""
    logger.warning(message)
    print(message)
