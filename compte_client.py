import tkinter as tk
from tkinter import ttk
import sqlite3

class ClientAccountApp:
    def __init__(self, parent, client_id, back_callback):
        self.parent = parent
        self.client_id = client_id
        self.back_callback = back_callback
        self.create_widgets()
        self.load_balance()
        self.load_transactions()
    
    def create_widgets(self):
        self.balance_label = tk.Label(self.parent, text="Balance: $0.00", font=("Arial", 16))
        self.balance_label.pack(pady=10)
        
        self.transactions_frame = tk.Frame(self.parent)
        self.transactions_frame.pack(pady=20)
        
        self.create_transaction_button("Deposit", "deposit")
        self.create_transaction_button("Withdrawal", "withdrawal")
        self.create_transaction_button("Transfer", "transfer")
        
        # Ajouter un bouton "Back" pour revenir à la page d'accueil
        back_button = ttk.Button(self.parent, text="Back", command=self.back_callback)
        back_button.pack(pady=10)
    
    def create_transaction_button(self, text, transaction_type):
        button = tk.Button(self.transactions_frame, text=text, command=lambda: self.toggle_transaction_menu(transaction_type))
        button.pack(side=tk.LEFT, padx=10)
        
        menu_frame = tk.Frame(self.transactions_frame)
        menu_frame.pack(side=tk.LEFT, padx=10)
        menu_frame.pack_forget()
        
        setattr(self, f"{transaction_type}_menu_frame", menu_frame)
    
    def toggle_transaction_menu(self, transaction_type):
        menu_frame = getattr(self, f"{transaction_type}_menu_frame")
        if menu_frame.winfo_ismapped():
            menu_frame.pack_forget()
        else:
            self.load_transaction_details(transaction_type)
            menu_frame.pack(side=tk.LEFT, padx=10)
    
    def load_balance(self):
        connection = sqlite3.connect('budget_buddy.db')
        cursor = connection.cursor()
        cursor.execute('SELECT SUM(montant) FROM transactions WHERE client_id = ?', (self.client_id,))
        balance = cursor.fetchone()[0]
        connection.close()
        
        if balance is None:
            balance = 0.00
        
        self.balance_label.config(text=f"Balance: ${balance:.2f}")
    
    def load_transactions(self):
        connection = sqlite3.connect('budget_buddy.db')
        cursor = connection.cursor()
        cursor.execute('SELECT type, date, reference, description, montant FROM transactions WHERE client_id = ?', (self.client_id,))
        transactions = cursor.fetchall()
        connection.close()
        
        self.transactions = {
            "deposit": [],
            "withdrawal": [],
            "transfer": []
        }
        
        for transaction in transactions:
            self.transactions[transaction[0]].append(transaction)
    
    def load_transaction_details(self, transaction_type):
        menu_frame = getattr(self, f"{transaction_type}_menu_frame")
        for widget in menu_frame.winfo_children():
            widget.destroy()
        
        for transaction in self.transactions[transaction_type]:
            date, reference, description, montant = transaction[1], transaction[2], transaction[3], transaction[4]
            tk.Label(menu_frame, text=f"Date: {date}").pack()
            tk.Label(menu_frame, text=f"Reference: {reference}").pack()
            tk.Label(menu_frame, text=f"Description: {description}").pack()
            tk.Label(menu_frame, text=f"Montant: ${montant:.2f}").pack()
            tk.Label(menu_frame, text="").pack()  # Empty line for spacing

if __name__ == '__main__':
    root = tk.Tk()
    app = ClientAccountApp(root, client_id=1, back_callback=root.destroy)  # Remplacez par l'ID du client réel
    root.mainloop()