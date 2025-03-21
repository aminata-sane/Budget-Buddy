import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import re
import hashlib

class BankingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Banking System")
        self.root.geometry("600x400")
        
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        
        self.load_images()
        self.show_home()
    
    def load_images(self):
        self.client_img = Image.open("images/client.jpg").resize((150, 200))
        self.client_photo = ImageTk.PhotoImage(self.client_img)
        
        self.banker_img = Image.open("images/bank.png").resize((150, 200))
        self.banker_photo = ImageTk.PhotoImage(self.banker_img)
    
    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
    
    def show_home(self):
        self.clear_frame()
        tk.Label(self.frame, text="Make your choice", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=20)
        
        client_button = tk.Button(self.frame, image=self.client_photo, command=self.show_client_login, borderwidth=0)
        client_button.grid(row=1, column=0, padx=20, pady=10)
        client_label = tk.Label(self.frame, text="Customer", font=("Arial", 12), cursor="hand2")
        client_label.grid(row=2, column=0, pady=5)
        client_label.bind("<Button-1>", lambda event: self.show_client_login())

        banker_button = tk.Button(self.frame, image=self.banker_photo, command=self.show_banker_page, borderwidth=0)
        banker_button.grid(row=1, column=1, padx=20, pady=10)
        banker_label = tk.Label(self.frame, text="Banker", font=("Arial", 12), cursor="hand2")
        banker_label.grid(row=2, column=1, pady=5)
        banker_label.bind("<Button-1>", lambda event: self.show_banker_page())
    
    def show_client_login(self):
        self.clear_frame()
        tk.Label(self.frame, text="Enter for customer", font=("Arial", 14)).pack(pady=20)
        tk.Button(self.frame, text="Back", command=self.show_home).pack(pady=10)
    
    def show_banker_page(self):
        self.clear_frame()
        tk.Label(self.frame, text="Choose your action", font=("Arial", 14)).pack(pady=20)
        tk.Button(self.frame, text="Registration", command=self.show_banker_registration).pack(pady=10)
        tk.Button(self.frame, text="Login", command=self.show_banker_login).pack(pady=10)
        tk.Button(self.frame, text="Back", command=self.show_home).pack(pady=10)
    
    def show_banker_registration(self):
        self.clear_frame()
        
        tk.Label(self.frame, text="Banker registration", font=("Arial", 14)).pack(pady=10)
        
        tk.Label(self.frame, text="Name:").pack()
        self.name_entry = tk.Entry(self.frame)
        self.name_entry.pack()
        
        tk.Label(self.frame, text="Surname:").pack()
        self.surname_entry = tk.Entry(self.frame)
        self.surname_entry.pack()
        
        tk.Label(self.frame, text="Email:").pack()
        self.email_entry = tk.Entry(self.frame)
        self.email_entry.pack()
        
        tk.Label(self.frame, text="Password:").pack()
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.pack()
        
        tk.Button(self.frame, text="Register", command=self.register_banker).pack(pady=10)
        tk.Button(self.frame, text="Back", command=self.show_banker_page).pack(pady=10)
    
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
        
        tk.Label(self.frame, text="Banker login", font=("Arial", 14)).pack(pady=10)
        
        tk.Label(self.frame, text="Email:").pack()
        self.login_email_entry = tk.Entry(self.frame)
        self.login_email_entry.pack()
        
        tk.Label(self.frame, text="Password:").pack()
        self.login_password_entry = tk.Entry(self.frame, show="*")
        self.login_password_entry.pack()
        
        tk.Button(self.frame, text="Login", command=self.login_banker).pack(pady=10)
        tk.Button(self.frame, text="Back", command=self.show_banker_page).pack(pady=10)
    
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
        
        tk.Label(self.frame, text="Customer list", font=("Arial", 14)).pack(pady=10)
        
        clients = self.get_clients_of_banker(ID_banker)
        
        tree = ttk.Treeview(self.frame, columns=('ID', 'Name', 'Surname', 'Email'), show='headings')
        tree.heading('ID', text='ID')
        tree.heading('Name', text='Name')
        tree.heading('Surname', text='Surname')
        tree.heading('Email', text='Email')
    
        for client in clients:
            tree.insert('', tk.END, values=client)
        
        tree.pack(pady=10)
        tk.Button(self.frame, text="Back", command=self.show_banker_page).pack(pady=10)
    
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

if __name__ == '__main__':
    root = tk.Tk()
    app = BankingApp(root)
    root.mainloop()
