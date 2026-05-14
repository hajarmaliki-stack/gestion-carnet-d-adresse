import re

class Contact:
    def __init__(self, nom: str, email: str, numéro: str):
        assert isinstance(nom, str) and nom.strip(), "Le nom doit être une chaîne non vide."
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        # Ajout du support pour les numéros avec espaces comme dans le screenshot
        pattern_numéro = r"^[0-9\s]+$"
        
        assert re.fullmatch(pattern, email) is not None, "Adresse email invalide."
        assert re.fullmatch(pattern_numéro, numéro) is not None, \
            "Le numéro doit comporter des chiffres (et des espaces)."

        self.nom = nom.strip()
        self.email = email.strip()
        self.numéro = numéro.strip()

    def __str__(self):
        return f"{self.nom} | {self.email} | {self.numéro}"

    def __repr__(self):
        return f"Contact({self.nom!r}, {self.email!r}, {self.numéro!r})"
    
    def to_dict(self):
        return {
            "nom": self.nom,
            "email": self.email,
            "numero": self.numéro
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            nom=data.get("nom", ""),
            email=data.get("email", ""),
            numéro=data.get("numero", "")
        )
