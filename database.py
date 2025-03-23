import os
import sqlite3

# Utilisez un chemin absolu pour la base de données
db_path = os.path.join(os.path.dirname(__file__), 'budget_buddy.db')

def create_connection():
    connection = sqlite3.connect(db_path)
    return connection

def create_table():
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Nom TEXT NOT NULL,
            Prenom TEXT NOT NULL,
            Email TEXT NOT NULL UNIQUE,
            Mot_de_passe TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            type TEXT NOT NULL,
            date TEXT NOT NULL,
            reference TEXT NOT NULL,
            description TEXT,
            montant REAL NOT NULL,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
    ''')
    
    connection.commit()
    connection.close()

def add_client(nom, prenom, email, mot_de_passe):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO clients (Nom, Prenom, Email, Mot_de_passe)
        VALUES (?, ?, ?, ?)
    ''', (nom, prenom, email, mot_de_passe))
    conn.commit()
    conn.close()

def get_clients():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, Nom, Prenom, Email FROM clients')
    clients = cursor.fetchall()
    conn.close()
    return clients

def add_transaction(client_id, transaction_type, date, reference, description, montant):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO transactions (client_id, type, date, reference, description, montant)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (client_id, transaction_type, date, reference, description, montant))
    connection.commit()
    connection.close()

def get_transactions():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions')
    transactions = cursor.fetchall()
    conn.close()
    return transactions

def get_client_balance(client_id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT SUM(montant) FROM transactions WHERE client_id = ?', (client_id,))
    balance = cursor.fetchone()[0]
    connection.close()
    
    if balance is None:
        balance = 0.00
    
    return balance

def verify_client(email, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, Mot_de_passe FROM clients WHERE Email = ?', (email,))
    client = cursor.fetchone()
    conn.close()
    
    if client and client[1] == password:
        return client[0]  # Return client ID if password matches
    return None

if __name__ == '__main__':
    create_table()
    
    # Ajouter des clients
    add_client('John', 'Doe', 'john.doe@example.com', 'password123')
    add_client('Jane', 'Smith', 'jane.smith@example.com', 'password456')
    
    # Ajouter des transactions
    add_transaction(1, 'deposit', '2025-03-21', 'REF123', 'Initial deposit', 1000.00)
    add_transaction(1, 'withdrawal', '2025-03-22', 'REF124', 'ATM withdrawal', -200.00)
    add_transaction(1, 'transfer', '2025-03-23', 'REF125', 'Transfer to savings', -300.00)
    add_transaction(2, 'deposit', '2025-03-21', 'REF126', 'Initial deposit', 1500.00)
    add_transaction(2, 'withdrawal', '2025-03-22', 'REF127', 'ATM withdrawal', -500.00)
    
    # Vérifier les données
    clients = get_clients()
    for client in clients:
        print(client)
    
    transactions = get_transactions()
    for transaction in transactions:
        print(transaction)
    
    # Calculer le solde total des transactions pour le client avec l'ID 1
    balance = get_client_balance(1)
    print(f"Balance for client 1: ${balance:.2f}")


