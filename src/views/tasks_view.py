import datetime
from tkcalendar import DateEntry
from src.services.tasks_service import TasksService
from src.views.base_view import BaseView
import tkinter as tk
from tkinter import ttk

from src.models.tasks_entity import TaskEntity

class TaskManagementView(BaseView):
    def __init__(self, master, show_view_callback, tasks_service: TasksService):
        super().__init__(master, show_view_callback)
        self.config(bg="#e0ffe0")

        self.tasks_service = tasks_service

        # Variables for entries
        self.task_title_entry = None
        self.task_priority_entry = tk.StringVar(self) # Variable for storing radiogroup value

        # Variables for calendar
        self.task_completion_date_var = tk.StringVar(self)
        self.task_completion_date_hour_var = tk.StringVar(self, value="00")
        self.task_completion_date_minute_var = tk.StringVar(self, value="00")

        # Store canvas window IDs for both canvases
        self.pending_canvas_frame_id = None
        self.completed_canvas_frame_id = None

        self._loaded_tasks_pending = []
        self._loaded_tasks_completed = []

        self._create_widgets()
        self._build_ui()

        # Delayed loading of all tasks to ensure UI is rendered.
        self.after(100, self._load_all_tasks_on_startup)

    def _load_all_tasks_on_startup(self):
        self._load_all_tasks()

    def _create_widgets(self):

        # ------------------------------- FRAMES and CANVAS -------------------------------
        # Main fraime, central frame
        self.main_frame = tk.Frame(self, bg="#e0ffe0")

        # ----------------------------------- LEFT SIDE (PENDING TASKS) -------------------------------
        # Left frame: To be completed TASKS
        self.left_frame = tk.Frame(self, bg="#e0ffe0")

        # Introduce a new frame for the very top row of the left_frame
        self.left_top_center_frame = tk.Frame(self.left_frame, bg="#e0ffe0")
        self.left_top_left_frame = tk.Frame(self.left_top_center_frame, bg="#e0ffe0")


        # Frame: task_list_frame (Container for pending tasks canvas and scrollbar)
        self.task_list_frame = ttk.Frame(self.left_frame)

        # Canvas: task_pending_canvas
        self.task_pending_canvas = tk.Canvas(self.task_list_frame, bg="#e0ffe0", bd=0, highlightthickness=0)

        # Bindings for pending canvas - using generalized _on_canvas_configure
        self.task_pending_canvas.bind("<Configure>", lambda event: self._on_canvas_configure(event, self.task_pending_canvas, self.general_pending_task_frame, self.pending_canvas_frame_id))
        self.task_pending_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Frame: general_pending_task_frame (Inner frame inside pending canvas)
        self.general_pending_task_frame = ttk.Frame(self.task_pending_canvas, style="TFrame")

        # Store the window ID for the pending canvas
        self.pending_canvas_frame_id = self.task_pending_canvas.create_window((0, 0), window=self.general_pending_task_frame, anchor="nw", width=self.task_pending_canvas.winfo_width())
        # Bind the inner frame to generalized _on_frame_configure
        self.general_pending_task_frame.bind("<Configure>", lambda event: self._on_frame_configure(event, self.task_pending_canvas, self.general_pending_task_frame, self.pending_canvas_frame_id))


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
                                                      textvariable=self.task_completion_date_hour_var,
                                                      width=3,
                                                      format="%02.0f")

        # Minute Spinbox: task_completion_minute_entry
        self.task_completion_minute_entry = ttk.Spinbox(self.date_time_frame,
                                                        from_=0, to=59,
                                                        wrap=True,
                                                        textvariable=self.task_completion_date_minute_var,
                                                        width=3,
                                                        format="%02.0f")

        # ------------------------------- LABELS -------------------------------
        # Label: "Administrar tareas"
        self.admin_tasks_label = ttk.Label(self.main_frame,
                                           text="Administrar tareas",
                                           style="main_title.TLabel")

        # Label: "Describe tu tarea:"
        self.task_description_label = ttk.Label(self.data_input_frame_left, text="Describe tu tarea:", style="secondary_label.TLabel")


        # Label: "Fecha límite:"
        self.due_date_label = ttk.Label(self.data_input_frame_right, text="Fecha límite:", style="secondary_label.TLabel")

        # Label: Separator for time
        self.time_separator_label = ttk.Label(self.date_time_frame, text=":", style="secondary_label.TLabel")

        # Label: "Prioridad:"
        self.priority_label = ttk.Label(self.priority_frame, text="Prioridad:", style="secondary_label.TLabel")
        # ------------------------------- BUTTONS -------------------------------


        # Button: "Volver"
        self.back_button = ttk.Button(self.left_top_left_frame,
                                      text="Volver",
                                      style="main_button.TButton",
                                      command=lambda: self.navigate_to("main"))

        # Button: "Volver"
        self.add_button = ttk.Button(self.priority_frame, text="Agregar",
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


        # ------------------------------- SCROLLBAR (PENDING) -------------------------------
        self.task_pending_scrollbar = ttk.Scrollbar(self.task_list_frame,
                                                    orient="vertical",
                                                    command=self.task_pending_canvas.yview)


        # ----------------------------------- RIGHT SIDE (COMPLETED TASKS) -------------------------------
        # Right frame: Completed TASKS
        self.right_frame = tk.Frame(self, bg="#e0ffe0")

        # Button: "Ajustes"
        self.settings_button = ttk.Button(self.right_frame,
                                          text="Ajustes",
                                          style="secondary_button.TButton",
                                          command=lambda: self.navigate_to("options"))

        # Frame para los tasks completados (Container for completed tasks canvas and scrollbar)
        self.task_completed_list_frame = ttk.Frame(self.right_frame)

        # Canvas: task_completed_canvas
        self.task_completed_canvas = tk.Canvas(self.task_completed_list_frame, bg="#e0ffe0", bd=0, highlightthickness=0)

        # Bindings for completed canvas - using generalized _on_canvas_configure
        self.task_completed_canvas.bind("<Configure>", lambda event: self._on_canvas_configure(event, self.task_completed_canvas, self.general_completed_task_frame, self.completed_canvas_frame_id))
        self.task_completed_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Frame: general_completed_task_frame (Inner frame inside completed canvas)
        self.general_completed_task_frame = ttk.Frame(self.task_completed_canvas, style="TFrame")

        # IMPORTANT: Use task_completed_canvas.winfo_width() for width here!
        self.completed_canvas_frame_id = self.task_completed_canvas.create_window((0,0), window=self.general_completed_task_frame, anchor="nw", width=self.task_completed_canvas.winfo_width())

        # Bind the inner frame to generalized _on_frame_configure (NOT _on_canvas_configure)
        self.general_completed_task_frame.bind("<Configure>", lambda event: self._on_frame_configure(event, self.task_completed_canvas, self.general_completed_task_frame, self.completed_canvas_frame_id))

        # Removed initial _load_all_tasks() call here (handled by self.after in __init__)

        # ------------------------------- SCROLLBAR (COMPLETED) -------------------------------
        self.task_completed_scrollbar = ttk.Scrollbar(self.task_completed_list_frame,
                                                      orient="vertical",
                                                      command=self.task_completed_canvas.yview)

    def _build_ui(self):
        # ------------------------------- ------ -------------------------------
        # ------------------------------- Layout -------------------------------
        # ------------------------------- ------ -------------------------------
        # Packing frames
        self.main_frame.pack(fill="both")
        self.right_frame.pack(side="right", fill="both", padx=10)
        self.left_frame.pack(side="left", fill="both", padx=10)
        self.left_top_center_frame.pack(side="top", fill="x", pady=5)
        self.left_top_left_frame.pack(side="left", fill="x", pady=5)

        # ------------------------------- CENTERED UI -------------------------------

        self.admin_tasks_label.pack(side="bottom", pady=(20,0))

        # ------------------------------- RIGHT FRAME -------------------------------

        self.settings_button.pack(pady=10)
        # Pack the completed tasks list frame, canvas, and scrollbar
        self.task_completed_list_frame.pack(pady=10, padx=5, fill="both", expand=True)
        self.task_completed_canvas.pack(side="left", fill="both", expand=True) # Changed fill to both
        self.task_completed_scrollbar.pack(side="right", fill="y")
        self.task_completed_canvas.configure(yscrollcommand=self.task_completed_scrollbar.set)

        # ------------------------------- LEFT FRAME -------------------------------

        self.back_button.pack(pady=5)

        # ------------------------------- Data loading and display -------------------------------

        self.task_list_frame.pack(pady=10, padx=5, fill="both", expand=True) # Changed fill to both

        # Canvas: task_pending_canvas
        self.task_pending_canvas.pack(side="left", fill="both", expand=True) # Changed fill to both

        # Scrollbar: task_pending_scrollbar
        self.task_pending_scrollbar.pack(side="right", fill="y")
        self.task_pending_canvas.configure(yscrollcommand=self.task_pending_scrollbar.set)

        # Packing data input frames
        self.data_input_frame_left.pack(side="left", pady=10, padx=10)
        self.data_input_frame_right.pack(side="right", pady=10, padx=10)

        self.task_description_label.pack(pady=(10, 0))

        self.task_title_entry.pack(pady=10, fill="x", expand=True)

        # --- START TIME PICKER ---

        self.due_date_label.pack(pady=(10, 0))

        self.date_time_frame.pack(side="top", pady=5)

        self.task_completion_date_entry.pack(side="left", padx=5)

        self.task_completion_hour_entry.pack(side="left")

        self.time_separator_label.pack(side="left")

        self.task_completion_minute_entry.pack(side="left")


        # --- END TIME PICKER ---

        # --- START RADIO BUTTONS ---

        # Frame: priority_frame (to hold radio buttons)
        self.priority_frame.pack(side="bottom", pady=5)

        self.priority_label.pack(side="top", pady=5)

        self.task_priority_entry.set("Normal") # Default selection

        self.priority_button_urgente.pack(side="left", padx=10)

        self.priority_button_importante.pack(side="left", padx=10)

        self.priority_button_normal.pack(side="left", padx=10)

        # --- END RADIO BUTTONS ---
        self.add_button.pack(side="bottom",padx=5)

        # Removed _load_all_tasks() call here (handled by self.after in __init__)

    def _add_new_task(self):

        var_task_entity_title = self.task_title_entry.get("1.0", "end-1c").strip()
        var_task_entity_priority = self.task_priority_entry.get()
        var_task_entity_completion_date = self.task_completion_date_entry.get_date()

        var_completion_hour_str = self.task_completion_date_hour_var.get()
        var_completion_minute_str = self.task_completion_date_minute_var.get()

        var_complete_datetime = None

        if var_task_entity_completion_date:
            try:
                selected_hour = int(var_completion_hour_str)
                selected_minute = int(var_completion_minute_str)
                var_complete_datetime = datetime.datetime.combine(
                    var_task_entity_completion_date,
                    datetime.time(selected_hour, selected_minute))
            except ValueError:
                print("Internal error.")
                return

        if not var_task_entity_title:
            print("Error: Entry cannot be empty.")
            return

        try:
            new_task = TaskEntity(title=var_task_entity_title,
                                  priority=var_task_entity_priority,
                                  is_active=True, # New tasks are active
                                  completion_date=var_complete_datetime,
                                  created_at=datetime.datetime.now())

            query_task = self.tasks_service.add_task(new_task)

            self.task_title_entry.delete("1.0", "end")

            print(f"Task added: {query_task}")

            # Recargar para mostrar las tareas recien agregadas
            self._load_all_tasks() # Call the unified loader

        except Exception as e:
            print(f"Error adding task: {e}")

    def _load_all_tasks(self):
        print("DEBUG: Loading all tasks...")

        self._load_completed_tasks()
        self._load_pending_tasks()

    def _load_completed_tasks(self):
        self._loaded_tasks_completed = self.tasks_service.get_completed_tasks()

        if self._loaded_tasks_completed:
            print(f"COMPLETED: Se encontraron los siguientes datos: {self._loaded_tasks_completed}")
        else:
            print("COMPLETED: No se encontraron datos.")
        # Always call display to ensure UI is cleared or updated correctly
        self._display_completed_tasks()

    def _load_pending_tasks(self):
        self._loaded_tasks_pending = self.tasks_service.get_pending_tasks()

        if self._loaded_tasks_pending:
            print(f"PENDING: Se encontraron los siguientes datos: {self._loaded_tasks_pending}")
        else:
            print("PENDING: No se encontraron datos.")
        # Always call display to ensure UI is cleared or updated correctly
        self._display_pending_tasks()

    def _display_pending_tasks(self):
        # Clear existing task widgets from the inner_task_frame
        for widget in self.general_pending_task_frame.winfo_children():
            widget.destroy()

        if not self._loaded_tasks_pending:
            ttk.Label(self.general_pending_task_frame, text="No tasks found.", style="TaskTitle.TLabel").pack(pady=5)
            # Use correct frame for update_idletasks
            self.general_pending_task_frame.update_idletasks()
            # Use generalized scroll region update
            self._update_scroll_region(self.task_pending_canvas, self.general_pending_task_frame, self.pending_canvas_frame_id)
            return

        self._loaded_tasks_pending.reverse()

        for i, task in enumerate(self._loaded_tasks_pending):

            task_item_frame = tk.Frame(
                self.general_pending_task_frame,
                background="lightgray",
                borderwidth=1,
                relief="solid"
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
                 f"| Estado: {'Pendiente' if task.is_active else 'Completado'}")
            ttk.Label(task_item_frame,
                      text=details_text,
                      style="TaskDetail.TLabel",
                      anchor="w",
                      background="lightgray") \
                .pack(fill="x")

            if i < len(self._loaded_tasks_pending) - 1:
                ttk.Separator(self.general_pending_task_frame, orient="horizontal").pack(fill="x", pady=5)

        self.general_pending_task_frame.update_idletasks()
        self._update_scroll_region(self.task_pending_canvas, self.general_pending_task_frame, self.pending_canvas_frame_id)

    def _display_completed_tasks(self):
        # Clear existing task widgets from the inner_task_frame
        for widget in self.general_completed_task_frame.winfo_children(): # Correct parent for clearing
            widget.destroy()

        if not self._loaded_tasks_completed:
            # Pack "No tasks found" into the inner frame, not the list frame
            ttk.Label(self.general_completed_task_frame, text="No tasks found.", style="TaskTitle.TLabel").pack(pady=5)
            # Use correct frame for update_idletasks
            self.general_completed_task_frame.update_idletasks()
            # Use generalized scroll region update
            self._update_scroll_region(self.task_completed_canvas, self.general_completed_task_frame, self.completed_canvas_frame_id)
            return

        self._loaded_tasks_completed.reverse()

        for i, task in enumerate(self._loaded_tasks_completed):

            task_item_frame = tk.Frame(
                self.general_completed_task_frame, # Correct parent
                background="lightgray",
                borderwidth=1,
                relief="solid"
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
                 f"| Estado: {'Pendiente' if task.is_active else 'Completado'}")
            ttk.Label(task_item_frame,
                      text=details_text,
                      style="TaskDetail.TLabel",
                      anchor="w",
                      background="lightgray") \
                .pack(fill="x")

            if i < len(self._loaded_tasks_completed) - 1:
                ttk.Separator(self.general_completed_task_frame, orient="horizontal").pack(fill="x", pady=5)

        self.general_completed_task_frame.update_idletasks()
        self._update_scroll_region(self.task_completed_canvas, self.general_completed_task_frame, self.completed_canvas_frame_id)

    # --- Canvas & Scrollbar Helper Methods ---
    # Generalized _on_canvas_configure to accept canvas, inner_frame, and frame_id
    def _on_canvas_configure(self, event, canvas_obj, inner_frame, frame_id):
        """Called when a canvas changes size."""
        if frame_id is not None:
            canvas_obj.itemconfig(frame_id, width=event.width)
        self._update_scroll_region(canvas_obj, inner_frame, frame_id)

    # Generalized _on_frame_configure to accept canvas, inner_frame, and frame_id
    def _on_frame_configure(self, event, canvas_obj, inner_frame, frame_id):
        """Called when an inner frame (inside a canvas) changes size."""
        self._update_scroll_region(canvas_obj, inner_frame, frame_id)

    # Generalized _update_scroll_region to accept canvas, inner_frame, and frame_id
    def _update_scroll_region(self, canvas_obj, inner_frame, frame_id):
        """Updates the scroll region of the given canvas based on its inner frame's bounding box."""
        if frame_id is not None:
            inner_frame.update_idletasks() # Ensure inner frame widgets are rendered
            bbox = canvas_obj.bbox(frame_id)
            if bbox is not None:
                canvas_obj.config(scrollregion=bbox)

    def _on_mousewheel(self, event):
        # Determine which canvas has focus or is under the mouse
        widget = event.widget
        while widget and not isinstance(widget, tk.Canvas):
            widget = widget.master

        if widget and isinstance(widget, tk.Canvas):
            if self.master.tk.call("tk", "windowingsystem") == "aqua": # MacOS
                widget.yview_scroll(-1 * event.delta, "units")
            elif self.master.tk.call("tk", "windowingsystem") == "x11": # Linux
                widget.yview_scroll(-1 * event.delta, "units")
            else: # Windows
                widget.yview_scroll(-1 * (event.delta // 120), "units")