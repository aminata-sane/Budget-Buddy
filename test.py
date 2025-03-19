import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import add_client, get_clients
from security import validate_password, hash_password


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

    def add_client(self):
        nom = self.nom_entry.get()
        prénom = self.prenom_entry.get()
        email = self.email_entry.get()
        mot_de_passe = self.mot_de_passe_entry.get()

        valid, message = validate_password(mot_de_passe)
        if not valid:
            messagebox.showwarning("Erreur", message)
            return

        hashed_password = hash_password(mot_de_passe)

        if nom and prénom and email and mot_de_passe:
            add_client(nom, prénom, email, hashed_password)
            messagebox.showinfo("Succès", "Client ajouté avec succès!")
        else:
            messagebox.showwarning("Erreur", "Tous les champs sont obligatoires!")

    def view_clients(self):
        clients = get_clients()
        self.clients_window = tk.Toplevel(self.root)
        self.clients_window.title("Liste des clients")

        self.tree = ttk.Treeview(self.clients_window, columns=('ID', 'Nom', 'Prénom', 'Email'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nom', text='Nom')
        self.tree.heading('Prénom', text='Prenom')
        self.tree.heading('Email', text='Email')

        for client in clients:
            self.tree.insert('', tk.END, values=client)

        self.tree.pack(pady=10)

if __name__ == '__main__':
    root = tk.Tk()
    app = ClientApp(root)
    root.mainloop()
