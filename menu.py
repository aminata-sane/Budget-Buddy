import tkinter as tk
from PIL import Image, ImageTk
import os
import subprocess

def open_inscription_client():
    subprocess.Popen(["/usr/local/bin/python3", "/Users/mameaminataconstancesane/Desktop/Budget-Buddy/inscription_client.py"])

def open_connexion_client():
    subprocess.Popen(["/usr/local/bin/python3", "/Users/mameaminataconstancesane/Desktop/Budget-Buddy/connexion_client.py"])

def show_inscription_client():
    # Clear the window
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Create new content for inscription page
    tk.Label(frame, text="Formulaire d'inscription Client", font=("Arial", 14), bg="white", fg="black").pack(pady=20)
    
    # Add form fields
    tk.Label(frame, text="Nom:", font=("Arial", 12), bg="white", fg="black").pack(pady=5)
    tk.Entry(frame).pack(pady=5)
    
    tk.Label(frame, text="Prénom:", font=("Arial", 12), bg="white", fg="black").pack(pady=5)
    tk.Entry(frame).pack(pady=5)
    
    tk.Label(frame, text="Email:", font=("Arial", 12), bg="white", fg="black").pack(pady=5)
    tk.Entry(frame).pack(pady=5)
    
    tk.Label(frame, text="Mot de passe:", font=("Arial", 12), bg="white", fg="black").pack(pady=5)
    tk.Entry(frame, show="*").pack(pady=5)
    
    tk.Button(frame, text="S'inscrire", bg="white", fg="black", bd=0).pack(pady=10)
    tk.Button(frame, text="Back", command=show_client_login, bg="white", fg="black", bd=0).pack(pady=10)

def show_connexion_client():
    # Clear the window
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Create new content for connexion page
    tk.Label(frame, text="Formulaire de Connexion Client", font=("Arial", 14), bg="white", fg="black").pack(pady=20)
    
    # Add form fields
    tk.Label(frame, text="Email:", font=("Arial", 12), bg="white", fg="black").pack(pady=5)
    tk.Entry(frame).pack(pady=5)
    
    tk.Label(frame, text="Mot de passe:", font=("Arial", 12), bg="white", fg="black").pack(pady=5)
    tk.Entry(frame, show="*").pack(pady=5)
    
    tk.Button(frame, text="Se connecter", bg="white", fg="black", bd=0).pack(pady=10)
    tk.Button(frame, text="Back", command=show_client_login, bg="white", fg="black", bd=0).pack(pady=10)

def show_client_login():
    # Clear the window
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Create new content for client page 
    tk.Label(frame, text="Client Login Page", font=("Arial", 14), bg="white", fg="black").pack(pady=20)
    
    # Add buttons with images
    inscription_button = tk.Button(frame, image=inscription_photo, command=show_inscription_client, bg="white", bd=0)
    inscription_button.pack(side=tk.LEFT, padx=20, pady=10)
    tk.Label(frame, text="Inscription", font=("Arial", 12), bg="white", fg="black").pack(side=tk.LEFT, padx=20)

    connexion_button = tk.Button(frame, image=connexion_photo, command=show_connexion_client, bg="white", bd=0)
    connexion_button.pack(side=tk.RIGHT, padx=20, pady=10)
    tk.Label(frame, text="Connexion", font=("Arial", 12), bg="white", fg="black").pack(side=tk.RIGHT, padx=20)

    tk.Button(frame, text="Back to Home", command=show_home, bg="white", fg="black", bd=0).pack(pady=10)

def show_banker_login():
    # Clear the window
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Create new content for banker page
    tk.Label(frame, text="Banker Login Page", font=("Arial", 14), bg="white", fg="black").pack(pady=20)
    tk.Button(frame, text="Back to Home", command=show_home, bg="white", fg="black", bd=0).pack(pady=10)

def show_home():
    # Clear the window
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Create home page with buttons
    client_button = tk.Button(frame, image=client_photo, command=show_client_login, bg="white", bd=0)
    client_button.grid(row=1, column=0, padx=20, pady=10)
    tk.Label(frame, text="Client", font=("Arial", 12), bg="white", fg="black").grid(row=2, column=0)
    
    banker_button = tk.Button(frame, image=banker_photo, command=show_banker_login, bg="white", bd=0)
    banker_button.grid(row=1, column=1, padx=20, pady=10)
    tk.Label(frame, text="Banker", font=("Arial", 12), bg="white", fg="black").grid(row=2, column=1)

    # Center the frame in the window
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_rowconfigure(2, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)

root = tk.Tk()
root.title("Banking System")

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set window size to screen size
root.geometry(f"{screen_width}x{screen_height}")

# Set background color
root.configure(bg="white")

# Add logo and slogan
logo_label = tk.Label(root, text="Bank Logo", font=("Arial", 24), bg="white", fg="black")
logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

slogan_label = tk.Label(root, text="Your Friendly Bank !", font=("Arial", 16), bg="white", fg="black")
slogan_label.grid(row=0, column=1, padx=10, pady=5, sticky="n")

frame = tk.Frame(root, bg="white")
frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

# Load images for buttons
def load_image(image_path, size):
    if os.path.exists(image_path):
        img = Image.open(image_path).resize(size)
        return ImageTk.PhotoImage(img)
    else:
        print(f"Image not found: {image_path}")
        return None

client_photo = load_image("images/client.png", (screen_width // 2, screen_height - 200))
banker_photo = load_image("images/bank.png", (screen_width // 2, screen_height - 200))
inscription_photo = load_image("images/inscription.png", (100, 100))
connexion_photo = load_image("images/connexion.png", (100, 100))

# New page
show_home()

root.mainloop()