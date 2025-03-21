

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import re
import hashlib

# Function to create a connection to the database
def create_connection():
    return sqlite3.connect('budget_buddy.db')

# Function to hash a password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to authenticate a banker
def authenticate_banker(email, mot_de_passe):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT ID_banker FROM banker WHERE Email = ? AND Mot_de_passe = ?', 
                   (email, hash_password(mot_de_passe)))
    banker = cursor.fetchone()
    connection.close()
    return banker  

# Function to get clients of banker
def get_clients_of_banker(ID_banker):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('''
        SELECT clients.ID_client, clients.Nom, clients.Prenom, clients.Email
        FROM clients
        JOIN banker_clients ON clients.ID_client = banker_clients.ID_client
        WHERE banker_clients.ID_banker = ?''', (ID_banker,))
    clients = cursor.fetchall()
    connection.close()
    return clients

# Function to add a banker
def add_banker(nom, prenom, email, mot_de_passe):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO banker (Nom, Prenom, Email, Mot_de_passe) VALUES (?, ?, ?, ?)', 
                   (nom, prenom, email, hash_password(mot_de_passe)))
    connection.commit()
    connection.close()

# --- Main window ---
root = tk.Tk()
root.title("Banking System")
root.geometry("600x400")

frame = tk.Frame(root)
frame.pack()

# --- Add images ---
client_img = Image.open("images/client.jpg").resize((150, 200))
client_photo = ImageTk.PhotoImage(client_img)

banker_img = Image.open("images/bank.png").resize((150, 200))
banker_photo = ImageTk.PhotoImage(banker_img)

# --- Function to switch the pages ---
def show_home():
    clear_frame()
    tk.Label(frame, text="Make your choise", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=20)
    # .pack(pady=20)
    
    client_button = tk.Button(frame, image=client_photo, command=show_client_login, borderwidth=0)
    client_button.grid(row=1, column=0, padx=20, pady=10)
    # client_button.pack(side="left", padx=20)
    # tk.Label(frame, text="Customer", font=("Arial", 12)).pack(side="left")
    client_label = tk.Label(frame, text="Customer", font=("Arial", 12), cursor="hand2")
    client_label.grid(row=2, column=0, pady=5)
    client_label.bind("<Button-1>", lambda event: show_client_login())

    banker_button = tk.Button(frame, image=banker_photo, command=show_banker_page, borderwidth=0)
    banker_button.grid(row=1, column=1, padx=20, pady=10)
    # banker_button.pack(side="right", padx=20)
    # tk.Label(frame, text="Banker", font=("Arial", 12)).pack(side="right")
    banker_label = tk.Label(frame, text="Banker", font=("Arial", 12), cursor="hand2")
    banker_label.grid(row=2, column=1, pady=5)
    banker_label.bind("<Button-1>", lambda event: show_banker_page())

def show_client_login():
    clear_frame()
    tk.Label(frame, text="Enter for customer", font=("Arial", 14)).pack(pady=20)
    tk.Button(frame, text="Back", command=show_home).pack(pady=10)

def show_banker_page():
    clear_frame()
    tk.Label(frame, text="Choose your action", font=("Arial", 14)).pack(pady=20)
    tk.Button(frame, text="Registration", command=show_banker_registration).pack(pady=10)
    tk.Button(frame, text="Login", command=show_banker_login).pack(pady=10)
    tk.Button(frame, text="Back", command=show_home).pack(pady=10)

def show_banker_registration():
    clear_frame()
    
    tk.Label(frame, text="Banker registration", font=("Arial", 14)).pack(pady=10)
    
    tk.Label(frame, text="Name:").pack()
    name_entry = tk.Entry(frame)
    name_entry.pack()
    
    tk.Label(frame, text="Surname:").pack()
    surname_entry = tk.Entry(frame)
    surname_entry.pack()
    
    tk.Label(frame, text="Email:").pack()
    email_entry = tk.Entry(frame)
    email_entry.pack()
    
    tk.Label(frame, text="Password:").pack()
    password_entry = tk.Entry(frame, show="*")
    password_entry.pack()
    
    def register_banker():
        name = name_entry.get()
        surname = surname_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        
        if not (name and surname and email and password):
            messagebox.showwarning("Error", "Fill in all fields!")
            return
        
        add_banker(name, surname, email, password)
        messagebox.showinfo("Success", "The registration is successful!")
        show_banker_page()
    
    tk.Button(frame, text="Registrated", command=register_banker).pack(pady=10)
    tk.Button(frame, text="Back", command=show_banker_page).pack(pady=10)

def show_banker_login():
    clear_frame()
    
    tk.Label(frame, text="Banker enter", font=("Arial", 14)).pack(pady=10)
    
    tk.Label(frame, text="Email:").pack()
    email_entry = tk.Entry(frame)
    email_entry.pack()
    
    tk.Label(frame, text="Password:").pack()
    password_entry = tk.Entry(frame, show="*")
    password_entry.pack()
    
    def login_banker():
        email = email_entry.get()
        password = password_entry.get()
        
        banker = authenticate_banker(email, password)
        
        if banker:
            messagebox.showinfo("Success", "Logged in!")
            show_clients_list(banker[0])
        else:
            messagebox.showerror("Error", "Incorrect email or password.")
    
    tk.Button(frame, text="Login", command=login_banker).pack(pady=10)
    tk.Button(frame, text="Back", command=show_banker_page).pack(pady=10)

def show_clients_list(ID_banker):
    clear_frame()
    
    tk.Label(frame, text="Customer list", font=("Arial", 14)).pack(pady=10)
    
    clients = get_clients_of_banker(ID_banker)
    
    tree = ttk.Treeview(frame, columns=('ID', 'Name', 'Surname', 'Email'), show='headings')
    tree.heading('ID', text='ID')
    tree.heading('Name', text='Name')
    tree.heading('Surname', text='Surname')
    tree.heading('Email', text='Email')

    for client in clients:
        tree.insert('', tk.END, values=client)
    
    tree.pack(pady=10)
    tk.Button(frame, text="Back", command=show_banker_page).pack(pady=10)

# Function to clear the frame
def clear_frame():
    for widget in frame.winfo_children():
        widget.destroy()

# Start the main page
show_home()

# Start the main loop
root.mainloop()
