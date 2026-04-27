import re
import os
import json

from contact import Contact

class AdressBook:
    # def __init__(self):
    #     self.contacts = []

    # def add_contact(self, contact: Contact):
    #     if contact in self.contacts:
    #         print("Ce contact existe déjà dans le carnet d'adresses.")
    #         return
    #     for con in self.contacts:
    #         if con.nom.lower() == contact.nom.lower():
    #             print("Un contact avec ce nom existe déjà dans le carnet d'adresses.")
    #             return
    #         elif con.email.lower() == contact.email.lower():
    #             print("Un contact avec cet email existe déjà dans le carnet d'adresses.")
    #             return
    #         elif con.numéro.lower() == contact.numéro.lower():
    #             print("Un contact avec ce numéro existe déjà dans le carnet d'adresses.")
    #             return
    
    #     self.contacts.append(contact)
    #     print("Contact ajouté avec succès !")

    # def remove_contact(self, value: str):
    #     #type_value = "nom"

    #     regex = r"^[a-zA-Z\s]+$"
    #     regex_email = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    #     regex_numéro = r"^(06|07)\d{8}$"


    #     if re.fullmatch(regex, value) is not None:
    #         #type_value = "nom"
    #         for con in self.contacts:
    #             if con.nom.lower() == value.lower():
    #                 self.contacts.remove(con)
    #                 print("Contact supprimé avec succès!")
    #                 return
    #         print("Contact introuvable !")

    #     elif re.fullmatch(regex_email, value) is not None:
    #         #type_value = "email"
    #         for con in self.contacts:
    #             if con.email.lower() == value.lower():
    #                 self.contacts.remove(con)
    #                 print("Contact supprimé avec succès!")
    #                 return
    #         print("Contact introuvable !")

    #     elif re.fullmatch(regex_numéro, value) is not None:
    #         #type_value = "numéro"   
    #         for con in self.contacts:                
    #             if con.numéro.lower() == value.lower():
    #                 self.contacts.remove(con)
    #                 print("Contact supprimé avec succès!")
    #                 return
    #         print("Contact introuvable !")
    #     else:
    #         print("La valeur fournie n'est pas valide.")
    #         return
        

    # def display_contacts(self):
    #     if not self.contacts:
    #         print("Le carnet d'adresses est vide.")
    #     else:
    #         print("\nListe des contacts :")
    #         print("-" * 50)
    #         for i, contact in enumerate(self.contacts, 1):
    #             print(f"{i}. {contact}")
    #         print("-" * 50)

    def __init__(self, fichier = "contacts.json"):
        self.contacts = []
        self.fichier = fichier
        if not os.path.exists(self.fichier):
            open(self.fichier, "w").close()

    

    def add_contact(self, contact: Contact):
        if contact in self.contacts:
            print("Ce contact existe déjà dans le carnet d'adresses.")
            return
        for con in self.contacts:
            if con.nom.lower() == contact.nom.lower():
                print("Un contact avec ce nom existe déjà dans le carnet d'adresses.")
                return
            elif con.email.lower() == contact.email.lower():
                print("Un contact avec cet email existe déjà dans le carnet d'adresses.")
                return
            elif con.numéro.lower() == contact.numéro.lower():
                print("Un contact avec ce numéro existe déjà dans le carnet d'adresses.")
                return
    
        self.contacts.append(contact)
        self.save_to_file()
        print("Contact ajouté avec succès !")

    def remove_contact(self, value: str):
        #type_value = "nom" 
        regex = r"^[a-zA-Z\s]+$"
        regex_email = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        regex_numéro = r"^(06|07)\d{8}$"

        self.load_from_file()
        new_contacts = []
        found = False

        if re.fullmatch(regex, value) is not None:
           for c in self.contacts:
               if c["nom"].lower() != value.lower():
                   new_contacts.append(c)
               else :
                   found = True

        
        
        self.contacts = new_contacts
        self.save_to_file()

        if found:
            print("Contact supprimé avec succès!")
        else : 
            print("Contact introuvable !")

       



        # if re.fullmatch(regex, value) is not None:
        #     #type_value = "nom"
        #     for con in self.contacts:
        #         if con.nom.lower() == value.lower():
        #             self.contacts.remove(con)
        #             print("Contact supprimé avec succès!")
        #             return
        #     print("Contact introuvable !")

        # elif re.fullmatch(regex_email, value) is not None:
        #     #type_value = "email"
        #     for con in self.contacts:
        #         if con.email.lower() == value.lower():
        #             self.contacts.remove(con)
        #             print("Contact supprimé avec succès!")
        #             return
        #     print("Contact introuvable !")

        # elif re.fullmatch(regex_numéro, value) is not None:
        #     #type_value = "numéro"   
        #     for con in self.contacts:                
        #         if con.numéro.lower() == value.lower():
        #             self.contacts.remove(con)
        #             print("Contact supprimé avec succès!")
        #             return
        #     print("Contact introuvable !")
        # else:
        #     print("La valeur fournie n'est pas valide.")
        #     return
        

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

    def save_to_file(self, filename="contacts.json"): 
       contacts_dict_list = [contact.to_dict() for contact in self.contacts] 
       try: 
           with open(filename, 'w', encoding='utf-8') as file: 
               json.dump(contacts_dict_list, file, indent=4, ensure_ascii=False) 
               print(f"Donnees sauvegardees avec succes dans {filename}") 
       except Exception as e: 
           print(f"Erreur lors de la sauvegarde : {e}") 

    def load_from_file(self, filename="contacts.json"):  
        try: 
            with open (filename, 'r' , encoding=' utf-8') as file: 
                contacts_dict_list = json.load(file)
            self.contacts = [] 
            for data in contacts_dict_list: 
                contact = Contact.from_dict(self,data) 
                self.contacts.append(contact) 
                print(f"Donnees chargees avec succes depuis {filename}") 
        except FileNotFoundError: 
            print("Aucun fichier de sauvegarde trouve. Demarrage avec un carnet vide.") 
        except json.JSONDecodeError: 
            print("Erreur : Le fichier de sauvegarde est corrompu.") 

