import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageDraw
import os
import hashlib
from database import create_table 
from database import verify_client, add_banker, add_client, get_clients_of_banker # Importer les fonctions nécessaires
from compte_client import ClientAccountApp  # Importer la classe ClientAccountApp
from portefeuille_client import PortefeuilleClientApp  # Importer la classe PortefeuilleClientApp
import sqlite3

class BankingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Banking System")

        create_table()
        
        # The size of ecran
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        self.root.geometry(f"{screen_width}x{screen_height}")
        
        # Set gradient background
        self.bg_image = self.create_gradient_image(screen_width, screen_height, "#757D86", "#FB84AE")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        
        # Show gradient background
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Add logo and label
        self.logo_image = self.load_image("images/logo.png", (80, 80))
        if self.logo_image:
            self.logo_label = tk.Label(self.root, image=self.logo_image, bg="#FB84AE")
            self.logo_label.place(x=20, y=20) 
        
        title_label = tk.Label(self.root, text="Optimize Your Finances like your code", font=("Arial", 24, "bold"), fg="white", bg="#5E5E5E", padx=20, pady=10)
        title_label.place(relx=0.5, y=20, anchor="n")
        
        # Main frame
        self.frame = tk.Frame(self.root, bg="#917d8f") 
        self.frame.place(relx=0.5, rely=0.5, anchor="center", width=screen_width * 0.9, height=screen_height * 0.6)
        
        self.load_images()
        self.show_home()

    def create_gradient_image(self, width, height, color1, color2):

