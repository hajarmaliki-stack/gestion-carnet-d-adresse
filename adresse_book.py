import os
import csv
import sqlite3

from contact import Contact
from database import get_connection

# Colonnes complètes (Partie 8)
_COLS = "nom, email, num, categorie, adresse, fonction, entreprise"


class AdressBook:
    def __init__(self):
        self.contacts = []
        self.load_contacts()

    def add_contact(self, contact: Contact):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                f"INSERT INTO contacts ({_COLS}) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (contact.nom, contact.email, contact.num,
                 contact.categorie, contact.adresse,
                 contact.fonction, contact.entreprise)
            )
            conn.commit()
            self.load_contacts()
            return True, ""
        except Exception as e:
            err = str(e).lower()
            # Détecter quel champ est en doublon
            email_dup = "email" in err
            num_dup   = any(x in err for x in ["num", "phone", "téléphone"])
            # Vérifier manuellement si email ou num existe déjà
            cursor2 = conn.cursor()
            cursor2.execute("SELECT email, num FROM contacts WHERE email=? OR num=?",
                            (contact.email, contact.num))
            rows = cursor2.fetchall()
            existing_emails = {r[0] for r in rows}
            existing_nums   = {r[1] for r in rows}
            email_dup = contact.email in existing_emails
            num_dup   = contact.num   in existing_nums
            if email_dup and num_dup:
                msg = "Cet email ET ce numéro de téléphone existent déjà."
            elif email_dup:
                msg = f"L'email '{contact.email}' est déjà utilisé par un autre contact."
            elif num_dup:
                msg = f"Le numéro '{contact.num}' est déjà utilisé par un autre contact."
            else:
                msg = "Ce contact existe déjà (doublon détecté)."
            return False, msg
        finally:
            conn.close()

    def remove_contact(self, value: str):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM contacts WHERE nom = ? OR num = ?", (value, value))
        row = cursor.fetchone()

        if row:
            cursor.execute("DELETE FROM contacts WHERE id = ?", (row[0],))
            conn.commit()
            print("Contact supprimé avec succès!")
            found = True
        else:
            print("Contact introuvable !")
            found = False

        conn.close()
        self.load_contacts()
        return found

    def display_contacts(self):
        self.load_contacts()
        if not self.contacts:
            print("Le carnet d'adresses est vide.")
        else:
            print("\nListe des contacts :")
            print("-" * 60)
            for i, contact in enumerate(self.contacts, 1):
                print(f"{i}. {contact}")
            print("-" * 60)

    def load_contacts(self):
        """Récupère tous les contacts depuis la base de données SQLite."""
        self.contacts = []
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(f"SELECT {_COLS} FROM contacts")
        rows = cursor.fetchall()

        for row in rows:
            self.contacts.append(Contact(
                nom=row[0], email=row[1], num=row[2],
                categorie=row[3]  if len(row) > 3 else "Autre",
                adresse=row[4]    if len(row) > 4 else "",
                fonction=row[5]   if len(row) > 5 else "",
                entreprise=row[6] if len(row) > 6 else "",
            ))

        conn.close()

    def export_to_csv(self, filename="contacts.csv"):
        """Exporte tous les contacts vers un fichier CSV."""
        self.load_contacts()
        try:
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Nom", "Email", "Téléphone",
                                 "Catégorie", "Adresse", "Fonction", "Entreprise"])
                for c in self.contacts:
                    writer.writerow([c.nom, c.email, c.num,
                                     c.categorie, c.adresse, c.fonction, c.entreprise])
            print(f"Contacts exportés avec succès dans '{filename}'.")
            return True
        except Exception as e:
            print(f"Erreur lors de l'exportation : {e}")
            return False

    def update_contact(self, old_nom, new_contact: Contact):
        """Met à jour un contact existant."""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """UPDATE contacts
                   SET nom=?, email=?, num=?,
                       categorie=?, adresse=?, fonction=?, entreprise=?
                   WHERE nom=?""",
                (new_contact.nom, new_contact.email, new_contact.num,
                 new_contact.categorie, new_contact.adresse,
                 new_contact.fonction, new_contact.entreprise,
                 old_nom)
            )
            conn.commit()
            success = cursor.rowcount > 0
            msg = ""
        except sqlite3.IntegrityError:
            # Vérifier quel champ est en doublon
            cursor2 = conn.cursor()
            cursor2.execute(
                "SELECT email, num FROM contacts WHERE (email=? OR num=?) AND nom != ?",
                (new_contact.email, new_contact.num, old_nom)
            )
            rows = cursor2.fetchall()
            existing_emails = {r[0] for r in rows}
            existing_nums   = {r[1] for r in rows}
            email_dup = new_contact.email in existing_emails
            num_dup   = new_contact.num   in existing_nums
            if email_dup and num_dup:
                msg = "Cet email ET ce numéro de téléphone existent déjà."
            elif email_dup:
                msg = f"L'email '{new_contact.email}' est déjà utilisé par un autre contact."
            elif num_dup:
                msg = f"Le numéro '{new_contact.num}' est déjà utilisé par un autre contact."
            else:
                msg = "Doublon détecté lors de la mise à jour."
            success = False
        finally:
            conn.close()

        if success:
            self.load_contacts()
        return success, msg

    def search_contact(self, query):
        """Recherche des contacts par nom, numéro, catégorie ou entreprise."""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            f"""SELECT {_COLS} FROM contacts
                WHERE nom LIKE ? OR num LIKE ?
                   OR categorie LIKE ? OR entreprise LIKE ?""",
            (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%")
        )
        rows = cursor.fetchall()
        conn.close()

        return [Contact(
            nom=row[0], email=row[1], num=row[2],
            categorie=row[3]  if len(row) > 3 else "Autre",
            adresse=row[4]    if len(row) > 4 else "",
            fonction=row[5]   if len(row) > 5 else "",
            entreprise=row[6] if len(row) > 6 else "",
        ) for row in rows]

    def filter_by_category(self, categorie: str):
        """Filtre les contacts par catégorie."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT {_COLS} FROM contacts WHERE categorie = ?", (categorie,)
        )
        rows = cursor.fetchall()
        conn.close()

        return [Contact(
            nom=row[0], email=row[1], num=row[2],
            categorie=row[3], adresse=row[4],
            fonction=row[5], entreprise=row[6],
        ) for row in rows]

    def get_contact_by_name(self, nom):
        """Récupère l'ID et les détails d'un contact par son nom."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nom, email, num FROM contacts WHERE nom = ?", (nom,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {"id": row[0], "nom": row[1], "email": row[2], "num": row[3]}
        return None

    def get_rendezvous_for_date(self, date):
        """Récupère tous les rendez-vous pour une date donnée (format YYYY-MM-DD)."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT r.heure, c.id, c.nom, c.email, c.num
               FROM rendezvous r
               JOIN contacts c ON r.contact_id = c.id
               WHERE r.date = ?""",
            (date,)
        )
        rows = cursor.fetchall()
        conn.close()
        
        res = {}
        for row in rows:
            res[row[0]] = {
                "id": row[1],
                "nom": row[2],
                "email": row[3],
                "num": row[4]
            }
        return res

    def add_rendezvous(self, contact_id, date, heure):
        """Enregistre un nouveau rendez-vous."""
        conn = get_connection()
        cursor = conn.cursor()
        success = False
        try:
            cursor.execute(
                "INSERT INTO rendezvous (contact_id, date, heure) VALUES (?, ?, ?)",
                (contact_id, date, heure)
            )
            conn.commit()
            success = True
        except sqlite3.IntegrityError:
            pass  # Le créneau est déjà pris
        finally:
            conn.close()
        return success

    def delete_rendezvous(self, date, heure):
        """Supprime un rendez-vous pour une date et une heure données."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM rendezvous WHERE date = ? AND heure = ?", (date, heure))
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success