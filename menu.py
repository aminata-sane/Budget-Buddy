import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageDraw
import os
import hashlib
from database import verify_client, add_banker, authenticate_banker, get_clients_of_banker, add_client  # Importer les fonctions nécessaires
from compte_client import ClientAccountApp  # Importer la classe ClientAccountApp
from portefeuille_client import PortefeuilleClientApp  # Importer la classe PortefeuilleClientApp

class BankingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Banking System")
        
        # Set window size to large smartphone size (e.g., 414x896 pixels)
        self.root.geometry("414x896")
        
        # Set background color
        self.root.configure(bg="white")
        
        self.frame = tk.Frame(self.root, bg="white")
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self.load_images()
        self.show_home()
    
    def round_corners(self, image, radius):
        # Create a mask with rounded corners
        mask = Image.new("L", image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0) + image.size, radius, fill=255)
        image.putalpha(mask)
        return image
    
    def load_image(self, image_path, size, radius=20):
        if os.path.exists(image_path):
            img = Image.open(image_path).resize(size)
            img = self.round_corners(img, radius)
            print(f"Image loaded: {image_path}")  # Message de débogage
            return ImageTk.PhotoImage(img)
        else:
            print(f"Image not found: {image_path}")
            return None
    
    def load_images(self):
        self.logo_photo = self.load_image("images/logo.png", (100, 100), radius=20)  # Adjust image size and radius
        self.client_photo = self.load_image("images/client.png", (350, 450), radius=20)  # Adjust image size and radius
        self.banker_photo = self.load_image("images/bank.png", (350, 450), radius=20)  # Adjust image size and radius
        self.inscription_photo = self.load_image("images/registration.png", (75, 75), radius=20)  # Adjust image size and radius
        self.connexion_photo = self.load_image("images/login.png", (75, 75), radius=20)  # Adjust image size and radius
    
    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
    
    def show_home(self):
        self.clear_frame()
        
        logo_label = tk.Label(self.frame, image=self.logo_photo, bg="white")
        logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        
        tk.Label(self.frame, text="Welcome to Your Friendly Bank!", font=("Arial", 20, "bold"), bg="white", fg="black").grid(row=0, column=1, columnspan=2, pady=20)
        
        self.frame.columnconfigure(0, weight=1, minsize=100)
        self.frame.columnconfigure(1, weight=1, minsize=100)
        self.frame.rowconfigure(1, weight=1, minsize=150)
        
        client_button = tk.Button(self.frame, image=self.client_photo, command=self.show_client_login, borderwidth=0, bg="white")
        client_button.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        client_label = tk.Label(self.frame, text="✨Customer✨", font=("Arial", 25), cursor="hand2", bg="white", fg="black")
        client_label.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        client_label.bind("<Button-1>", lambda event: self.show_client_login())

        banker_button = tk.Button(self.frame, image=self.banker_photo, command=self.show_banker_page, borderwidth=0, bg="white")
        banker_button.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")
        banker_label = tk.Label(self.frame, text="✨Banker✨", font=("Arial", 25), cursor="hand2", bg="white", fg="black")
        banker_label.grid(row=2, column=1, padx=20, pady=10, sticky="nsew")
        banker_label.bind("<Button-1>", lambda event: self.show_banker_page())
    
    def show_client_login(self):
        self.clear_frame()
        tk.Label(self.frame, text="Client Login Page", font=("Arial", 14), bg="white", fg="black").pack(pady=20)
        
        inscription_button = tk.Button(self.frame, image=self.inscription_photo, command=self.show_inscription_client, bg="white", bd=0)
        inscription_button.pack(side=tk.LEFT, padx=20, pady=10, expand=True, fill=tk.BOTH)
        tk.Label(self.frame, text="Registration", font=("Arial", 12), bg="white", fg="black").pack(side=tk.LEFT, padx=20, expand=True, fill=tk.BOTH)

        connexion_button = tk.Button(self.frame, image=self.connexion_photo, command=self.show_connexion_client, bg="white", bd=0)
        connexion_button.pack(side=tk.RIGHT, padx=20, pady=10, expand=True, fill=tk.BOTH)
        tk.Label(self.frame, text="Login", font=("Arial", 12), bg="white", fg="black").pack(side=tk.RIGHT, padx=20, expand=True, fill=tk.BOTH)

        tk.Button(self.frame, text="Back to Home", command=self.show_home, bg="white", fg="black", bd=0).pack(pady=10, expand=True, fill=tk.BOTH)
    
    def show_banker_page(self):
        self.clear_frame()
        tk.Label(self.frame, text="Choose your action", font=("Arial", 14), bg="white", fg="black").pack(pady=20)
        tk.Button(self.frame, text="Registration", command=self.show_banker_registration, bg="white", fg="black").pack(pady=10, expand=True, fill=tk.BOTH)
        tk.Button(self.frame, text="Login", command=self.show_banker_login, bg="white", fg="black").pack(pady=10, expand=True, fill=tk.BOTH)
        tk.Button(self.frame, text="Back", command=self.show_home, bg="white", fg="black").pack(pady=10, expand=True, fill=tk.BOTH)
    
    def show_banker_registration(self):
        self.clear_frame()
        
        tk.Label(self.frame, text="Banker registration", font=("Arial", 14), bg="white", fg="black").pack(pady=10)
        
        tk.Label(self.frame, text="Name:", bg="white", fg="black").pack()
        self.name_entry = tk.Entry(self.frame)
        self.name_entry.pack(expand=True, fill=tk.BOTH)
        
        tk.Label(self.frame, text="Surname:", bg="white", fg="black").pack()
        self.surname_entry = tk.Entry(self.frame)
        self.surname_entry.pack(expand=True, fill=tk.BOTH)
        
        tk.Label(self.frame, text="Email:", bg="white", fg="black").pack()
        self.email_entry = tk.Entry(self.frame)
        self.email_entry.pack(expand=True, fill=tk.BOTH)
        
        tk.Label(self.frame, text="Password:", bg="white", fg="black").pack()
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.pack(expand=True, fill=tk.BOTH)
        
        tk.Button(self.frame, text="Register", command=self.register_banker, bg="white", fg="black").pack(pady=10, expand=True, fill=tk.BOTH)
        tk.Button(self.frame, text="Back", command=self.show_banker_page, bg="white", fg="black").pack(pady=10, expand=True, fill=tk.BOTH)
    
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
        self.login_email_entry.pack(expand=True, fill=tk.BOTH)
        
        tk.Label(self.frame, text="Password:", bg="white", fg="black").pack()
        self.login_password_entry = tk.Entry(self.frame, show="*")
        self.login_password_entry.pack(expand=True, fill=tk.BOTH)
        
        tk.Button(self.frame, text="Login", command=self.login_banker, bg="white", fg="black").pack(pady=10, expand=True, fill=tk.BOTH)
        tk.Button(self.frame, text="Back", command=self.show_banker_page, bg="white", fg="black").pack(pady=10, expand=True, fill=tk.BOTH)
    
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
        PortefeuilleClientApp(self.frame, ID_banker, back_callback=self.show_home)
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def show_inscription_client(self):
        self.clear_frame()
        tk.Label(self.frame, text="Client Registration Form", font=("Arial", 14), bg="white", fg="black").pack(pady=20)
        
        tk.Label(self.frame, text="Name:", font=("Arial", 12), bg="white", fg="black").pack(pady=5)
        self.nom_entry = tk.Entry(self.frame)
        self.nom_entry.pack(pady=5, expand=True, fill=tk.BOTH)
        
        tk.Label(self.frame, text="Surname:", font=("Arial", 12), bg="white", fg="black").pack(pady=5)
        self.prenom_entry = tk.Entry(self.frame)
        self.prenom_entry.pack(pady=5, expand=True, fill=tk.BOTH)
        
        tk.Label(self.frame, text="Email:", font=("Arial", 12), bg="white", fg="black").pack(pady=5)
        self.email_entry = tk.Entry(self.frame)
        self.email_entry.pack(pady=5, expand=True, fill=tk.BOTH)
        
        tk.Label(self.frame, text="Password:", font=("Arial", 12), bg="white", fg="black").pack(pady=5)
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.pack(pady=5, expand=True, fill=tk.BOTH)
        
        tk.Button(self.frame, text="Register", command=self.register_client, bg="white", fg="black", bd=0).pack(pady=10, expand=True, fill=tk.BOTH)
        tk.Button(self.frame, text="Back", command=self.show_client_login, bg="white", fg="black", bd=0).pack(pady=10, expand=True, fill=tk.BOTH)
    
    def register_client(self):
        name = self.nom_entry.get()
        surname = self.prenom_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        if not (name and surname and email and password):
            messagebox.showwarning("Error", "Fill in all fields!")
            return
        
        hashed_password = self.hash_password(password)
        add_client(name, surname, email, hashed_password)
        messagebox.showinfo("Success", "Registration successful!")
        self.show_client_login()

    def show_connexion_client(self):
        self.clear_frame()
        tk.Label(self.frame, text="Client Login Form", font=("Arial", 14), bg="white", fg="black").pack(pady=20)
        
        tk.Label(self.frame, text="Email:", font=("Arial", 12), bg="white", fg="black").pack(pady=5)
        self.email_entry = tk.Entry(self.frame)
        self.email_entry.pack(pady=5, expand=True, fill=tk.BOTH)
        
        tk.Label(self.frame, text="Password:", font=("Arial", 12), bg="white", fg="black").pack(pady=5)
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.pack(pady=5, expand=True, fill=tk.BOTH)
        
        tk.Button(self.frame, text="Login", command=self.login_client, bg="white", fg="black", bd=0).pack(pady=10, expand=True, fill=tk.BOTH)
        tk.Button(self.frame, text="Back", command=self.show_client_login, bg="white", fg="black", bd=0).pack(pady=10, expand=True, fill=tk.BOTH)
    
    def login_client(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        client_id = verify_client(email, password)
        if client_id:
            self.clear_frame()
            ClientAccountApp(self.frame, client_id, back_callback=self.show_home)
        else:
            messagebox.showerror("Login Error", "Incorrect email or password")

if __name__ == '__main__':
    root = tk.Tk()
    app = BankingApp(root)
    root.mainloop()