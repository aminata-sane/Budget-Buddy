import sqlite3

def create_connection():
    connection = sqlite3.connect('budget_buddy.db')
    return connection

def create_table():
    connection = create_connection()
    cursor = connection.cursor()

    # table banker
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS banker (
            ID_banker INTEGER PRIMARY KEY AUTOINCREMENT,
            Nom TEXT NOT NULL,
            Prenom TEXT NOT NULL,
            Email TEXT NOT NULL UNIQUE,
            Mot_de_passe TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            retrait REAL,
            dépot REAL,
            transfert REAL,
            montant REAL NOT NULL,
            description TEXT,
            ID_client INTEGER,
            FOREIGN KEY (ID_client) REFERENCES clients(ID_client)
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

        # table of banker_clients connection
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS banker_clients (
            ID_banker INTEGER,
            ID_client INTEGER,
            PRIMARY KEY (ID_banker, ID_client),
            FOREIGN KEY (ID_banker) REFERENCES banker(ID_banker),
            FOREIGN KEY (ID_client) REFERENCES clients(ID_client)
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

def add_banker(nom, prenom, email, mot_de_passe):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO banker (Nom, Prénom, Email, Mot_de_passe)
        VALUES (?, ?, ?, ?, ?)
    ''', (nom, prenom, email, mot_de_passe))
    connection.commit()
    connection.close()


# Connection beetwen banker and client
def assign_client_to_banker(ID_banker, ID_client):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO banker_clients (ID_banker, ID_client)
        VALUES (?, ?)
    ''', (ID_banker, ID_client))
    connection.commit()
    connection.close()

# Get all clients of a banker
def get_clients_of_banker(ID_banker):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('''
        SELECT clients.ID_client, clients.Nom, clients.Prenom, clients.Email
        FROM clients
        JOIN banker_clients ON clients.ID_client = banker_clients.ID_client
        WHERE banker_clients.ID_banker = ?
    ''', (ID_banker,))
    clients = cursor.fetchall()
    connection.close()
    return clients

# Banker authentication
def authenticate_banker(email, mot_de_passe):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('''
        SELECT ID_banker FROM banker WHERE Email = ? AND Mot_de_passe = ?
    ''', (email, mot_de_passe))
    banker = cursor.fetchone()
    connection.close()
    # Return the ID of the banker if found
    return banker  

if __name__ == '__main__':
    create_table()