# Two colors gradient
        gradient = Image.new("RGB", (width, height), color1)
        draw = ImageDraw.Draw(gradient) 
        
        for i in range(height):
            ratio = i / height
            r = int((1 - ratio) * int(color1[1:3], 16) + ratio * int(color2[1:3], 16))
            g = int((1 - ratio) * int(color1[3:5], 16) + ratio * int(color2[3:5], 16))
            b = int((1 - ratio) * int(color1[5:7], 16) + ratio * int(color2[5:7], 16))
            draw.line([(0, i), (width, i)], fill=(r, g, b))
        
        return gradient
    
    def load_images(self):
        self.client_photo = self.load_image("images/client.png", (400, 500)) 
        self.banker_photo = self.load_image("images/bank.png", (400, 500))    
        self.inscription_photo = self.load_image("images/registration.png", (80, 80))
        self.connexion_photo = self.load_image("images/login.png", (80, 80))

    def load_image(self, image_path, size):
        if os.path.exists(image_path):
            img = Image.open(image_path).resize(size)
            return ImageTk.PhotoImage(img)
        else:
            print(f"Image not found: {image_path}")
            return None
    
    def clear_frame(self):
    #    Clean frame
        for widget in self.frame.winfo_children():
            widget.destroy()
    
    def show_home(self):
        self.clear_frame()

        # Left side - client
        client_image_label = tk.Label(self.frame, image=self.client_photo, bg="#FB84AE")
        client_image_label.place(relx=0.25, rely=0.3, anchor="center") 
        
        # Right side - banker
        banker_image_label = tk.Label(self.frame, image=self.banker_photo, bg="#FB84AE")
        banker_image_label.place(relx=0.75, rely=0.3, anchor="center")  
        
        #  Button for client
        client_button = tk.Button(self.frame, text="Customer", font=("Arial", 18, "bold"), bg="#5E5E5E", fg="white", borderwidth=0, command=self.show_client_login)
        client_button.place(relx=0.25, rely=0.9, anchor="center")  
        
        # Button for banker
        banker_button = tk.Button(self.frame, text="Banker", font=("Arial", 18, "bold"), bg="#5E5E5E", fg="white", borderwidth=0, command=self.show_banker_page)
        banker_button.place(relx=0.75, rely=0.9, anchor="center")  
    
    def show_client_login(self):
        self.clear_frame()
        tk.Label(self.frame, text="Client Login Page", font=("Arial", 14), bg="white", fg="black").pack(pady=20)
        
        inscription_button = tk.Button(self.frame, image=self.inscription_photo, command=self.show_inscription_client, bg="white", bd=0)
        inscription_button.pack(side=tk.LEFT, padx=20, pady=10)
        tk.Label(self.frame, text="Inscription", font=("Arial", 12), bg="white", fg="black").pack(side=tk.LEFT, padx=20)

        connexion_button = tk.Button(self.frame, image=self.connexion_photo, command=self.show_connexion_client, bg="white", bd=0)
        connexion_button.pack(side=tk.RIGHT, padx=20, pady=10)
        tk.Label(self.frame, text="Connexion", font=("Arial", 12), bg="white", fg="black").pack(side=tk.RIGHT, padx=20)

        tk.Button(self.frame, text="Back to Home", command=self.show_home, bg="white", fg="black", bd=0).pack(pady=10)
    
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
        add_banker(name, surname, email, hashed_password)
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
            self.clear_frame()
            PortefeuilleClientApp(self.frame, banker[0], back_callback=self.show_home)
        else:
            messagebox.showerror("Error", "Incorrect email or password.")
    
    def show_clients_list(self, ID_banker):
        self.clear_frame()
        
        tk.Label(self.frame, text="Customer list", font=("Arial", 14), bg="white", fg="black").pack(pady=10)
        
        clients = get_clients_of_banker(ID_banker)
        
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
    

    def show_inscription_client(self):
        self.clear_frame()
        tk.Label(self.frame, text="Formulaire d'inscription Client", font=("Arial", 14), bg="white", fg="black").pack(pady=20)
        
        tk.Label(self.frame, text="Nom:", font=("Arial", 12), bg="white", fg="black").pack(pady=5)
        self.nom_entry = tk.Entry(self.frame)
        self.nom_entry.pack(pady=5)
        
        tk.Label(self.frame, text="Prénom:", font=("Arial", 12), bg="white", fg="black").pack(pady=5)
        self.prenom_entry = tk.Entry(self.frame)
        self.prenom_entry.pack(pady=5)
        
        tk.Label(self.frame, text="Email:", font=("Arial", 12), bg="white", fg="black").pack(pady=5)
        self.email_entry = tk.Entry(self.frame)
        self.email_entry.pack(pady=5)
        
        tk.Label(self.frame, text="Mot de passe:", font=("Arial", 12), bg="white", fg="black").pack(pady=5)
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.pack(pady=5)
        
        tk.Button(self.frame, text="S'inscrire", command=self.register_client, bg="white", fg="black", bd=0).pack(pady=10)
        tk.Button(self.frame, text="Back", command=self.show_client_login, bg="white", fg="black", bd=0).pack(pady=10)
    
    def register_client(self):
        nom = self.nom_entry.get()
        prenom = self.prenom_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        if not (nom and prenom and email and password):
            messagebox.showwarning("Error", "Fill in all fields!")
            return
        
        hashed_password = self.hash_password(password)
        add_client(nom, prenom, email, hashed_password)
        messagebox.showinfo("Success", "Registration successful!")
        self.show_client_login()

    def show_connexion_client(self):
        self.clear_frame()
        tk.Label(self.frame, text="Formulaire de Connexion Client", font=("Arial", 14), bg="white", fg="black").pack(pady=20)
        
        tk.Label(self.frame, text="Email:", font=("Arial", 12), bg="white", fg="black").pack(pady=5)
        self.email_entry = tk.Entry(self.frame)
        self.email_entry.pack(pady=5)
        
        tk.Label(self.frame, text="Mot de passe:", font=("Arial", 12), bg="white", fg="black").pack(pady=5)
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.pack(pady=5)
        
        tk.Button(self.frame, text="Se connecter", command=self.login_client, bg="white", fg="black", bd=0).pack(pady=10)
        tk.Button(self.frame, text="Back", command=self.show_client_login, bg="white", fg="black", bd=0).pack(pady=10)
    
    def login_client(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        client_id = verify_client(email, password)
        if client_id:
            self.clear_frame()
            ClientAccountApp(self.frame, client_id, back_callback=self.show_home)
        else:
            messagebox.showerror("Erreur de connexion", "Email ou mot de passe incorrect")

if __name__ == '__main__':
    root = tk.Tk()
    app = BankingApp(root)
    root.mainloop()