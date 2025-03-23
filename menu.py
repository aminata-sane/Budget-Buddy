import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import hashlib
from database import verify_client, add_banker, authenticate_banker, get_clients_of_banker  # Importer les fonctions nécessaires
from compte_client import ClientAccountApp  # Importer la classe ClientAccountApp
from portefeuille_client import PortefeuilleClientApp  # Importer la classe PortefeuilleClientApp

class BankingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Banking System")
        
        # Get screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Set window size to screen size
        self.root.geometry(f"{screen_width}x{screen_height}")
        
        # Set background color
        self.root.configure(bg="white")
        
        # Add logo and slogan
        logo_label = tk.Label(self.root, text="Bank Logo", font=("Arial", 24), bg="white", fg="black")
        logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        slogan_label = tk.Label(self.root, text="Your Friendly Bank !", font=("Arial", 16), bg="white", fg="black")
        slogan_label.grid(row=0, column=1, padx=10, pady=5, sticky="n")
        
        self.frame = tk.Frame(self.root, bg="white")
        self.frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        
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
        
        banker = authenticate_banker(email, password)
        
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
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

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