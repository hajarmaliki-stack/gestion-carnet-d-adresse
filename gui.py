import tkinter as tk
from tkinter import messagebox
from adresse_book import AdressBook
from contact import Contact
from rdv_gui import RendezvousWindow

class ContactViewInterface:
    def get_contact_input(self) -> dict:
        raise NotImplementedError

    def set_contact_input(self, nom: str, email: str, tel: str):
        raise NotImplementedError

    def clear_inputs(self):
        raise NotImplementedError

    def show_contacts(self, contacts: list):
        raise NotImplementedError

    def show_error(self, title: str, message: str):
        raise NotImplementedError

    def show_warning(self, title: str, message: str):
        raise NotImplementedError

    def show_info(self, title: str, message: str):
        raise NotImplementedError

    def get_selected_contact(self) -> str:
        raise NotImplementedError

    def confirm_deletion(self, nom: str) -> bool:
        raise NotImplementedError

    def open_rdv_manager(self, selected_name: str):
        raise NotImplementedError


class ContactPresenter:
    def __init__(self, view: ContactViewInterface, model: AdressBook):
        self.view = view
        self.model = model

    def on_load(self):
        self.model.load_contacts()
        self.view.show_contacts(self.model.contacts)

    def on_clear_clicked(self):
        self.view.clear_inputs()

    def on_add_clicked(self):
        data = self.view.get_contact_input()
        nom = data.get("nom", "").strip()
        email = data.get("email", "").strip()
        tel = data.get("tel", "").strip()

        if not nom or not email or not tel:
            self.view.show_warning("Avertissement", "Veuillez remplir tous les champs.")
            return

        try:
            contact = Contact(nom, email, tel)
            success = self.model.add_contact(contact)
            if success:
                self.on_load()
                self.view.clear_inputs()
            else:
                self.view.show_error("Erreur", "Le contact existe déjà.")
        except AssertionError as e:
            self.view.show_error("Erreur", str(e))

    def on_delete_clicked(self):
        nom_selected = self.view.get_selected_contact()
        if nom_selected:
            confirm = self.view.confirm_deletion(nom_selected)
            if confirm:
                self.model.remove_contact(nom_selected)
                self.on_load()
                self.view.clear_inputs()
        else:
            self.view.show_warning("Avertissement", "Veuillez sélectionner un contact à supprimer.")

    def on_select(self, nom_selected: str):
        for c in self.model.contacts:
            if c.nom == nom_selected:
                self.view.set_contact_input(c.nom, c.email, c.num)
                break

    def on_export_clicked(self):
        success = self.model.export_to_csv()
        if success:
            self.view.show_info("Succès", "Les contacts ont été exportés avec succès !")
        else:
            self.view.show_error("Erreur", "Une erreur est survenue lors de l'exportation.")

    def on_rdv_clicked(self):
        data = self.view.get_contact_input()
        selected_name = data.get("nom", "").strip()
        self.view.open_rdv_manager(selected_name)


