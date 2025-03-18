import sqlite3

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
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO clients (Nom, Prénom, Email, Mot_de_passe)
        VALUES (?, ?, ?, ?)
    ''', (nom, prenom, email, mot_de_passe))
    connection.commit()
    connection.close()

def get_clients():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM clients')
    clients = cursor.fetchall()
    connection.close()
    return clients

if __name__ == '__main__':
    create_table()


