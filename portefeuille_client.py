import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from inscription_client import RegistrationApp  # Importer le formulaire d'inscription
from database import add_client, get_clients
import re
import hashlib

class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des Clients")

        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self.root, text="Gestion des Clients")
        self.label.pack(pady=10)

        self.add_button = ttk.Button(self.root, text="Ajouter un client", command=self.open_registration_form)
        self.add_button.pack(pady=10)

        self.view_button = ttk.Button(self.root, text="Voir les clients", command=self.view_clients)
        self.view_button.pack(pady=10)

    def open_registration_form(self):
        registration_window = tk.Toplevel(self.root)
        RegistrationApp(registration_window)

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
