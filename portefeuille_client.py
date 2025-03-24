import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from inscription_client import RegistrationApp  
from database import add_client, get_clients
import re
import hashlib
from compte_client import ClientAccountApp  

class PortefeuilleClientApp:
    def __init__(self, parent, banker_id, back_callback):
        self.parent = parent
        self.banker_id = banker_id
        self.back_callback = back_callback
        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self.parent, text="Customer management")
        self.label.pack(pady=10)

        self.add_button = ttk.Button(self.parent, text="Add a customer", command=self.open_registration_form)
        self.add_button.pack(pady=10)

        self.view_button = ttk.Button(self.parent, text="Open customers list", command=self.view_clients)
        self.view_button.pack(pady=10)

        # Add button back
        self.back_button = ttk.Button(self.parent, text="Back", command=self.back_callback)
        self.back_button.pack(pady=10)

    def open_registration_form(self):
        registration_window = tk.Toplevel(self.parent)
        RegistrationApp(registration_window)
        
        # Add button back
        back_button = ttk.Button(registration_window, text="Back", command=registration_window.destroy)
        back_button.pack(pady=10)

    def view_clients(self):
        clients = get_clients()
        self.clients_window = tk.Toplevel(self.parent)
        self.clients_window.title("Customers list")

        self.tree = ttk.Treeview(self.clients_window, columns=('ID', 'Name', 'Surname', 'Email'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Surname', text='Surname')
        self.tree.heading('Email', text='Email')

        for client in clients:
            self.tree.insert('', tk.END, values=client)

        self.tree.pack(pady=10)
        
        #Add button back
        back_button = ttk.Button(self.clients_window, text="Back", command=self.clients_window.destroy)
        back_button.pack(pady=10)

        # Opent customers page
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
    app = PortefeuilleClientApp(root, banker_id=1, back_callback=root.destroy) 
    root.mainloop()
