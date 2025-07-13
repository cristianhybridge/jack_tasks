from tkinter import ttk

def configure_styles():
    
    # Debe ser llamado una vez al inicio de la aplicación.
    style = ttk.Style()

    # Estilo global
    style.theme_use("clam")

    # Estilo para el título principal
    style.configure("main_title.TLabel",
                    font=("Arial", 20, "bold"),
                    foreground="white",
                    background="#5E8BA8",
                    padding=10)
    
    style.configure("main_title_green.TLabel",
                    font=("Arial", 20, "bold"),
                    foreground="white",
                    background="darkgreen",
                    padding=10)
    
    style.configure("main_title_blue.TLabel",
                    font=("Arial", 20, "bold"),
                    foreground="white",
                    background="darkblue",
                    padding=10)
    
    # Estilo para background de frames
    style.configure("taskview_frame.TFrame",
                    background="lightblue")

    style.configure("main_button.TButton",
                    font=("Helvetica", 10, "bold"),
                    foreground="white",
                    background="#67B6B9",
                    padding=5)
    style.map("main_button.TButton",
              foreground=[('pressed', 'gray'), ('active', 'lightblue')],
              background=[('pressed', '!disabled', '#45a049'), ('active', '#5CB85C')])
    
    style.configure("submit_button.TButton",
                    font=("Helvetica", 10, "bold"),
                    foreground="white",
                    background="darkblue",
                    padding=5)
    style.map("submit_button.TButton",
              foreground=[('pressed', 'white'), ('active', 'white')],
              background=[('pressed', '!disabled', 'black'), ('active', 'darkblue')])


    style.configure("TaskTitle.TLabel",
                    background="lightblue",
                    foreground="#333333",
                    font=("Helvetica", 10, "bold"),
                    padding=5,
                    relief="solid",
                    borderwidth=1)
    style.map("TaskTitle.TLabel",
              background=[('active', 'black')])

    style.configure("basic_text.TLabel",
                    font=("Arial", 10),
                    foreground="black")