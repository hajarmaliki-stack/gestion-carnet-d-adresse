import tkinter as tk
from tkinter import ttk, messagebox
import re
from adresse_book import AdressBook
from contact import Contact

class Contact_GUI:
    def __init__(self, root):
        self.book = AdressBook()
        self.book.load_from_file()
        
        self.root = root
        self.root.title("Contact's Carnet!")
        
        # Dimensions
        self.root.geometry("350x450")
        self.root.resizable(True, True)
        
        # Background color
        self.bg_color = "#f0f0f0"
        self.root.configure(bg=self.bg_color)
        
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
        self.btn_effacer = tk.Button(frameH, text="Effacer", command=self.effacer, width=10)
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
        
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        
        # --- frameB (Bottom Frame) ---
        frameB = tk.Frame(mainframe, bd=2, relief=tk.GROOVE, padx=5, pady=5)
        frameB.pack(fill=tk.X)
        
        self.btn_ajouter = tk.Button(frameB, text="Ajouter", command=self.ajouter, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        self.btn_ajouter.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2, pady=2, ipady=2)
        
        self.btn_supprimer = tk.Button(frameB, text="Supprimer", command=self.supprimer, bg="#F44336", fg="white", font=("Arial", 10, "bold"))
        self.btn_supprimer.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2, pady=2, ipady=2)
        
        self.btn_afficher = tk.Button(frameB, text="Afficher", command=self.afficher, bg="#2196F3", fg="white", font=("Arial", 10, "bold"))
        self.btn_afficher.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2, pady=2, ipady=2)
        
        # Initialize listbox
        self.afficher()

    def effacer(self):
        self.nom_var.set("")
        self.email_var.set("")
        self.tel_var.set("")
        self.listbox.selection_clear(0, tk.END)

    def ajouter(self):
        nom = self.nom_var.get().strip()
        email = self.email_var.get().strip()
        tel = self.tel_var.get().strip()
        
        if not nom or not email or not tel:
            messagebox.showwarning("Avertissement", "Veuillez remplir tous les champs.")
            return

        try:
            contact = Contact(nom, email, tel)
            success = self.book.add_contact(contact)
            if success:
                self.afficher()
                self.effacer()
            else:
                messagebox.showerror("Erreur", "Le contact existe déjà.")
        except AssertionError as e:
            messagebox.showerror("Erreur", str(e))
            
    def supprimer(self):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            nom = self.listbox.get(index)
            
            # Confirm deletion
            confirm = messagebox.askyesno("Confirmation", f"Êtes-vous sûr de vouloir supprimer '{nom}' ?")
            if confirm:
                self.book.remove_contact(nom)
                self.afficher()
                self.effacer()
        else:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un contact à supprimer.")

    def afficher(self):
        self.listbox.delete(0, tk.END)
        self.book.load_from_file()
        for contact in self.book.contacts:
            self.listbox.insert(tk.END, contact.nom)

    def on_select(self, event):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            nom_selected = self.listbox.get(index)
            for c in self.book.contacts:
                if c.nom == nom_selected:
                    self.nom_var.set(c.nom)
                    self.email_var.set(c.email)
                    self.tel_var.set(c.numéro)
                    break

if __name__ == "__main__":
    root = tk.Tk()
    app = Contact_GUI(root)
    root.mainloop()
