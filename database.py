import os
import sqlite3

#Utilisez un chemein absolu pour la base de données
db_path = os.path.join(os.path.dirname(__file__), 'clients.db')

def create_connection():
    connection = sqlite3.connect('budget_buddy.db')
    return connection

def create_table():
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            date TEXT NOT NULL,
            retrait REAL,
            dépot REAL,
            transfert REAL,
            montant REAL NOT NULL,
            description TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            ID_client INTEGER PRIMARY KEY,
            Nom TEXT NOT NULL,
            Prenom TEXT NOT NULL,
            Email TEXT NOT NULL UNIQUE,
            Mot_de_passe TEXT NOT NULL
        )
    ''')
    
    connection.commit()
    connection.close()

def add_client(nom, prenom, email, mot_de_passe):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO clients (Nom, Prenom, Email, Mot_de_passe)
        VALUES (?, ?, ?, ?)
    ''', (nom, prenom, email, mot_de_passe))
    conn.commit()
    conn.close()

def get_clients():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT ID, Nom, Prenom, Email FROM clients')
    clients = cursor.fetchall()
    conn.close()
    return clients

if __name__ == '__main__':
    create_table()


