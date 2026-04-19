import re

class Contact:
    def __init__(self, nom: str, email: str, numéro: str):
        assert isinstance(nom, str) and nom.strip(), "Le nom doit être une chaîne non vide."
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        pattern_numéro = r"^(06|07)\d{8}$"
        assert re.fullmatch(pattern, email) is not None, "Adresse email invalide."
        assert re.fullmatch(pattern_numéro, numéro) is not None, \
            "Le numéro doit comporter 10 chiffres et commencer par 06 ou 07."

        self.nom = nom.strip()
        self.email = email.strip()
        self.numéro = numéro.strip()

    def __str__(self):
        return f"{self.nom} | {self.email} | {self.numéro}"

    def __repr__(self):
        return f"Contact({self.nom!r}, {self.email!r}, {self.numéro!r})"
