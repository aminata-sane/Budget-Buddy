
import tkinter as tk
from PIL import Image, ImageTk

def show_client_login():
    # Clear the window
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Create new content for client page 
    tk.Label(frame, text="Client Login Page", font=("Arial", 14)).pack(pady=20)
    tk.Button(frame, text="Back to Home", command=show_home).pack(pady=10)

def show_banker_login():
    # Clear the window
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Create new content for banker page
    tk.Label(frame, text="Banker Login Page", font=("Arial", 14)).pack(pady=20)
    tk.Button(frame, text="Back to Home", command=show_home).pack(pady=10)

def show_home():
    # Clear the window
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Create home page with buttons
    client_button = tk.Button(frame, image=client_photo, command=show_client_login)
    client_button.grid(row=0, column=0, padx=20, pady=10)
    tk.Label(frame, text="Client", font=("Arial", 12)).grid(row=1, column=0)
    
    banker_button = tk.Button(frame, image=banker_photo, command=show_banker_login)
    banker_button.grid(row=0, column=1, padx=20, pady=10)
    tk.Label(frame, text="Banker", font=("Arial", 12)).grid(row=1, column=1)

root = tk.Tk()
root.title("Banking System")
root.geometry("600x350")

frame = tk.Frame(root)
frame.pack()

# Download photos
client_img = Image.open("images/client.jpg").resize((150, 200))
client_photo = ImageTk.PhotoImage(client_img)

banker_img = Image.open("images/bank.png").resize((150, 200))
banker_photo = ImageTk.PhotoImage(banker_img)

# New page
show_home()

root.mainloop()


# import tkinter as tk
# from tkinter import messagebox
# from PIL import Image, ImageTk


# def open_client_login():
#     messagebox.showinfo("Login", "Redirecting to Client Login")
#     # Тут відкриється сторінка входу клієнта

# def open_banker_login():
#     messagebox.showinfo("Login", "Redirecting to Banker Login")
#     # Тут відкриється сторінка входу банкіра

# root = tk.Tk()
# root.title("Banking System")
# root.geometry("600x300")

# frame = tk.Frame(root)
# frame.pack()

# # Завантаження зображень
# client_img = Image.open("images/client.jpg").resize((200, 200))
# client_photo = ImageTk.PhotoImage(client_img)

# banker_img = Image.open("images/bank.png").resize((200, 200))
# banker_photo = ImageTk.PhotoImage(banker_img)

# # Кнопки із зображеннями
# client_button = tk.Button(frame, image=client_photo, command=open_client_login)
# client_button.grid(row=0, column=0, padx=20, pady=20)

# banker_button = tk.Button(frame, image=banker_photo, command=open_banker_login)
# banker_button.grid(row=0, column=1, padx=20, pady=20)

# root.mainloop()

# import tkinter as tk
# from PIL import Image, ImageTk

# def open_client_login():
#     client_window = tk.Toplevel(root)
#     client_window.title("Client Login")
#     client_window.geometry("400x200")
#     tk.Label(client_window, text="Client Login Page", font=("Arial", 14)).pack(pady=20)

# def open_banker_login():
#     banker_window = tk.Toplevel(root)
#     banker_window.title("Banker Login")
#     banker_window.geometry("400x200")
#     tk.Label(banker_window, text="Banker Login Page", font=("Arial", 14)).pack(pady=20)

# root = tk.Tk()
# root.title("Banking System")
# root.geometry("600x350")

# frame = tk.Frame(root)
# frame.pack()

# # Download photos
# client_img = Image.open("images/client.jpg").resize((200, 200))
# client_photo = ImageTk.PhotoImage(client_img)

# banker_img = Image.open("images/bank.png").resize((200, 200))
# banker_photo = ImageTk.PhotoImage(banker_img)

# # The buttons with images
# client_button = tk.Button(frame, image=client_photo, command=open_client_login)
# client_button.grid(row=0, column=0, padx=20, pady=10)
# tk.Label(frame, text="Client", font=("Arial", 12)).grid(row=1, column=0)

# banker_button = tk.Button(frame, image=banker_photo, command=open_banker_login)
# banker_button.grid(row=0, column=1, padx=20, pady=10)
# tk.Label(frame, text="Banker", font=("Arial", 12)).grid(row=1, column=1)

# root.mainloop()