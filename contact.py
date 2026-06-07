import re

class Contact:
    def __init__(self, nom: str, email: str, num: str,
                 categorie: str = "Autre", adresse: str = "",
                 fonction: str = "", entreprise: str = ""):
        nom   = nom.strip()
        email = email.strip()
        num   = num.strip()

        regex_nom   = r"^[a-zA-Z\s]+$"
        regex_email = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        regex_num   = r"^(06|07)\d{8}$"

        assert re.fullmatch(regex_nom, nom)   is not None, \
            "Le nom doit être une chaîne non vide composée de lettres et d'espaces."
        assert re.fullmatch(regex_email, email) is not None, \
            "L'email doit être une adresse email valide."
        assert re.fullmatch(regex_num, num)   is not None, \
            "Le numéro de téléphone doit être 10 chiffres commençant par 06 ou 07."

        self.nom        = nom
        self.email      = email
        self.num        = num
        # ── Partie 8 : champs supplémentaires ──────────────────────────
        self.categorie  = categorie  or "Autre"
        self.adresse    = adresse    or ""
        self.fonction   = fonction   or ""
        self.entreprise = entreprise or ""

    def __str__(self):
        return (f"{self.nom} | {self.email} | {self.num} | "
                f"{self.categorie} | {self.entreprise}")

    def __repr__(self):
        return (f"Contact({self.nom!r}, {self.email!r}, {self.num!r}, "
                f"categorie={self.categorie!r})")

    def to_dict(self):
        return {
            "nom":        self.nom,
            "email":      self.email,
            "num":        self.num,
            "categorie":  self.categorie,
            "adresse":    self.adresse,
            "fonction":   self.fonction,
            "entreprise": self.entreprise,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            nom        = data.get("nom",        ""),
            email      = data.get("email",      ""),
            num        = data.get("num",        ""),
            categorie  = data.get("categorie",  "Autre"),
            adresse    = data.get("adresse",    ""),
            fonction   = data.get("fonction",   ""),
            entreprise = data.get("entreprise", ""),
        )

