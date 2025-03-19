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
            depot REAL,
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
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            ID_account INTEGER PRIMARY KEY,
            ID_client INTEGER,
            account_type TEXT NOT NULL,
            balance REAL NOT NULL,
            FOREIGN KEY (ID_client) REFERENCES clients (ID_client)
        )
    ''')
    
    connection.commit()
    connection.close()

def add_client(nom, prenom, email, mot_de_passe):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute('''
            INSERT INTO clients (Nom, Prenom, Email, Mot_de_passe)
            VALUES (?, ?, ?, ?)
        ''', (nom, prenom, email, mot_de_passe))
        connection.commit()
    except Exception as e:
        print(f"Erreur lors de l'ajout du client : {e}")
        raise
    finally:
        connection.close()

def get_clients():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM clients')
    clients = cursor.fetchall()
    print(f"Clients récupérés: {clients}")  # Ajoutez ce message de débogage pour vérifier les clients récupérés
    connection.close()
    return clients

if __name__ == '__main__':
    create_table()




