
from services.tasks_service import TasksService
from views.base_view import BaseView
import tkinter as tk
from tkinter import ttk

from models.tasks_entity import TaskEntity

class TaskManagementView(BaseView):
    def __init__(self, master, show_view_callback, current_username, tasks_service: TasksService):
        super().__init__(master, show_view_callback, current_username)
        self.config(bg="#e0ffe0")
        
        self.tasks_service = tasks_service
        self.task_title_entry = None
        
        self._loaded_tasks = []
        
        self._create_widgets()

    def _create_widgets(self):
        ttk.Label(self,
                  text="Administrar tareas",
                  style="main_title.TLabel"
                  ).pack(pady=50)

        ttk.Button(self,
                   text="Volver",
                   style="main_button.TButton",
                   command=lambda: self.navigate_to("main")
                   ).pack(pady=10)

        ttk.Button(self, 
                   text="Ajustes",
                   style="secondary_button.TButton",
                   command=lambda: self.navigate_to("options")
                   ).pack(pady=10)
        
        # ------------------------------- Data loading and display -------------------------------
        # Create a frame to hold the scrollable list of tasks
        self.task_list_frame = ttk.Frame(self)
        self.task_list_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Create a Canvas for the scrollable region
        self.task_canvas = tk.Canvas(self.task_list_frame, bg="#e0ffe0", bd=0, highlightthickness=0)
        self.task_canvas.pack(side="left", fill="both", expand=True)

        # Add a scrollbar to the canvas
        self.task_scrollbar = ttk.Scrollbar(self.task_list_frame, orient="vertical", command=self.task_canvas.yview)
        self.task_scrollbar.pack(side="right", fill="y")
        self.task_canvas.configure(yscrollcommand=self.task_scrollbar.set)

        # Create another frame INSIDE the canvas to hold the task items
        # This is where the actual task labels will go
        self.inner_task_frame = ttk.Frame(self.task_canvas, style="TFrame") # You might want to define a style for this frame
        self.task_canvas.create_window((0, 0), window=self.inner_task_frame, anchor="nw", width=self.task_canvas.winfo_width())

        # Bind the configure event of the canvas to update the inner frame's width
        self.task_canvas.bind("<Configure>", self._on_canvas_configure)
        # Bind the scroll wheel for scrolling (for non-Windows OS, can be added with more binds)
        self.task_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # ------------------------------- ------------------------------- -------------------------------

        self._load_tasks()

        # Registra la entrada en la variable
        self.task_title_entry = ttk.Entry(self,
                                          style="main_entry.TEntry")
        self.task_title_entry.pack(pady=10)
        
        ttk.Button(self, text="Agregar",
                   style="submit_button.TButton",
                   command=self._add_new_task
                   ).pack(pady=10)
        
    
    def _add_new_task(self):
        var_taskEntity = self.task_title_entry.get().strip() 
            # get obtiene el texto de task_title_entry
                # strip elimina los espacios en blanco al inicio y al final
        
        if not var_taskEntity:
            print("Error: Entry cannot be empty.")
            return
        
        try:
            new_task = TaskEntity(title=var_taskEntity, priority="Normal", is_active=True)
            
            query_task = self.tasks_service.add_task(new_task)
            print(f"Task added: {query_task}")
            
            # Limpiar Entry despues de agregar
            self.task_title_entry.delete(0, tk.END)
            
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
        
        # print(self._loaded_tasks)
        # 
        # for x in self.tasks_service.get_tasks():
        #     print(x)

    def _display_tasks(self):
        # Clear existing task widgets from the inner_task_frame
        for widget in self.inner_task_frame.winfo_children():
            widget.destroy()

        if not self._loaded_tasks:
            ttk.Label(self.inner_task_frame, text="No tasks found.", style="TaskTitle.TLabel").pack(pady=5)
            # Update scrollable region after adding content
            self.inner_task_frame.update_idletasks()
            self.task_canvas.config(scrollregion=self.task_canvas.bbox("all"))
            return

        for i, task in enumerate(self._loaded_tasks):
            # Create a frame for each task to group its title and details
            task_item_frame = ttk.Frame(self.inner_task_frame, style="TaskTitle.TLabel") # Use a style for the frame
            task_item_frame.pack(fill="x", pady=2, padx=5) # Pack each task item

            # Display title
            ttk.Label(task_item_frame, text=f"{i+1}. {task.title}", style="TaskTitle.TLabel", anchor="w") \
                .pack(fill="x")

            # Display details (priority, completion date, active status)
            details_text = f"Priority: {task.priority} | Due: {task.completion_date if task.completion_date else 'N/A'} | Active: {'Yes' if task.is_active else 'No'}"
            ttk.Label(task_item_frame, text=details_text, style="TaskDetail.TLabel", anchor="w") \
                .pack(fill="x")

            # Add a separator if it's not the last task
            if i < len(self._loaded_tasks) - 1:
                ttk.Separator(self.inner_task_frame, orient="horizontal").pack(fill="x", pady=5)

        # IMPORTANT: Update the scrollable region of the canvas after adding all items
        self.inner_task_frame.update_idletasks() # Ensure widgets are rendered to get correct size
        self.task_canvas.config(scrollregion=self.task_canvas.bbox("all"))

    # --- Canvas & Scrollbar Helper Methods ---
    def _on_canvas_configure(self, event):
        # Update the width of the inner frame to match the canvas's width
        # This makes sure the content frame fills the canvas horizontally
        self.task_canvas.itemconfig(self.task_canvas.create_window((0, 0), window=self.inner_task_frame, anchor="nw"),
                                    width=event.width)
        # Also update the scroll region
        self.inner_task_frame.update_idletasks()
        self.task_canvas.config(scrollregion=self.task_canvas.bbox("all"))

    def _on_mousewheel(self, event):
        # For Windows, use event.delta. For MacOS/Linux, event.num
        if self.master.tk.call("tk", "windowingsystem") == "aqua": # MacOS
            self.task_canvas.yview_scroll(-1 * event.delta, "units")
        elif self.master.tk.call("tk", "windowingsystem") == "x11": # Linux
            self.task_canvas.yview_scroll(-1 * event.delta, "units")
        else: # Windows
            self.task_canvas.yview_scroll(-1 * (event.delta // 120), "units")