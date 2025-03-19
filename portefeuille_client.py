import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import add_client, get_clients
import re
import hashlib

class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des Clients")

        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self.root, text="Ajouter un nouveau client")
        self.label.pack(pady=10)

        self.nom_label = ttk.Label(self.root, text="Nom:")
        self.nom_label.pack(pady=5)
        self.nom_entry = ttk.Entry(self.root)
        self.nom_entry.pack(pady=5)

        self.prénom_label = ttk.Label(self.root, text="Prenom:")
        self.prénom_label.pack(pady=5)
        self.prénom_entry = ttk.Entry(self.root)
        self.prénom_entry.pack(pady=5)

        self.email_label = ttk.Label(self.root, text="Email:")
        self.email_label.pack(pady=5)
        self.email_entry = ttk.Entry(self.root)
        self.email_entry.pack(pady=5)

        self.mot_de_passe_label = ttk.Label(self.root, text="Mot de passe:")
        self.mot_de_passe_label.pack(pady=5)
        self.mot_de_passe_entry = ttk.Entry(self.root, show="*")
        self.mot_de_passe_entry.pack(pady=5)

        self.add_button = ttk.Button(self.root, text="Ajouter", command=self.add_client)
        self.add_button.pack(pady=10)

        self.view_button = ttk.Button(self.root, text="Voir les clients", command=self.view_clients)
        self.view_button.pack(pady=10)

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

    def add_client(self):
        nom = self.nom_entry.get()
        prénom = self.prénom_entry.get()
        email = self.email_entry.get()
        mot_de_passe = self.mot_de_passe_entry.get()

        valid, message = self.validate_password(mot_de_passe)
        if not valid:
            messagebox.showwarning("Erreur", message)
            return

        hashed_password = self.hash_password(mot_de_passe)

        if nom and prénom and email and mot_de_passe:
            try:
                add_client(nom, prénom, email, hashed_password)
                messagebox.showinfo("Succès", "Client ajouté avec succès!")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'ajout du client : {e}")
        else:
            messagebox.showwarning("Erreur", "Tous les champs sont obligatoires!")

    def view_clients(self):
        clients = get_clients()
        print(f"Clients: {clients}")  # Ajoutez ce message de débogage pour vérifier les clients récupérés
        self.clients_window = tk.Toplevel(self.root)
        self.clients_window.title("Liste des clients")

        self.tree = ttk.Treeview(self.clients_window, columns=('ID', 'Nom', 'Prenom', 'Email'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nom', text='Nom')
        self.tree.heading('Prenom', text='Prenom')
        self.tree.heading('Email', text='Email')

        for client in clients:
            print(f"Ajout du client: {client}")  # Ajoutez ce message de débogage pour vérifier chaque client ajouté
            self.tree.insert('', tk.END, values=client)

        self.tree.pack(pady=10)

if __name__ == '__main__':
    root = tk.Tk()
    app = ClientApp(root)
    root.mainloop()
