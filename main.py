import re

from contact import Contact
from adresse_book import AdressBook


def main():
    book = AdressBook()

    print("=" * 40)
    print("   Carnet d'Adresses")
    print("=" * 40)

    while True:
        print("\nMenu :")
        print("  1. Add Contact")
        print("  2. Remove Contact")
        print("  3. Display Contacts")
        print("  4. Quit")

        choice = input("\nVotre choix : ").strip()

        regex_nom = r"^[a-zA-Z\s]+$"
        regex_email = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        regex_numéro = r"^(06|07)\d{8}$"

        if choice == "1":

            nom  = input("Nom       : ").strip()
            if re.fullmatch(regex_nom, nom) is None:
                print("Erreur : Le nom doit être une chaîne non vide composée de lettres et d'espaces.")
                continue


            email = input("Email     : ").strip()
            if re.fullmatch(regex_email, email) is None:
                print("Erreur : L'email doit être une adresse email valide.")
                continue

            numéro = input("Téléphone : ").strip()
            if re.fullmatch(regex_numéro, numéro) is None:
                print("Erreur : Le numéro de téléphone doit être une chaîne de 10 chiffres commençant par 06 ou 07.")
                continue

            try:
                book.add_contact(Contact(nom, email, numéro))
            except AssertionError as err:
                print(f"Erreur : {err}")

        elif choice == "2":
            nom = input("Nom de contact à supprimer : ").strip()
            book.remove_contact(nom)

        elif choice == "3":
            book.display_contacts()

        elif choice == "4":
            print("👋 Au revoir !")
            break

        else:
            print(" Choix invalide. Veuillez entrer 1, 2, 3 ou 4.")


if __name__ == "__main__":
    main()
