import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import add_banker, get_clients_of_banker, authenticate_banker
import re
import hashlib

class BankerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des Banquiers")

        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self.root, text="Créer un compte banquier")
        self.label.pack(pady=10)

        self.nom_label = ttk.Label(self.root, text="Nom:")
        self.nom_label.pack(pady=5)
        self.nom_entry = ttk.Entry(self.root)
        self.nom_entry.pack(pady=5)

        self.prenom_label = ttk.Label(self.root, text="Prénom:")
        self.prenom_label.pack(pady=5)
        self.prenom_entry = ttk.Entry(self.root)
        self.prenom_entry.pack(pady=5)

        self.email_label = ttk.Label(self.root, text="Email:")
        self.email_label.pack(pady=5)
        self.email_entry = ttk.Entry(self.root)
        self.email_entry.pack(pady=5)

        self.mot_de_passe_label = ttk.Label(self.root, text="Mot de passe:")
        self.mot_de_passe_label.pack(pady=5)
        self.mot_de_passe_entry = ttk.Entry(self.root, show="*")
        self.mot_de_passe_entry.pack(pady=5)

        self.add_button = ttk.Button(self.root, text="S'inscrire", command=self.add_banker)
        self.add_button.pack(pady=10)

        self.login_label = ttk.Label(self.root, text="Connexion Banquier")
        self.login_label.pack(pady=10)

        self.login_email_label = ttk.Label(self.root, text="Email:")
        self.login_email_label.pack(pady=5)
        self.login_email_entry = ttk.Entry(self.root)
        self.login_email_entry.pack(pady=5)

        self.login_password_label = ttk.Label(self.root, text="Mot de passe:")
        self.login_password_label.pack(pady=5)
        self.login_password_entry = ttk.Entry(self.root, show="*")
        self.login_password_entry.pack(pady=5)

        self.login_button = ttk.Button(self.root, text="Se connecter", command=self.login)
        self.login_button.pack(pady=10)

    def validate_password(self, password):
        if len(password) > 10:
            return False, "Le mot de passe ne doit pas dépasser 10 caractères."
        if not re.search(r"[A-Z]", password):
            return False, "Le mot de passe doit contenir au moins une majuscule."
        if not re.search(r"[a-z]", password):
            return False, "Le mot de passe doit contenir au moins une minuscule."
        if not re.search(r"[0-9]", password):
            return False, "Le mot de passe doit contenir au moins un chiffre."
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "Le mot de passe doit contenir au moins un caractère spécial."
        return True, ""

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def add_banker(self):
        nom = self.nom_entry.get()
        prenom = self.prenom_entry.get()
        email = self.email_entry.get()
        mot_de_passe = self.mot_de_passe_entry.get()

        valid, message = self.validate_password(mot_de_passe)
        if not valid:
            messagebox.showwarning("Erreur", message)
            return

        hashed_password = self.hash_password(mot_de_passe)

        if nom and prenom and email and mot_de_passe:
            try:
                add_banker(nom, prenom, email, hashed_password)
                messagebox.showinfo("Succès", "Banquier ajouté avec succès!")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'ajout du banquier : {e}")
        else:
            messagebox.showwarning("Erreur", "Tous les champs sont obligatoires!")

    def login(self):
        email = self.login_email_entry.get()
        mot_de_passe = self.login_password_entry.get()
        hashed_password = self.hash_password(mot_de_passe)

        banker = authenticate_banker(email, hashed_password)
        if banker:
            messagebox.showinfo("Succès", "Connexion réussie!")
            self.view_clients(banker[0])  # Récupérer ID_banker
        else:
            messagebox.showerror("Erreur", "Email ou mot de passe incorrect.")

    def view_clients(self, ID_banker):
        clients = get_clients_of_banker(ID_banker)
        self.clients_window = tk.Toplevel(self.root)
        self.clients_window.title("Liste des clients attribués")

        self.tree = ttk.Treeview(self.clients_window, columns=('ID', 'Nom', 'Prenom', 'Email'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nom', text='Nom')
        self.tree.heading('Prenom', text='Prenom')
        self.tree.heading('Email', text='Email')

        for client in clients:
            self.tree.insert('', tk.END, values=client)

        self.tree.pack(pady=10)

if __name__ == '__main__':
    root = tk.Tk()
    app = BankerApp(root)
    root.mainloop()
