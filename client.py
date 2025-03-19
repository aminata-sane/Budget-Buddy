import tkinter as tk
from PIL import Image, ImageTk

def show_client_login():
    # Clear the window
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Create new content for client page 
    tk.Label(frame, text="Client Login Page", font=("Arial", 14), bg="#935AB7", fg="white").pack(pady=20)
    tk.Button(frame, text="Back to Home", command=show_home, bg="#935AB7", fg="white", bd=0).pack(pady=10)

def show_banker_login():
    # Clear the window
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Create new content for banker page
    tk.Label(frame, text="Banker Login Page", font=("Arial", 14), bg="#935AB7", fg="white").pack(pady=20)
    tk.Button(frame, text="Back to Home", command=show_home, bg="#935AB7", fg="white", bd=0).pack(pady=10)

def show_home():
    # Clear the window
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Create home page with buttons
    client_button = tk.Button(frame, image=client_photo, command=show_client_login, bg="#935AB7", bd=0)
    client_button.grid(row=1, column=0, padx=20, pady=10)
    tk.Label(frame, text="Client", font=("Arial", 12), bg="#935AB7", fg="white").grid(row=2, column=0)
    
    banker_button = tk.Button(frame, image=banker_photo, command=show_banker_login, bg="#935AB7", bd=0)
    banker_button.grid(row=1, column=1, padx=20, pady=10)
    tk.Label(frame, text="Banker", font=("Arial", 12), bg="#935AB7", fg="white").grid(row=2, column=1)

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
root.configure(bg="#935AB7")

# Add logo and slogan
logo_label = tk.Label(root, text="Bank Logo", font=("Arial", 24), bg="#935AB7", fg="white")
logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

slogan_label = tk.Label(root, text="Your Friendly Bank !", font=("Arial", 16), bg="#935AB7", fg="white")
slogan_label.grid(row=0, column=1, padx=10, pady=5, sticky="n")

frame = tk.Frame(root, bg="#935AB7")
frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

# Download photos
client_img = Image.open("images/client.png").resize((screen_width // 2, screen_height - 200))  # Ajuster la hauteur des images
client_photo = ImageTk.PhotoImage(client_img)

banker_img = Image.open("images/bank.png").resize((screen_width // 2, screen_height - 200))  # Ajuster la hauteur des images
banker_photo = ImageTk.PhotoImage(banker_img)

# New page
show_home()

root.mainloop()