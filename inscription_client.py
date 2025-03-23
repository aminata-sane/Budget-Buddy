import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import add_client, get_clients
import re
import hashlib
import sqlite3

# Utilisez un chemin absolu pour la base de données
db_path = os.path.join(os.path.dirname(__file__), 'clients.db')
# Create the clients table if it doesn't exist
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS clients (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nom TEXT NOT NULL,
    Prenom TEXT NOT NULL,
    Email TEXT NOT NULL,
    Mot_de_passe TEXT NOT NULL
);
''')
conn.commit()
conn.close()

class RegistrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inscription des Clients")

        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self.root, text="Formulaire d'inscription Client")
        self.label.pack(pady=10)

        self.nom_label = ttk.Label(self.root, text="Nom:")
        self.nom_label.pack(pady=5)
        self.nom_entry = ttk.Entry(self.root)
        self.nom_entry.pack(pady=5)

        self.prenom_label = ttk.Label(self.root, text="Prenom:")  # Utilisez "Prenom" au lieu de "Prénom"
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

        self.add_button = ttk.Button(self.root, text="Ajouter", command=self.add_client)
        self.add_button.pack(pady=10)

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
        prenom = self.prenom_entry.get()  # Utilisez "prenom" au lieu de "prénom"
        email = self.email_entry.get()
        mot_de_passe = self.mot_de_passe_entry.get()

        valid, message = self.validate_password(mot_de_passe)
        if not valid:
            messagebox.showwarning("Erreur", message)
            return

        hashed_password = self.hash_password(mot_de_passe)

        if nom and prenom and email and mot_de_passe:
            try:
                add_client(nom, prenom, email, hashed_password)
                messagebox.showinfo("Succès", "Client ajouté avec succès!")
                self.root.destroy()  # Fermer la fenêtre après l'ajout du client
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
    app = RegistrationApp(root)
    root.mainloop()