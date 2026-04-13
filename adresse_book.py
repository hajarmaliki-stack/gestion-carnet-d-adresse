from contact import Contact

class AdressBook:
    def __init__(self):
        self.contacts = []

    def add_contact(self, contact: Contact):
        self.contacts.append(contact)
        print("Contact ajouté avec succès !")

    def remove_contact(self, name: str):
        for con in self.contacts:
            if con.nom.lower() == name.lower():
                self.contacts.remove(con)
                print("Contact supprimé avec succès !")
                return

        print("Contact introuvable !")

    def display_contacts(self):
        if not self.contacts:
            print("Le carnet d'adresses est vide.")
        else:
            print("\nListe des contacts :")
            print("-" * 50)
            for i, contact in enumerate(self.contacts, 1):
                print(f"{i}. {contact}")
            print("-" * 50)


    



