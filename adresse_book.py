import re

from contact import Contact

class AdressBook:
    def __init__(self):
        self.contacts = []

    def add_contact(self, contact: Contact):
        self.contacts.append(contact)
        print("Contact ajouté avec succès !")

    def remove_contact(self, value: str):
        #type_value = "nom"

        regex = r"^[a-zA-Z\s]+$"
        regex_email = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        regex_numéro = r"^(06|07)\d{8}$"


        if re.fullmatch(regex, value) is not None:
            #type_value = "nom"
            for con in self.contacts:
                if con.nom.lower() == value.lower():
                    self.contacts.remove(con)
                    print("Contact supprimé avec succès!")
                    return
            print("Contact introuvable !")

        elif re.fullmatch(regex_email, value) is not None:
            #type_value = "email"
            for con in self.contacts:
                if con.email.lower() == value.lower():
                    self.contacts.remove(con)
                    print("Contact supprimé avec succès!")
                    return
            print("Contact introuvable !")

        elif re.fullmatch(regex_numéro, value) is not None:
            #type_value = "numéro"   
            for con in self.contacts:                
                if con.numéro.lower() == value.lower():
                    self.contacts.remove(con)
                    print("Contact supprimé avec succès!")
                    return
            print("Contact introuvable !")
        else:
            print("La valeur fournie n'est pas valide.")
            return
        

    def display_contacts(self):
        if not self.contacts:
            print("Le carnet d'adresses est vide.")
        else:
            print("\nListe des contacts :")
            print("-" * 50)
            for i, contact in enumerate(self.contacts, 1):
                print(f"{i}. {contact}")
            print("-" * 50)



