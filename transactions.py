from database import create_connection

def deposit(account_id, amount):
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, account_id))
    cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (?, 'deposit', ?)", (account_id, amount))
    
    conn.commit()
    conn.close()

def withdraw(account_id, amount):
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT balance FROM accounts WHERE id = ?", (account_id,))
    balance = cursor.fetchone()[0]
    
    if balance >= amount:
        cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, account_id))
        cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (?, 'withdraw', ?)", (account_id, -amount))
        conn.commit()
    else:
        print("Insufficient funds!")

    conn.close()

def transfer(sender_id, receiver_id, amount):
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT balance FROM accounts WHERE id = ?", (sender_id,))
    balance = cursor.fetchone()[0]
    
    if balance >= amount:
        cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, sender_id))
        cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, receiver_id))
        cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (?, 'transfer_out', ?)", (sender_id, -amount))
        cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (?, 'transfer_in', ?)", (receiver_id, amount))
        conn.commit()
    else:
        print("Insufficient funds for transfer!")

    conn.close()
