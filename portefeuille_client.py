import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from inscription_client import RegistrationApp  # Importer le formulaire d'inscription
from database import add_client, get_clients
import re
import hashlib
from compte_client import ClientAccountApp  # Importer la classe ClientAccountApp

class PortefeuilleClientApp:
    def __init__(self, parent, banker_id, back_callback):
        self.parent = parent
        self.banker_id = banker_id
        self.back_callback = back_callback
        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self.parent, text="Gestion des Clients")
        self.label.pack(pady=10)

        self.add_button = ttk.Button(self.parent, text="Ajouter un client", command=self.open_registration_form)
        self.add_button.pack(pady=10)

        self.view_button = ttk.Button(self.parent, text="Voir les clients", command=self.view_clients)
        self.view_button.pack(pady=10)

        # Ajouter un bouton "Back" pour revenir à la page d'accueil
        self.back_button = ttk.Button(self.parent, text="Back", command=self.back_callback)
        self.back_button.pack(pady=10)

    def open_registration_form(self):
        registration_window = tk.Toplevel(self.parent)
        RegistrationApp(registration_window)
        
        # Ajouter un bouton "Back" pour fermer la fenêtre d'inscription
        back_button = ttk.Button(registration_window, text="Back", command=registration_window.destroy)
        back_button.pack(pady=10)

    def view_clients(self):
        clients = get_clients()
        self.clients_window = tk.Toplevel(self.parent)
        self.clients_window.title("Liste des clients")

        self.tree = ttk.Treeview(self.clients_window, columns=('ID', 'Nom', 'Prenom', 'Email'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nom', text='Nom')
        self.tree.heading('Prenom', text='Prenom')
        self.tree.heading('Email', text='Email')

        for client in clients:
            self.tree.insert('', tk.END, values=client)

        self.tree.pack(pady=10)
        
        # Ajouter un bouton "Back" pour fermer la fenêtre de la liste des clients
        back_button = ttk.Button(self.clients_window, text="Back", command=self.clients_window.destroy)
        back_button.pack(pady=10)

        # Ajouter un événement de clic pour ouvrir le compte client
        self.tree.bind("<Double-1>", self.on_client_click)

    def on_client_click(self, event):
        selected_item = self.tree.selection()[0]
        client_id = self.tree.item(selected_item)['values'][0]
        self.clients_window.destroy()
        self.clear_frame()
        ClientAccountApp(self.parent, client_id, back_callback=self.back_callback)

    def clear_frame(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = PortefeuilleClientApp(root, banker_id=1, back_callback=root.destroy)  # Remplacez par l'ID du banquier réel
    root.mainloop()