class Contact_GUI(ContactViewInterface):
    def __init__(self, root):
        self.root = root
        self.root.title("Contact's Carnet!")
        
        # Dimensions
        self.root.geometry("520x480")
        self.root.resizable(True, True)
        
        # Background color
        self.bg_color = "#f0f0f0"
        self.root.configure(bg=self.bg_color)
        
        self.presenter = ContactPresenter(self, AdressBook())
        
        # Main container
        mainframe = tk.Frame(root, padx=10, pady=10, bg=self.bg_color)
        mainframe.pack(fill=tk.BOTH, expand=True)
        
        # --- frameH (Top Frame) ---
        frameH = tk.Frame(mainframe, bd=2, relief=tk.GROOVE, padx=10, pady=10)
        frameH.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(frameH, text="Nom :").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.nom_var = tk.StringVar()
        self.nom_entry = tk.Entry(frameH, textvariable=self.nom_var, width=25)
        self.nom_entry.grid(row=0, column=1, sticky=tk.E, padx=(5, 0), pady=5)
        
        tk.Label(frameH, text="Email :").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.email_var = tk.StringVar()
        self.email_entry = tk.Entry(frameH, textvariable=self.email_var, width=25)
        self.email_entry.grid(row=1, column=1, sticky=tk.E, padx=(5, 0), pady=5)

        tk.Label(frameH, text="Tel :").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.tel_var = tk.StringVar()
        self.tel_entry = tk.Entry(frameH, textvariable=self.tel_var, width=25)
        self.tel_entry.grid(row=2, column=1, sticky=tk.E, padx=(5, 0), pady=5)
        
        # Effacer button centered below inputs
        self.btn_effacer = tk.Button(frameH, text="Effacer", command=self.presenter.on_clear_clicked, width=10)
        self.btn_effacer.grid(row=3, column=0, columnspan=2, pady=(10, 0))
        
        frameH.grid_columnconfigure(0, weight=1)
        frameH.grid_columnconfigure(1, weight=3)
        
        # --- frameM (Middle Frame) ---
        frameM = tk.Frame(mainframe, bd=2, relief=tk.GROOVE)
        frameM.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.listbox = tk.Listbox(frameM, selectmode=tk.SINGLE, activestyle='dotbox')
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        scrollbar = tk.Scrollbar(frameM, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)
        
        self.listbox.bind('<<ListboxSelect>>', self.on_listbox_select)
        
        # --- frameB (Bottom Frame) ---
        frameB = tk.Frame(mainframe, bd=2, relief=tk.GROOVE, padx=5, pady=5)
        frameB.pack(fill=tk.X)
        
        self.btn_ajouter = tk.Button(frameB, text="Ajouter", command=self.presenter.on_add_clicked, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        self.btn_ajouter.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2, pady=2, ipady=2)
        
        self.btn_supprimer = tk.Button(frameB, text="Supprimer", command=self.presenter.on_delete_clicked, bg="#F44336", fg="white", font=("Arial", 10, "bold"))
        self.btn_supprimer.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2, pady=2, ipady=2)
        
        self.btn_afficher = tk.Button(frameB, text="Afficher", command=self.presenter.on_load, bg="#2196F3", fg="white", font=("Arial", 10, "bold"))
        self.btn_afficher.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2, pady=2, ipady=2)
        
        self.btn_exporter = tk.Button(frameB, text="Exporter CSV", command=self.presenter.on_export_clicked, bg="#FF9800", fg="white", font=("Arial", 10, "bold"))
        self.btn_exporter.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2, pady=2, ipady=2)
        
        self.btn_rdv = tk.Button(frameB, text="Gérer RDVs", command=self.presenter.on_rdv_clicked, bg="#9C27B0", fg="white", font=("Arial", 10, "bold"))
        self.btn_rdv.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2, pady=2, ipady=2)
        
        # Initialize listbox
        self.presenter.on_load()

    # --- View Interface Implementations ---
    def get_contact_input(self) -> dict:
        return {
            "nom": self.nom_var.get(),
            "email": self.email_var.get(),
            "tel": self.tel_var.get()
        }

    def set_contact_input(self, nom: str, email: str, tel: str):
        self.nom_var.set(nom)
        self.email_var.set(email)
        self.tel_var.set(tel)

    def clear_inputs(self):
        self.nom_var.set("")
        self.email_var.set("")
        self.tel_var.set("")
        self.listbox.selection_clear(0, tk.END)

    def show_contacts(self, contacts: list):
        self.listbox.delete(0, tk.END)
        for contact in contacts:
            self.listbox.insert(tk.END, contact.nom)

    def show_error(self, title: str, message: str):
        messagebox.showerror(title, message)

    def show_warning(self, title: str, message: str):
        messagebox.showwarning(title, message)

    def show_info(self, title: str, message: str):
        messagebox.showinfo(title, message)

    def get_selected_contact(self) -> str:
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            return self.listbox.get(index)
        return ""

    def confirm_deletion(self, nom: str) -> bool:
        return messagebox.askyesno("Confirmation", f"Êtes-vous sûr de vouloir supprimer '{nom}' ?")

    def open_rdv_manager(self, selected_name: str):
        RendezvousWindow(self.root, initial_contact_nom=selected_name if selected_name else None)

    def on_listbox_select(self, event):
        selected = self.get_selected_contact()
        if selected:
            self.presenter.on_select(selected)


if __name__ == "__main__":
    from auth_gui import show_login
    
    if show_login():
        root = tk.Tk()
        app = Contact_GUI(root)
        root.mainloop()
    else:
        print("Authentification requise. Fermeture de l'application.")
