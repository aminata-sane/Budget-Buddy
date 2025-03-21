import os
import sqlite3

# Utilisez un chemin absolu pour la base de données
db_path = os.path.join(os.path.dirname(__file__), 'clients.db')

def create_connection():
    connection = sqlite3.connect(db_path)
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
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Nom TEXT NOT NULL,
            Prenom TEXT NOT NULL,
            Email TEXT NOT NULL UNIQUE,
            Mot_de_passe TEXT NOT NULL
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
    cursor.execute('SELECT ID, Nom, Prenom, Email FROM clients')
    clients = cursor.fetchall()
    conn.close()
    return clients

def verify_client(email, mot_de_passe):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM clients WHERE Email = ? AND Mot_de_passe = ?
    ''', (email, mot_de_passe))
    client = cursor.fetchone()
    conn.close()
    return client is not None

if __name__ == '__main__':
    create_table()


