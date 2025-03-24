import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import *
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
        
        # Main frame
        self.frame = tk.Frame(self.root, bg="#917d8f") 
        self.frame.place(relx=0.5, rely=0.5, anchor="center", width=screen_width * 0.9, height=screen_height * 0.6)
        
        self.load_images()
        self.show_home()

    def round_corners(self, image, radius):
        # Create a mask with rounded corners
        mask = Image.new("L", image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0, image.size[0], image.size[1]), radius=radius, fill=255)
        image.putalpha(mask)
        return image

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
        self.logo_photo = self.load_image("images/logo.png", (100, 100), radius=20)  # Adjust image size and radius

        self.client_photo = self.load_image("images/client.png", (400, 500), radius=40)  # Adjust image size and radius
        self.banker_photo = self.load_image("images/bank.png", (400, 500), radius=40)  # Adjust image size and radius

        self.inscription_photo = self.load_image("images/regi.png", (400, 400), radius=50)  # Adjust image size and radius
        self.connexion_photo = self.load_image("images/log.png", (400, 400), radius=50)  # Adjust image size and radius

    def load_image(self, image_path, size, radius=None):
        if os.path.exists(image_path):
            img = Image.open(image_path).resize(size)

            if radius:
                img = self.round_corners(img, radius)
                print(f"Image loaded: {image_path}")  #  debug message
            return ImageTk.PhotoImage(img)
        else:
            print(f"Image not found: {image_path}")
            return None
    
    def clear_frame(self):
    #    Clean frame
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        # Clean heding if it exists
        if hasattr(self, 'title_label'):
            self.title_label.destroy()
    
    def show_home(self):
        self.clear_frame()

        self.title_label = tk.Label(self.root, text="Optimize Your Finances like your code", font=("Arial", 24, "bold"), fg="white", bg="#5E5E5E", padx=20, pady=10)
        self.title_label.place(relx=0.5, y=20, anchor="n")

        # Left side - client
        client_image_label = tk.Label(self.frame, image=self.client_photo, bg="#FB84AE")
        client_image_label.place(relx=0.25, rely=0.3, anchor="center") 
        
        # Right side - banker
        banker_image_label = tk.Label(self.frame, image=self.banker_photo, bg="#FB84AE")
        banker_image_label.place(relx=0.75, rely=0.3, anchor="center")  
        
        #  Button for client
        client_button = tk.Button(self.frame, text="✨Customer✨", font=("Arial", 18, "bold"), bg="#5E5E5E", fg="white", borderwidth=0, command=self.show_client_login)
        client_button.place(relx=0.25, rely=0.9, anchor="center")  
        
        # Button for banker
        banker_button = tk.Button(self.frame, text="✨Banker✨", font=("Arial", 18, "bold"), bg="#5E5E5E", fg="white", borderwidth=0, command=self.show_banker_page)
        banker_button.place(relx=0.75, rely=0.9, anchor="center")  
    
    def show_client_login(self):
        self.clear_frame()

        self.title_label = tk.Label(self.root, text="✨ It's gone! ✨", font=("Arial", 24, "bold"), fg="white", bg="#5E5E5E", padx=20, pady=10)
        self.title_label.place(relx=0.5, y=20, anchor="n")
        
        # Left side - Registration
        inscription_label_b = tk.Label(self.frame, image=self.inscription_photo, bg="#917d8f", bd=0)
        inscription_label_b.place(relx=0.25, rely=0.3, anchor="center")

        # Button for Registration
        registration_button = tk.Button(self.frame, text="✨ Registration", font=("Arial", 18, "bold"), bg="#5E5E5E", fg="white", borderwidth=0, command=self.show_inscription_client)
        registration_button.place(relx=0.25, rely=0.8, anchor="center")

        registration_label_c = tk.Label(self.frame, text="Welcome customer", font=("Arial", 12, "bold"), bg="#5E5E5E", fg="white", borderwidth=0)
        registration_label_c.place(relx=0.25, rely=0.95, anchor="center")

        # Right side - Login
        connexion_label_c = tk.Label(self.frame, image=self.connexion_photo, bg="#917d8f", bd=0)
        connexion_label_c.place(relx=0.75, rely=0.3, anchor="center")

        # Button for Login
        login_button = tk.Button(self.frame, text="Login ✨", font=("Arial", 18, "bold"), bg="#5E5E5E", fg="white", borderwidth=0, command=self.show_connexion_client)
        login_button.place(relx=0.75, rely=0.8, anchor="center")

        login_label_b = tk.Label(self.frame, text="Nice to see you again", font=("Arial", 12, "bold"), bg="#5E5E5E", fg="white", borderwidth=0)
        login_label_b.place(relx=0.75, rely=0.95, anchor="center")

        back_button = tk.Button(self.frame, text="Back", font=("Arial", 18, "bold"), bg="#5E5E5E", fg="white", borderwidth=0, command=self.show_home)
        back_button.place(relx=0.5, rely=0.8, anchor="center")
   
         
    def show_banker_page(self):
        self.clear_frame()

        self.title_label = tk.Label(self.root, text="✨ It's gone! ✨", font=("Arial", 24, "bold"), fg="white", bg="#5E5E5E", padx=20, pady=10)
        self.title_label.place(relx=0.5, y=20, anchor="n")

        # Left side - Registration
        inscription_label_b = tk.Label(self.frame, image=self.inscription_photo, bg="#917d8f", bd=0)
        inscription_label_b.place(relx=0.25, rely=0.3, anchor="center")

        # Button for Registration
        registration_button = tk.Button(self.frame, text="✨ Registration", font=("Arial", 18, "bold"), bg="#5E5E5E", fg="white", borderwidth=0, command=self.show_banker_registration)
        registration_button.place(relx=0.25, rely=0.8, anchor="center")

        registration_label_b = tk.Label(self.frame, text="Welcome banker", font=("Arial", 12, "bold"), bg="#5E5E5E", fg="white", borderwidth=0)
        registration_label_b.place(relx=0.25, rely=0.95, anchor="center")

        # Right side - Login
        connexion_label_b = tk.Label(self.frame, image=self.connexion_photo, bg="#917d8f", bd=0)
        connexion_label_b.place(relx=0.75, rely=0.3, anchor="center")

        # Button for Login
        login_button = tk.Button(self.frame, text="Login ✨", font=("Arial", 18, "bold"), bg="#5E5E5E", fg="white", borderwidth=0, command=self.show_banker_login)
        login_button.place(relx=0.75, rely=0.8, anchor="center")

        login_label_b = tk.Label(self.frame, text="Nice to see you again", font=("Arial", 12, "bold"), bg="#5E5E5E", fg="white", borderwidth=0)
        login_label_b.place(relx=0.75, rely=0.95, anchor="center")

        back_button = tk.Button(self.frame, text="Back", font=("Arial", 18, "bold"), bg="#5E5E5E", fg="white", borderwidth=0, command=self.show_home)
        back_button.place(relx=0.5, rely=0.8, anchor="center")

    def show_banker_registration(self):
        self.clear_frame()
        
        self.title_label = tk.Label(
            self.root,
            text="WELCOME TO YOUR NEW LIFE WITH YOUR FINANCES",
            font=("Arial", 24, "bold"),
            bg="#757D86", 
            fg="white",
            padx=20,
            pady=10
        )
        self.title_label.place(relx=0.5, rely=0.8, anchor="s") 
        
        # Registration form frame
        form_frame = Frame(self.frame, bg="#757D86", bd=5, relief="ridge")
        form_frame.place(relx=0.5, rely=0.4, anchor="center", width=550, height=370)
        
        self.first_name_entry = Entry(form_frame, font=("Arial", 12), bg="#F0F0F0", fg="gray")
        self.first_name_entry.insert(0, "Name") 
        self.first_name_entry.bind("<FocusIn>", lambda e: self.first_name_entry.delete(0, END))
        self.first_name_entry.pack(pady=5, fill=X, padx=20)
        
        self.name_entry = Entry(form_frame, font=("Arial", 12), bg="#F0F0F0", fg="gray")
        self.name_entry.insert(0, "Surame")
        self.name_entry.bind("<FocusIn>", lambda e: self.name_entry.delete(0, END))
        self.name_entry.pack(pady=5, fill=X, padx=20)
        
        self.email_entry = Entry(form_frame, font=("Arial", 12), bg="#F0F0F0", fg="gray")
        self.email_entry.insert(0, "Email")  
        self.email_entry.bind("<FocusIn>", lambda e: self.email_entry.delete(0, END))
        self.email_entry.pack(pady=5, fill=X, padx=20)
            
        self.password_entry = Entry(form_frame, font=("Arial", 12), bg="#F0F0F0", fg="gray", show="*")
        self.password_entry.insert(0, "Password")  
        self.password_entry.bind("<FocusIn>", lambda e: self.password_entry.delete(0, END))
        self.password_entry.pack(pady=5, fill=X, padx=20)

        # Password requirements
        password_requirements = Label(
            form_frame,
            text="Please adhere to the following requirements:\n"
                "10 character maximum.\n"
                "1 uppercase letter required.\n"
                "1 special character required.\n"
                "1 number required.",
            font=("Arial", 10), bg="white", fg="black", justify=LEFT
        )
        password_requirements.pack(pady=10)
        
        register_button = Button(form_frame, text="Save", font=("Arial", 14, "bold"), bg="#FFD700", fg="black", borderwidth=0, command=self.register_banker)
        register_button.pack(pady=20, fill=X, padx=20)

        back_button = Button(form_frame, text="Back",  font=("Arial", 14, "bold"), command=self.show_banker_page, bg="#5E5E5E", fg="white", borderwidth=0)
        back_button.pack(pady=10, fill=tk.X, padx=20)
    
    def register_banker(self):
        name = self.first_name_entry.get()
        surname = self.name_entry.get()
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
        
        self.title_label = tk.Label(
            self.root,
            text="Welcome back with us",
            font=("Arial", 24, "bold"),
            bg="#757D86", 
            fg="white",
            padx=20,
            pady=10
        )
        # self.title_label.place(relx=0.5, rely=0.8, anchor="s") 
        
        # tk.Label(self.frame, text="Email:", bg="white", fg="black").pack()
        # self.login_email_entry = tk.Entry(self.frame)
        # self.login_email_entry.pack()
        
        # tk.Label(self.frame, text="Password:", bg="white", fg="black").pack()
        # self.login_password_entry = tk.Entry(self.frame, show="*")
        # self.login_password_entry.pack()
        
        # tk.Button(self.frame, text="Login", command=self.login_banker, bg="white", fg="black").pack(pady=10)
        # tk.Button(self.frame, text="Back", command=self.show_banker_page, bg="white", fg="black").pack(pady=10)

        # Login form frame
        form_frame = Frame(self.frame, bg="#757D86", bd=5, relief="ridge")
        form_frame.place(relx=0.5, rely=0.4, anchor="center", width=550, height=300)

        # Download picture
        self.login_bg_image = self.load_image("images/login.png", (550, 300), radius=20)

        if self.login_bg_image:
            login_bg_label = Label(form_frame, image=self.login_bg_image, bg="#757D86")
            login_bg_label.place(x=0, y=0, relwidth=1, relheight=1)


        # Email field
        email_label = Label(form_frame, text="Email", font=("Arial", 12), bg="#757D86", fg="white")
        email_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.login_email_entry = Entry(form_frame, font=("Arial", 12), bg="#F0F0F0", fg="gray")
        self.login_email_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Password field
        password_label = Label(form_frame, text="Password", font=("Arial", 12), bg="#757D86", fg="white")
        password_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.login_password_entry = Entry(form_frame, font=("Arial", 12), bg="#F0F0F0", fg="gray", show="*")
        self.login_password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Login button
        login_button = Button(form_frame, text="Login", font=("Arial", 14, "bold"), bg="#FFD700", fg="black", borderwidth=0, command=self.login_banker)
        login_button.grid(row=2, column=0, columnspan=2, pady=20, padx=10, sticky="ew")

        # Back button
        back_button = Button(form_frame, text="Back", font=("Arial", 14, "bold"), bg="#5E5E5E", fg="white", borderwidth=0, command=self.show_banker_page)
        back_button.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        # Configure grid weights to make the form responsive
        form_frame.grid_columnconfigure(1, weight=1)
    
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

        # Додаємо обробник подій для Treeview
        tree.bind('<Button-1>', lambda event: self.on_client_selected(event, tree))
    
        tk.Button(self.frame, text="Back", command=self.show_banker_page, bg="white", fg="black").pack(pady=10)
    
    def on_client_selected(self, event, tree):
        item = tree.identify_row(event.y) 
        if item:
            client_id = tree.item(item, 'values')[0]  
            self.show_client_account(client_id)

    def show_client_account(self, client_id):
        self.clear_frame()
        ClientAccountApp(self.frame, client_id, back_callback=self.show_home)

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

        self.title_label = tk.Label(
            self.root,
            text="WELCOME TO YOUR NEW LIFE WITH YOUR FINANCES",
            font=("Arial", 24, "bold"),
            bg="#757D86", 
            fg="white",
            padx=20,
            pady=10
        )
        self.title_label.place(relx=0.5, rely=0.8, anchor="s")
        
        # Registration form frame
        form_frame = Frame(self.frame, bg="#757D86", bd=5, relief="ridge")
        form_frame.place(relx=0.5, rely=0.4, anchor="center", width=550, height=370)
        
        self.name_entry_c = Entry(form_frame, font=("Arial", 12), bg="#F0F0F0", fg="gray")
        self.name_entry_c.insert(0, "Name") 
        self.name_entry_c.bind("<FocusIn>", lambda e: self.name_entry_c.delete(0, END))
        self.name_entry_c.pack(pady=5, fill=X, padx=20)

        self.surname_entry_c = Entry(form_frame, font=("Arial", 12), bg="#F0F0F0", fg="gray")
        self.surname_entry_c.insert(0, "Surame")
        self.surname_entry_c.bind("<FocusIn>", lambda e: self.surname_entry_c.delete(0, END))
        self.surname_entry_c.pack(pady=5, fill=X, padx=20)
        
        self.email_entry_c = Entry(form_frame, font=("Arial", 12), bg="#F0F0F0", fg="gray")
        self.email_entry_c.insert(0, "Email")  
        self.email_entry_c.bind("<FocusIn>", lambda e: self.email_entry_c.delete(0, END))
        self.email_entry_c.pack(pady=5, fill=X, padx=20)
            
        self.password_entry_c = Entry(form_frame, font=("Arial", 12), bg="#F0F0F0", fg="gray", show="*")
        self.password_entry_c.insert(0, "Password")  
        self.password_entry_c.bind("<FocusIn>", lambda e: self.password_entry_c.delete(0, END))
        self.password_entry_c.pack(pady=5, fill=X, padx=20)

        # Password requirements
        password_requirements = Label(
            form_frame,
            text="Please adhere to the following requirements:\n"
                "10 character maximum.\n"
                "1 uppercase letter required.\n"
                "1 special character required.\n"
                "1 number required.",
            font=("Arial", 10), bg="white", fg="black", justify=LEFT
        )
        password_requirements.pack(pady=10)
        
        register_button = Button(form_frame, text="Save", font=("Arial", 14, "bold"), bg="#FFD700", fg="black", borderwidth=0, command=self.register_client)
        register_button.pack(pady=20, fill=X, padx=20)

        back_button = Button(form_frame, text="Back",  font=("Arial", 14, "bold"), command=self.show_client_login, bg="#5E5E5E", fg="white", borderwidth=0)
        back_button.pack(pady=10, fill=tk.X, padx=20)
    
    def register_client(self):
        name = self.name_entry_c.get()
        surname = self.surname_entry_c.get()
        email = self.email_entry_c.get()
        password = self.password_entry_c.get()
        
        if not (name and surname and email and password):
            messagebox.showwarning("Error", "Fill in all fields!")
            return
        
        hashed_password = self.hash_password(password)
        add_client(name, surname, email, hashed_password)
        messagebox.showinfo("Success", "Registration successful!")
        self.show_client_login()

    def show_connexion_client(self):
        self.clear_frame()

        self.title_label = tk.Label(
            self.root,
            text="Welcome back with us",
            font=("Arial", 24, "bold"),
            bg="#757D86", 
            fg="white",
            padx=20,
            pady=10
        )
        # Login form frame
        form_frame = Frame(self.frame, bg="#757D86", bd=5, relief="ridge")
        form_frame.place(relx=0.5, rely=0.4, anchor="center", width=550, height=300)

        # Download picture
        self.login_bg_image = self.load_image("images/login.png", (550, 300), radius=20)

        if self.login_bg_image:
            login_bg_label = Label(form_frame, image=self.login_bg_image, bg="#757D86")
            login_bg_label.place(x=0, y=0, relwidth=1, relheight=1)


        # Email field
        email_label = Label(form_frame, text="Email", font=("Arial", 12), bg="#757D86", fg="white")
        email_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.login_email_entry = Entry(form_frame, font=("Arial", 12), bg="#F0F0F0", fg="gray")
        self.login_email_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Password field
        password_label = Label(form_frame, text="Password", font=("Arial", 12), bg="#757D86", fg="white")
        password_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.login_password_entry = Entry(form_frame, font=("Arial", 12), bg="#F0F0F0", fg="gray", show="*")
        self.login_password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Login button
        login_button = Button(form_frame, text="Login", font=("Arial", 14, "bold"), bg="#FFD700", fg="black", borderwidth=0, command=self.login_client)
        login_button.grid(row=2, column=0, columnspan=2, pady=20, padx=10, sticky="ew")

        # Back button
        back_button = Button(form_frame, text="Back", font=("Arial", 14, "bold"), bg="#5E5E5E", fg="white", borderwidth=0, command=self.show_client_login)
        back_button.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        # Configure grid weights to make the form responsive
        form_frame.grid_columnconfigure(1, weight=1)
    
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