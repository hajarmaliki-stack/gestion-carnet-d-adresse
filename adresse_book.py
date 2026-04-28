import os
import json

from contact import Contact

class AdressBook:
    def __init__(self, fichier="contacts.json"):
        self.contacts = []
        self.fichier = fichier
        if not os.path.exists(self.fichier):
            open(self.fichier, "w", encoding='utf-8').close()

    def add_contact(self, contact: Contact):
        self.load_from_file()
        for con in self.contacts:
            if con.nom.lower() == contact.nom.lower():
                print("Un contact avec ce nom existe déjà dans le carnet d'adresses.")
                return False
            elif con.numéro.lower() == contact.numéro.lower():
                print("Un contact avec ce numéro existe déjà dans le carnet d'adresses.")
                return False
    
        self.contacts.append(contact)
        self.save_to_file()
        print("Contact ajouté avec succès !")
        return True

    def remove_contact(self, value: str):
        self.load_from_file()
        new_contacts = []
        found = False

        for c in self.contacts:
            if c.nom.lower() != value.lower() and c.numéro.lower() != value.lower():
                new_contacts.append(c)
            else:
                found = True
        
        self.contacts = new_contacts
        self.save_to_file()

        if found:
            print("Contact supprimé avec succès!")
        else: 
            print("Contact introuvable !")
        return found

    def display_contacts(self):
        self.load_from_file()
        if not self.contacts:
            print("Le carnet d'adresses est vide.")
        else:
            print("\nListe des contacts :")
            print("-" * 50)
            for i, contact in enumerate(self.contacts, 1):
                print(f"{i}. {contact}")
            print("-" * 50)

    def save_to_file(self): 
        contacts_dict_list = [contact.to_dict() for contact in self.contacts] 
        try: 
            with open(self.fichier, 'w', encoding='utf-8') as file: 
                json.dump(contacts_dict_list, file, indent=4, ensure_ascii=False) 
        except Exception as e: 
            print(f"Erreur lors de la sauvegarde : {e}") 

    def load_from_file(self):  
        try: 
            with open(self.fichier, 'r', encoding='utf-8') as file: 
                content = file.read().strip()
                if not content:
                    self.contacts = []
                    return
                contacts_dict_list = json.loads(content)
            self.contacts = [] 
            for data in contacts_dict_list: 
                contact = Contact.from_dict(data) 
                self.contacts.append(contact) 
        except FileNotFoundError: 
            print("Aucun fichier de sauvegarde trouve. Demarrage avec un carnet vide.") 
            self.contacts = []
        except json.JSONDecodeError: 
            print("Erreur : Le fichier de sauvegarde est corrompu.") 
            self.contacts = []
