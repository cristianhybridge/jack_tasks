import datetime
from tkcalendar import DateEntry
from services.tasks_service import TasksService
from services.users_service import UsersService
from views.base_view import BaseView
import tkinter as tk
from tkinter import ttk

from models.tasks_entity import TaskEntity

class TaskManagementView(BaseView):
    def __init__(self, master, show_view_callback, current_username, tasks_service: TasksService, users_service: UsersService):
        super().__init__(master, show_view_callback, current_username)
        self.config(bg="#e0ffe0")
        
        self.tasks_service = tasks_service
        
        # Variables for entries
        self.task_title_entry = None
        self.task_priority_entry = tk.StringVar(self) # Variable for storing radiogroup value
        
        # Variables for calendar
        self.task_completion_date_var = tk.StringVar(self)
        self.task_completion_date_hour_var = tk.StringVar(self, value="00")
        self.task_completion_date_minute_var = tk.StringVar(self, value="00")
        
        
        self._loaded_tasks = []
        
        # Method for the UI, similar to the html part in a razor component
            # And yes Hybridge teachers, 
        # I'm specifying these kind of paralelisms to make the code more readable to myself at least
        self._create_widgets()
        self._build_ui()

# ----------------------------------- Data loading and display -------------------------------

    def _create_widgets(self):
    # ------------------------------- FRAMES and CANVAS -------------------------------
        # Left frame: To be completed TASKS
        self.left_frame = tk.Frame(self, bg="#e0ffe0")
    
        # Right frame: Completed TASKS
        self.right_frame = tk.Frame(self, bg="#e0ffe0")

        # Frame: topleft_left_frame
        self.topleft_left_frame = tk.Frame(self.left_frame, bg="#e0ffe0")

        # Frame: task_list_frame
        self.task_list_frame = ttk.Frame(self.left_frame)
        
        # Canvas: task_canvas
        self.task_canvas = tk.Canvas(self.task_list_frame, bg="#e0ffe0", bd=0, highlightthickness=0)

        # Bindings (these are not widgets, so no separate variable for them)
        self.task_canvas.bind("<Configure>", self._on_canvas_configure)
        self.task_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    
        # Frame: inner_task_frame
        self.general_task_frame = ttk.Frame(self.task_canvas, style="TFrame")
    
        self.task_canvas.create_window((0, 0), window=self.general_task_frame, anchor="nw", width=self.task_canvas.winfo_width())


        # Frame: data_input_frame_left
        self.data_input_frame_left = ttk.Frame(self.left_frame, style="taskview_frame.TFrame")
        # Frame: data_input_frame_right
        self.data_input_frame_right = ttk.Frame(self.left_frame, style="taskview_frame.TFrame")

        self.priority_frame = ttk.Frame(self.data_input_frame_right)

        # Frame: date_time_frame
        self.date_time_frame = ttk.Frame(self.data_input_frame_right)
    # ------------------------------- ENTRIES -------------------------------
        # Textbox: task_title_entry
        self.task_title_entry = tk.Text(self.data_input_frame_left,
                                        width=35,
                                        height=5,
                                        wrap="word",
                                        font=("Helvetica", 9),
                                        bg="white",
                                        fg="black",
                                        borderwidth=1,
                                        relief="solid")

        # Date Picker: task_completion_date_entry
        self.task_completion_date_entry = DateEntry(self.date_time_frame,
                                                    selectmode='day',
                                                    date_pattern='yyyy-mm-dd',
                                                    state='readonly',
                                                    font=('Helvetica', 10),
                                                    background='darkblue',
                                                    foreground='white',
                                                    bordercolor='gray',
                                                    headersbackground='darkblue',
                                                    headersforeground='white')

        # Hour Spinbox: task_completion_hour_entry
        self.task_completion_hour_entry = ttk.Spinbox(self.date_time_frame,
                                                      from_=0, to=23,
                                                      wrap=True,
                                                      textvariable=self.task_completion_date_hour_var, # Make sure this var is defined!
                                                      width=3,
                                                      format="%02.0f")

        # Minute Spinbox: task_completion_minute_entry
        self.task_completion_minute_entry = ttk.Spinbox(self.date_time_frame,
                                                        from_=0, to=59,
                                                        wrap=True,
                                                        textvariable=self.task_completion_date_minute_var, # Make sure this var is defined!
                                                        width=3,
                                                        format="%02.0f")
    # ------------------------------- LABELS -------------------------------
        # Label: "Administrar tareas"
        self.admin_tasks_label = ttk.Label(self,
                                           text="Administrar tareas",
                                           style="main_title.TLabel")

        # Label: "Describe tu tarea:"
        self.task_description_label = ttk.Label(self.data_input_frame_left, text="Describe tu tarea:", style="secondary_label.TLabel")

        # Label: "Prioridad:"
        self.priority_label = ttk.Label(self.data_input_frame_right, text="Prioridad:", style="secondary_label.TLabel")

        # Label: "Fecha límite:"
        self.due_date_label = ttk.Label(self.data_input_frame_right, text="Fecha límite:", style="secondary_label.TLabel")

        # Label: Separator for time
        self.time_separator_label = ttk.Label(self.date_time_frame, text=":", style="secondary_label.TLabel")

   
    # ------------------------------- BUTTONS -------------------------------
        # Button: "Ajustes"
        self.settings_button = ttk.Button(self.right_frame,
                                          text="Ajustes",
                                          style="secondary_button.TButton",
                                          command=lambda: self.navigate_to("options"))

        # Button: "Volver"
        self.back_button = ttk.Button(self.topleft_left_frame,
                                      text="Volver",
                                      style="main_button.TButton",
                                      command=lambda: self.navigate_to("main"))

        self.add_button = ttk.Button(self.left_frame, text="Agregar",
                                     style="submit_button.TButton",
                                     command=self._add_new_task)
    
        # Radiobutton: Urgente
        self.priority_button_urgente = ttk.Radiobutton(self.priority_frame,
                                                       text="Urgente",
                                                       variable=self.task_priority_entry,
                                                       value="Urgente",
                                                       style="TCheckbutton")

        # Radiobutton: Importante
        self.priority_button_importante = ttk.Radiobutton(self.priority_frame,
                                                          text="Importante",
                                                          variable=self.task_priority_entry,
                                                          value="Importante",
                                                          style="TCheckbutton")

        # Radiobutton: Normal
        self.priority_button_normal = ttk.Radiobutton(self.priority_frame,
                                                      text="Normal",
                                                      variable=self.task_priority_entry,
                                                      value="Normal",
                                                      style="TCheckbutton")

    
    # ------------------------------- SCROLLBAR -------------------------------
        self.task_scrollbar = ttk.Scrollbar(self.task_list_frame, 
                                            orient="vertical", 
                                            command=self.task_canvas.yview)
    
    # Una vez cargados todos los frames, procedemos a desplegar los tasks
        self._load_tasks()
    
    
    def _build_ui(self):
    # ------------------------------- ------ -------------------------------
    # ------------------------------- Layout -------------------------------
    # ------------------------------- ------ -------------------------------
        # Packing frames
        self.left_frame.pack(side="left", fill="both", padx=10)
        self.right_frame.pack(side="right", fill="both", padx=10)
    
    # ------------------------------- CENTERED UI -------------------------------
        
        self.admin_tasks_label.pack(pady=(50,20))
    
    # ------------------------------- RIGHT FRAME -------------------------------
        
        self.settings_button.pack(pady=10)
    
    # ------------------------------- LEFT FRAME -------------------------------
        
        self.topleft_left_frame.pack(side="left", fill="y")
    
        self.back_button.pack(pady=10)
    
    # ------------------------------- Data loading and display -------------------------------
        
        self.task_list_frame.pack(pady=10, padx=10, fill="x", expand=True)
    
        # Canvas: task_canvas
        self.task_canvas.pack(side="left", fill="x", expand=True)
    
        # Scrollbar: task_scrollbar
        self.task_scrollbar.pack(side="right", fill="y")
        self.task_canvas.configure(yscrollcommand=self.task_scrollbar.set)
    
    
    
        # Packing data input frames
        self.data_input_frame_left.pack(side="left", pady=10, padx=10)
        self.data_input_frame_right.pack(side="right", pady=10, padx=10)
    
        self.task_description_label.pack(pady=(10, 0))
        
        self.task_title_entry.pack(pady=10, fill="x", expand=True)
    
    
        # Frame: priority_frame (to hold radio buttons)
        self.priority_frame.pack(pady=5)
        
    # --- START TIME PICKER ---
    
        self.due_date_label.pack(pady=(10, 0))
    
        
        self.date_time_frame.pack(pady=5)
    
        
        self.task_completion_date_entry.pack(side="left", padx=5)
    
        
        self.task_completion_hour_entry.pack(side="left")
    
        
        self.time_separator_label.pack(side="left")
    
        
        self.task_completion_minute_entry.pack(side="left")
    
    # --- END TIME PICKER ---
    
    # --- START RADIO BUTTONS ---
        self.priority_label.pack(pady=(10, 0))
    
        self.task_priority_entry.set("Normal") # Default selection
        
        self.priority_button_urgente.pack(side="left", padx=10)
    
        
        self.priority_button_importante.pack(side="left", padx=10)
    
        
        self.priority_button_normal.pack(side="left", padx=10)
        
    # --- END RADIO BUTTONS ---
    
        self.add_button.pack(padx=10)

    def _add_new_task(self):
        
        # Registra la entrada en la variable
            # get obtiene el texto de task_title_entry
                # strip elimina los espacios en blanco al inicio y al final
        var_task_entity_title = self.task_title_entry.get("1.0", "end-1c").strip() 
        var_task_entity_priority = self.task_priority_entry.get()
        var_task_entity_completion_date = self.task_completion_date_entry.get_date()
        var_task_user_id = self.current_username
        
        var_completion_hour_str = self.task_completion_date_hour_var.get()
        var_completion_minute_str = self.task_completion_date_minute_var.get()
        
        # Variable for joining complete datetime (date+hours+minutes)
        var_complete_datetime = None
        
        if var_task_entity_completion_date: # Check if a date was actually selected
            try:
                selected_hour = int(var_completion_hour_str)
                selected_minute = int(var_completion_minute_str)
                # Combine the date object with a time object
                var_complete_datetime = datetime.datetime.combine(
                    var_task_entity_completion_date, 
                    datetime.time(selected_hour, selected_minute))
            except ValueError:
                print("Internal error.")
                # Consider showing a message box to the user
                return

        if not var_task_entity_title:
            print("Error: Entry cannot be empty.")
            return
        
        try:
            new_task = TaskEntity(title=var_task_entity_title,
                                  priority=var_task_entity_priority,
                                  is_active=True,
                                  completion_date=var_complete_datetime,
                                  created_at=datetime.datetime.now(),
                                  created_by=var_task_user_id)
            
            query_task = self.tasks_service.add_task(new_task)
            
            # Limpiar Entry despues de agregar
            self.task_title_entry.delete("1.0", "end")
            
            print(f"Task added: {query_task}")
            
            # Recargar para mostrar las tareas recien agregadas
            self._load_tasks()
            
        except Exception as e:
            print(f"Error adding task: {e}")

            
    def _load_tasks(self):
        
        self._loaded_tasks = self.tasks_service.get_tasks()
        
        if self._loaded_tasks:
            print(f"Se encontraron los siguientes datos: {self._loaded_tasks}")
            self._display_tasks()
        else:
            print("No se encontraron datos.")
        
    def _display_tasks(self):
        # Clear existing task widgets from the inner_task_frame
        for widget in self.general_task_frame.winfo_children():
            widget.destroy()

        if not self._loaded_tasks:
            ttk.Label(self.general_task_frame, text="No tasks found.", style="TaskTitle.TLabel").pack(pady=5)
            # Update scrollable region after adding content
            self.general_task_frame.update_idletasks()
            self.task_canvas.config(scrollregion=self.task_canvas.bbox("all"))
            return
        
        self._loaded_tasks.reverse()

        # This loop will create a frame for each register/task
        # Reversed for displaying from the bottom to top
        for i, task in enumerate(self._loaded_tasks):
            
            # Create a frame for each task to group its title and details
            task_item_frame = tk.Frame(  # <-- CHANGED THIS LINE!
                self.general_task_frame,
                background="lightgray",  # Make the background of THIS box light gray
                borderwidth=1,           # Give THIS box a border 1 pixel thick
                relief="solid"           # Make the border of THIS box a clear, solid line
            )

            task_item_frame.pack(fill="x", pady=2, padx=5, side="top", ipadx=5, ipady=5)

            ttk.Label(task_item_frame,
                      text=f"{task.title}",
                      style="TaskTitle.TLabel",
                      anchor="w",
                      background="lightgray") \
                .pack(fill="x")

            details_text = \
                (f"Creado el: {task.formatted_created_at} "
                 f"| Prioridad: {task.priority} "
                 f"| Terminar antes de: {task.formatted_completion_date if task.completion_date else 'N/A'} "
                 f"| Estado: {'Pendiente' if task.is_active else 'Completado'}"
                 f"| Creado por: {task.created_by}")
            ttk.Label(task_item_frame,
                      text=details_text,
                      style="TaskDetail.TLabel",
                      anchor="w",
                      background="lightgray") \
                .pack(fill="x")

            # Add a separator if it's not the last task
            if i < len(self._loaded_tasks) - 1:
                ttk.Separator(self.general_task_frame, orient="horizontal").pack(fill="x", pady=5)

        # IMPORTANT: Update the scrollable region of the canvas after adding all items
        self.general_task_frame.update_idletasks() # Ensure widgets are rendered to get correct size
        self.task_canvas.config(scrollregion=self.task_canvas.bbox("all"))

    # --- Canvas & Scrollbar Helper Methods ---
    def _on_canvas_configure(self, event):
        # Update the width of the inner frame to match the canvas's width
        # This makes sure the content frame fills the canvas horizontally
        self.task_canvas.itemconfig(self.task_canvas.create_window((0, 0), window=self.general_task_frame, anchor="nw"),
                                    width=event.width)
        # Also update the scroll region
        self.general_task_frame.update_idletasks()
        self.task_canvas.config(scrollregion=self.task_canvas.bbox("all"))

    def _on_mousewheel(self, event):
        # For Windows, use event.delta. For MacOS/Linux, event.num
        if self.master.tk.call("tk", "windowingsystem") == "aqua": # MacOS
            self.task_canvas.yview_scroll(-1 * event.delta, "units")
        elif self.master.tk.call("tk", "windowingsystem") == "x11": # Linux
            self.task_canvas.yview_scroll(-1 * event.delta, "units")
        else: # Windows
            self.task_canvas.yview_scroll(-1 * (event.delta // 120), "units")