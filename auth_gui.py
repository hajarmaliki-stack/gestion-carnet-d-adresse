import tkinter as tk
from tkinter import messagebox
from auth import Authenticator

class LoginViewInterface:
    def get_username(self) -> str:
        raise NotImplementedError
        
    def get_password(self) -> str:
        raise NotImplementedError
        
    def show_warning(self, title: str, message: str):
        raise NotImplementedError
        
    def show_error(self, title: str, message: str):
        raise NotImplementedError
        
    def clear_password(self):
        raise NotImplementedError
        
    def set_success(self, success: bool):
        raise NotImplementedError
        
    def destroy_view(self):
        raise NotImplementedError


class LoginPresenter:
    def __init__(self, view: LoginViewInterface, auth_model: Authenticator):
        self.view = view
        self.auth_model = auth_model
        
    def on_login_clicked(self):
        username = self.view.get_username().strip()
        password = self.view.get_password()
        
        if not username or not password:
            self.view.show_warning("Avertissement", "Veuillez remplir tous les champs.")
            return
            
        if self.auth_model.verify_credentials(username, password):
            self.view.set_success(True)
            self.view.destroy_view()
        else:
            self.view.show_error("Erreur", "Identifiants incorrects.")
            self.view.clear_password()
            
    def on_close(self):
        self.view.set_success(False)
        self.view.destroy_view()


class LoginWindow(LoginViewInterface):
    def __init__(self, root):
        self.root = root
        self.root.title("Connexion Administrateur")
        self.root.geometry("300x200")
        self.root.resizable(False, False)
        
        self.success = False
        self.presenter = LoginPresenter(self, Authenticator())
        
        # Centrer la fenêtre
        self.root.eval('tk::PlaceWindow . center')
        
        # Interface
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True, fill=tk.BOTH)
        
        tk.Label(frame, text="Nom d'utilisateur :").pack(anchor=tk.W, pady=(0, 5))
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(frame, text="Mot de passe :").pack(anchor=tk.W, pady=(0, 5))
        self.password_entry = tk.Entry(frame, show="*", width=30)
        self.password_entry.pack(fill=tk.X, pady=(0, 15))
        
        self.login_btn = tk.Button(frame, text="Se Connecter", command=self.presenter.on_login_clicked, bg="#2196F3", fg="white", font=("Arial", 10, "bold"))
        self.login_btn.pack(fill=tk.X)
        
        # Lier la touche Entrée au bouton de connexion
        self.root.bind('<Return>', lambda event: self.presenter.on_login_clicked())
        
        # Gérer la fermeture de la fenêtre
        self.root.protocol("WM_DELETE_WINDOW", self.presenter.on_close)

    def get_username(self) -> str:
        return self.username_entry.get()

    def get_password(self) -> str:
        return self.password_entry.get()

    def show_warning(self, title: str, message: str):
        messagebox.showwarning(title, message)

    def show_error(self, title: str, message: str):
        messagebox.showerror(title, message)

    def clear_password(self):
        self.password_entry.delete(0, tk.END)

    def set_success(self, success: bool):
        self.success = success

    def destroy_view(self):
        self.root.destroy()


def show_login():
    root = tk.Tk()
    login_app = LoginWindow(root)
    root.mainloop()
    return login_app.success


if __name__ == "__main__":
    if show_login():
        print("Connexion réussie ! Lancement de l'application...")
    else:
        print("Connexion échouée ou annulée.")
