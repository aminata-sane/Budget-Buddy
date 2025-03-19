import re
import hashlib

def validate_password(password):
        if len(password) > 10:
            return False, "Le mot de passe ne doit pas dépasser 10 caractères."
        if not re.search(r"[A-Z]", password):
            return False, "Le mot de passe doit contenir au moins une majuscule."
        if not re.search(r"[a-z]", password):
            return False, "Le mot de passe doit contenir au moins une minuscule."
        if not re.search(r"[0-9]", password):
            return False, "Le mot de passe doit contenir au moins un chiffre."
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "Le mot de passe doit contenir au moins un caractère spécial."
        return True, ""

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()