# app_styles.py

from tkinter import ttk

def configure_styles():
    """
    Configura todos los estilos de ttk para la aplicación.
    Debe ser llamado una vez al inicio de la aplicación.
    """
    style = ttk.Style()

    # Puedes elegir un tema global si lo deseas
    # style.theme_use("clam") # O "alt", "default", "winnative" (solo Windows)

    # Estilo para el título principal
    
    
    style.configure("main_title.TLabel",
                    font=("Arial", 20, "bold"),
                    foreground="#3e32a8",
                    background="lightblue",
                    padding=10)
    
    # Estilo para background de frames
        # Background frame TaskView
    style.configure("taskview_frame.TFrame",
                    background="#e0ffe0")

    # Estilo para botones
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
                    background="#00ad23",
                    padding=5)
    style.map("submit_button.TButton",
              foreground=[('pressed', 'gray'), ('active', 'lightblue')],
              background=[('pressed', '!disabled', '#45a049'), ('active', '#5CB85C')])

    style.configure("secondary_button.TButton",
                    font=("Helvetica", 10, "bold"),
                    foreground="white",
                    background="#FF9A8D",
                    padding=5)
    style.map("secondary_button_button.TButton",
              foreground=[('pressed', 'gray'), ('active', 'lightblue')],
              background=[('pressed', '!disabled', '#45a049'), ('active', '#5CB85C')])

    style.configure("danger_button.TButton",
                    font=("Helvetica", 10, "bold"),
                    foreground="white",
                    background="#FF9A8D",
                    padding=5)
    style.map("danger_button_button.TButton",
              foreground=[('pressed', 'gray'), ('active', 'lightblue')],
              background=[('pressed', '!disabled', '#45a049'), ('active', '#5CB85C')])


    style.configure("TaskTitle.TLabel",
                    background="#f0f0f0", # Light grey background for each task
                    foreground="#333333", # Darker text color
                    font=("Helvetica", 12, "bold"),
                    padding=5,
                    relief="solid", # A subtle border
                    borderwidth=1)
    style.configure("TaskDetail.TLabel",
                    background="#f0f0f0",
                    foreground="#666666", # Lighter text for details
                    font=("Helvetica", 10))
    style.map("TaskTitle.TLabel",
              background=[('active', '#e0e0e0')]) # Hover effect

    # Estilo para etiquetas de texto normal
    style.configure("basic_text.TLabel",
                    font=("Arial", 10),
                    foreground="black")

    # Otros estilos que necesites...
    # style.configure("CajaEntrada.TEntry", ...)
    # style.configure("MiFrame.TFrame", background="red")