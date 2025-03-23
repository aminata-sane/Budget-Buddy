import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import hashlib
import os

class BankingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Banking System")
        self.root.geometry("600x400")
        
        self.frame = tk.Frame(self.root, bg="white")
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self.load_images()
        self.show_home()
    
    def load_images(self):
        self.client_photo = self.load_image("images/client.png", (150, 200))
        self.banker_photo = self.load_image("images/bank.png", (150, 200))
        self.inscription_photo = self.load_image("images/registration.png", (100, 100))
        self.connexion_photo = self.load_image("images/login.png", (100, 100))
    
    def load_image(self, image_path, size):
        if os.path.exists(image_path):
            img = Image.open(image_path).resize(size)
            return ImageTk.PhotoImage(img)
        else:
            print(f"Image not found: {image_path}")
            return None
    
    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
    
    def show_home(self):
        self.clear_frame()
        tk.Label(self.frame, text="Make your choice", font=("Arial", 14), bg="white", fg="black").grid(row=0, column=0, columnspan=2, pady=20)
        
        client_button = tk.Button(self.frame, image=self.client_photo, command=self.show_client_login, borderwidth=0, bg="white")
        client_button.grid(row=1, column=0, padx=20, pady=10)
        client_label = tk.Label(self.frame, text="Customer", font=("Arial", 12), cursor="hand2", bg="white", fg="black")
        client_label.grid(row=2, column=0, pady=5)
        client_label.bind("<Button-1>", lambda event: self.show_client_login())

        banker_button = tk.Button(self.frame, image=self.banker_photo, command=self.show_banker_page, borderwidth=0, bg="white")
        banker_button.grid(row=1, column=1, padx=20, pady=10)
        banker_label = tk.Label(self.frame, text="Banker", font=("Arial", 12), cursor="hand2", bg="white", fg="black")
        banker_label.grid(row=2, column=1, pady=5)
        banker_label.bind("<Button-1>", lambda event: self.show_banker_page())
    
    def show_client_login(self):
        self.clear_frame()
        tk.Label(self.frame, text="Enter for customer", font=("Arial", 14), bg="white", fg="black").pack(pady=20)
        tk.Button(self.frame, text="Back", command=self.show_home, bg="white", fg="black").pack(pady=10)
    
    def show_banker_page(self):
        self.clear_frame()
        tk.Label(self.frame, text="Choose your action", font=("Arial", 14), bg="white", fg="black").pack(pady=20)
        tk.Button(self.frame, text="Registration", command=self.show_banker_registration, bg="white", fg="black").pack(pady=10)
        tk.Button(self.frame, text="Login", command=self.show_banker_login, bg="white", fg="black").pack(pady=10)
        tk.Button(self.frame, text="Back", command=self.show_home, bg="white", fg="black").pack(pady=10)
    
    def show_banker_registration(self):
        self.clear_frame()
        
        tk.Label(self.frame, text="Banker registration", font=("Arial", 14), bg="white", fg="black").pack(pady=10)
        
        tk.Label(self.frame, text="Name:", bg="white", fg="black").pack()
        self.name_entry = tk.Entry(self.frame)
        self.name_entry.pack()
        
        tk.Label(self.frame, text="Surname:", bg="white", fg="black").pack()
        self.surname_entry = tk.Entry(self.frame)
        self.surname_entry.pack()
        
        tk.Label(self.frame, text="Email:", bg="white", fg="black").pack()
        self.email_entry = tk.Entry(self.frame)
        self.email_entry.pack()
        
        tk.Label(self.frame, text="Password:", bg="white", fg="black").pack()
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.pack()
        
        tk.Button(self.frame, text="Register", command=self.register_banker, bg="white", fg="black").pack(pady=10)
        tk.Button(self.frame, text="Back", command=self.show_banker_page, bg="white", fg="black").pack(pady=10)
    
    def register_banker(self):
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        if not (name and surname and email and password):
            messagebox.showwarning("Error", "Fill in all fields!")
            return
        
        hashed_password = self.hash_password(password)
        self.add_banker(name, surname, email, hashed_password)
        messagebox.showinfo("Success", "Registration successful!")
        self.show_banker_page()
    
    def show_banker_login(self):
        self.clear_frame()
        
        tk.Label(self.frame, text="Banker login", font=("Arial", 14), bg="white", fg="black").pack(pady=10)
        
        tk.Label(self.frame, text="Email:", bg="white", fg="black").pack()
        self.login_email_entry = tk.Entry(self.frame)
        self.login_email_entry.pack()
        
        tk.Label(self.frame, text="Password:", bg="white", fg="black").pack()
        self.login_password_entry = tk.Entry(self.frame, show="*")
        self.login_password_entry.pack()
        
        tk.Button(self.frame, text="Login", command=self.login_banker, bg="white", fg="black").pack(pady=10)
        tk.Button(self.frame, text="Back", command=self.show_banker_page, bg="white", fg="black").pack(pady=10)
    
    def login_banker(self):
        email = self.login_email_entry.get()
        password = self.login_password_entry.get()
        
        banker = self.authenticate_banker(email, password)
        
        if banker:
            messagebox.showinfo("Success", "Logged in!")
            self.show_clients_list(banker[0])
        else:
            messagebox.showerror("Error", "Incorrect email or password.")
    
    def show_clients_list(self, ID_banker):
        self.clear_frame()
        
        tk.Label(self.frame, text="Customer list", font=("Arial", 14), bg="white", fg="black").pack(pady=10)
        
        clients = self.get_clients_of_banker(ID_banker)
        
        tree = ttk.Treeview(self.frame, columns=('ID', 'Name', 'Surname', 'Email'), show='headings')
        tree.heading('ID', text='ID')
        tree.heading('Name', text='Name')
        tree.heading('Surname', text='Surname')
        tree.heading('Email', text='Email')
    
        for client in clients:
            tree.insert('', tk.END, values=client)
        
        tree.pack(pady=10)
        tk.Button(self.frame, text="Back", command=self.show_banker_page, bg="white", fg="black").pack(pady=10)
    
    def create_connection(self):
        return sqlite3.connect('budget_buddy.db')
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate_banker(self, email, password):
        connection = self.create_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT ID_banker FROM banker WHERE Email = ? AND Mot_de_passe = ?', 
                       (email, self.hash_password(password)))
        banker = cursor.fetchone()
        connection.close()
        return banker  
    
    def add_banker(self, nom, prenom, email, mot_de_passe):
        connection = self.create_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO banker (Nom, Prenom, Email, Mot_de_passe) VALUES (?, ?, ?, ?)', 
                       (nom, prenom, email, mot_de_passe))
        connection.commit()
        connection.close()
    
    def get_clients_of_banker(self, ID_banker):
        connection = self.create_connection()
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

if __name__ == '__main__':
    root = tk.Tk()
    app = BankingApp(root)
    root.mainloop()