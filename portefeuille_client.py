import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from inscription_client import RegistrationApp  # Importer le formulaire d'inscription
from database import add_client, get_clients, get_clients_of_banker
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
        tk.Label(self.parent, text="Customer list", font=("Arial", 14), bg="white", fg="black").pack(pady=10)
        
        clients = get_clients_of_banker(self.banker_id)
        
        self.tree = ttk.Treeview(self.parent, columns=('ID', 'Name', 'Surname', 'Email'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Surname', text='Surname')
        self.tree.heading('Email', text='Email')

        for client in clients:
            self.tree.insert('', tk.END, values=client)
        
        self.tree.pack(pady=10)
        self.tree.bind("<Double-1>", self.on_client_click)  # Ajouter un événement de double-clic

        tk.Button(self.parent, text="Back", command=self.back_callback, bg="white", fg="black").pack(pady=10)

    def on_client_click(self, event):
        selected_item = self.tree.selection()[0]
        client_id = self.tree.item(selected_item, 'values')[0]
        self.clear_frame()
        ClientAccountApp(self.parent, client_id, back_callback=self.back_callback)

    def clear_frame(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = PortefeuilleClientApp(root, banker_id=1, back_callback=root.destroy)  # Remplacez par l'ID du banquier réel
    root.mainloop()
