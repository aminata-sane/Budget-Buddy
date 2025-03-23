import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import verify_client

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Client Login")

        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self.root, text="Client Login Form")
        self.label.pack(pady=10)

        self.email_label = ttk.Label(self.root, text="Email:")
        self.email_label.pack(pady=5)
        self.email_entry = ttk.Entry(self.root)
        self.email_entry.pack(pady=5)

        self.password_label = ttk.Label(self.root, text="Password:")
        self.password_label.pack(pady=5)
        self.password_entry = ttk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = ttk.Button(self.root, text="Login", command=self.login_client)
        self.login_button.pack(pady=10)

    def login_client(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if email and password:
            try:
                if verify_client(email, password):
                    messagebox.showinfo("Success", "Login successful!")
                else:
                    messagebox.showwarning("Error", "Incorrect email or password.")
            except Exception as e:
                messagebox.showerror("Error", f"Error during login: {e}")
        else:
            messagebox.showwarning("Error", "All fields are required!")

if __name__ == '__main__':
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()