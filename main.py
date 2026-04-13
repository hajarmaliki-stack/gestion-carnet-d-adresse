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

        if choice == "1":
            nom  = input("Nom       : ").strip()
            email = input("Email     : ").strip()
            numéro = input("Téléphone : ").strip()
            try:
                book.add_contact(Contact(nom, email, numéro))
            except AssertionError as err:
                print(f"Erreur : {err}")

        elif choice == "2":
            nom = input("Nom du contact à supprimer : ").strip()
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
