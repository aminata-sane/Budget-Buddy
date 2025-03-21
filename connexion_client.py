import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import verify_client

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Connexion Client")

        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self.root, text="Formulaire de Connexion Client")
        self.label.pack(pady=10)

        self.email_label = ttk.Label(self.root, text="Email:")
        self.email_label.pack(pady=5)
        self.email_entry = ttk.Entry(self.root)
        self.email_entry.pack(pady=5)

        self.mot_de_passe_label = ttk.Label(self.root, text="Mot de passe:")
        self.mot_de_passe_label.pack(pady=5)
        self.mot_de_passe_entry = ttk.Entry(self.root, show="*")
        self.mot_de_passe_entry.pack(pady=5)

        self.login_button = ttk.Button(self.root, text="Se connecter", command=self.login_client)
        self.login_button.pack(pady=10)

    def login_client(self):
        email = self.email_entry.get()
        mot_de_passe = self.mot_de_passe_entry.get()

        if email and mot_de_passe:
            try:
                if verify_client(email, mot_de_passe):
                    messagebox.showinfo("Succès", "Connexion réussie!")
                else:
                    messagebox.showwarning("Erreur", "Email ou mot de passe incorrect.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la connexion : {e}")
        else:
            messagebox.showwarning("Erreur", "Tous les champs sont obligatoires!")

if __name__ == '__main__':
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()