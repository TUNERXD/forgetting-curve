from CTkMessagebox import CTkMessagebox
import customtkinter
import datetime

from data import TaskManager, Task, StudyTask, WorkTask

# main app
class App(customtkinter.CTk):
    
    def __init__(self):
        super().__init__()
        self.title("Forgetting Curve Study/Task Scheduler")
        self.geometry("1100x700")
        customtkinter.set_appearance_mode("System")
        
        # initialize task manager
        self.task_manager = TaskManager.load_tasks()
        self.add_toplevel_window = None
        self.edit_toplevel_window = None
        self.selected_task = None

        # 30% control 70% Tasks
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=7)
        self.grid_rowconfigure(0, weight=1)

        # ========== Left Frame: Menu ========== #
        self.controls_frame = customtkinter.CTkFrame(self)
        self.controls_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.controls_frame.grid_columnconfigure(0, weight=1)
        self.controls_frame.grid_rowconfigure(3, weight=1)

        # Title of left frame
        self.label = customtkinter.CTkLabel(self.controls_frame, text="Menu", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label.grid(row=0, column=0, padx=10, pady=10)

        # Add task Button
        self.add_task_button = customtkinter.CTkButton(self.controls_frame, text="Add New Task", command=self.open_add)
        self.add_task_button.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

        self.refresh_button = customtkinter.CTkButton(self.controls_frame, text="Refresh", command=self.refresh_task)
        self.refresh_button.grid(row=2, column=0, padx=20, pady=0, sticky="ew")


        # ---------- Task Details ---------- #
        self.details_frame = customtkinter.CTkFrame(self.controls_frame, fg_color="gray20")
        self.details_frame.grid(row=3, column=0, padx=20, pady=20, sticky="nsew")
        self.details_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        self.details_label = customtkinter.CTkLabel(self.details_frame, text="Task Details", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.details_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Name of Selected task
        self.details_name_label = customtkinter.CTkLabel(self.details_frame, text="Select a task to see details.", justify="left", wraplength=250)
        self.details_name_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Name of Selected task
        self.details_common_label = customtkinter.CTkLabel(self.details_frame, text="", justify="left")
        self.details_common_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        
        # Name, Due date of Selected task
        self.details_specific_label = customtkinter.CTkLabel(self.details_frame, text="", justify="left")
        self.details_specific_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")


        # ---------- detail buttons frame ---------- #
        self.review_button_frame = customtkinter.CTkFrame(self.details_frame, fg_color="transparent")
        self.review_button_frame.grid(row=4, column=0, padx=10, pady=2, sticky="ew")
        self.review_button_frame.grid_columnconfigure(0, weight=1)

        # Review button for StudyTask    
        self.review_button = customtkinter.CTkButton(self.review_button_frame, text="Mark as Reviewed", command=self.review_selected_task)

        # Common Buttons, Add/Edit
        self.details_button_frame = customtkinter.CTkFrame(self.details_frame, fg_color="transparent")
        self.details_button_frame.grid(row=5, column=0, padx=10, pady=2, sticky="ew")
        self.details_button_frame.grid_columnconfigure(0, weight=1)
        self.details_button_frame.grid_columnconfigure(1, weight=1)

        self.edit_button = customtkinter.CTkButton(self.details_button_frame, text="Edit Task", command=self.open_edit)
        self.delete_button = customtkinter.CTkButton(self.details_button_frame, text="Delete Task", fg_color="gray30", hover_color="gray40", command=self.delete_selected_task)


        # ========== Right Frame: Task List ========== #

        # ---------- Create Tabs ---------- #
        self.tab_view = customtkinter.CTkTabview(self)
        self.tab_view.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # add each tab to tab_view
        self.tab_all = self.tab_view.add("All Tasks")
        self.tab_study = self.tab_view.add("Study")
        self.tab_work = self.tab_view.add("Work")
        
        # ---------- All Tasks Tab Scrollable Frame ---------- #
        self.tab_all.grid_columnconfigure(0, weight=1)
        self.tab_all.grid_rowconfigure(0, weight=1)
        self.all_tasks_scrollable_frame = customtkinter.CTkScrollableFrame(self.tab_all)
        self.all_tasks_scrollable_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.all_tasks_scrollable_frame.grid_columnconfigure(0, weight=1)
        
        # ---------- StudyTask Tab Scrollable Frame ---------- #
        self.tab_study.grid_columnconfigure(0, weight=1)
        self.tab_study.grid_rowconfigure(0, weight=1)
        self.study_tasks_scrollable_frame = customtkinter.CTkScrollableFrame(self.tab_study)
        self.study_tasks_scrollable_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.study_tasks_scrollable_frame.grid_columnconfigure(0, weight=1)
        
        # ---------- WorkTask Tab Scrollable Frame ---------- #
        self.tab_work.grid_columnconfigure(0, weight=1)
        self.tab_work.grid_rowconfigure(0, weight=1)
        self.work_tasks_scrollable_frame = customtkinter.CTkScrollableFrame(self.tab_work)
        self.work_tasks_scrollable_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.work_tasks_scrollable_frame.grid_columnconfigure(0, weight=1)

        # Initial Refresh
        self.refresh_task()
        self.update_details_panel()

    def open_add(self):
        '''
        Method to open Add task window
        '''
        
        if self.add_toplevel_window is None or not self.add_toplevel_window.winfo_exists():
            self.add_toplevel_window = TaskAddToplevel(self, task_manager=self.task_manager, sr = self.save_refresh)
        else:
            self.add_toplevel_window.focus()
            
    def open_edit(self):
        '''
        Method to open Edit task window
        '''
        
        if not self.selected_task:
            return
            
        if self.edit_toplevel_window is None or not self.edit_toplevel_window.winfo_exists():
            self.edit_toplevel_window = TaskEditToplevel(self, task=self.selected_task, sr=self.save_refresh)
        else:
            self.edit_toplevel_window.focus()
            
    def create_task(self, master_frame, task: Task) -> customtkinter.CTkFrame:
        '''
        Function to Create Task Card
        '''
        # Create a an empty frame
        task_frame = customtkinter.CTkFrame(master_frame, fg_color="gray20")
        task_frame.columnconfigure(0, weight=1)

        # get the task details
        task_details = task.get_details()
        

        # Normal Task color
        type_color = "#59ff72"

        # WorkTask Color
        if isinstance(task, WorkTask):
            type_color = "#1976D2"
        
        # Task Due color
        if task.is_due():
            type_color = "#FBC02D"
            
            # Color Based on WorkTask Priority
            if isinstance(task, WorkTask):
                if task.priority == 2:
                    type_color = "#eb0000"
                elif task.priority == 1:
                    type_color = "#fc8f00"
                    

        header_frame = customtkinter.CTkFrame(task_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=10, pady=(5,0), sticky="ew")
        header_frame.columnconfigure(0, weight=1)
        
        type_label = customtkinter.CTkLabel(header_frame, text=f" {task.get_task_type().upper()} ", fg_color=type_color, corner_radius=5, font=customtkinter.CTkFont(size=12, weight="bold"))
        type_label.grid(row=0, column=0, sticky="w")
        
        details_label = customtkinter.CTkLabel(header_frame, text=task_details, text_color="gray70", justify="right")
        details_label.grid(row=0, column=1, sticky="e", padx=10)

        name_label = customtkinter.CTkLabel(task_frame, text=task.name, font=customtkinter.CTkFont(size=16, weight="bold"), justify="left")
        name_label.grid(row=1, column=0, padx=10, pady=(0, 5), sticky="w")

        if isinstance(task, StudyTask):
            retention_percent = task.get_retention_percent()
            progress_bar = customtkinter.CTkProgressBar(task_frame, height=10)
            progress_bar.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")
            progress_bar.set(retention_percent)
            
            retention_label = customtkinter.CTkLabel(header_frame, text=f"{retention_percent*100:.0f}%", text_color="gray70", justify="right")
            retention_label.grid(row=0, column=2, sticky="e", padx=10)

        
        click_handler = lambda event, t=task: self.select_task(t)
        task_frame.bind("<Button-1>", click_handler)
        header_frame.bind("<Button-1>", click_handler)
        type_label.bind("<Button-1>", click_handler)
        details_label.bind("<Button-1>", click_handler)
        name_label.bind("<Button-1>", click_handler)

        if isinstance(task, StudyTask):
            progress_bar.bind("<Button-1>", click_handler)
            retention_label.bind("<Button-1>", click_handler)
            
        return task_frame

            
    def refresh_task(self):
        
        # destroy all widgets in every tabs
        for widget in self.all_tasks_scrollable_frame.winfo_children():
            widget.destroy()
        for widget in self.study_tasks_scrollable_frame.winfo_children():
            widget.destroy()
        for widget in self.work_tasks_scrollable_frame.winfo_children():
            widget.destroy()

        # Get all tasks
        tasks = self.task_manager.get_tasks()
        
        # if tasks = []
        if not tasks:
            label_all = customtkinter.CTkLabel(self.all_tasks_scrollable_frame, text="No tasks added yet.")
            label_all.pack(pady=10)
            label_study = customtkinter.CTkLabel(self.study_tasks_scrollable_frame, text="No Study tasks added yet.")
            label_study.pack(pady=10)
            label_work = customtkinter.CTkLabel(self.work_tasks_scrollable_frame, text="No Work tasks added yet.")
            label_work.pack(pady=10)
            
        
        study_count = 0
        work_count = 0

        for task in tasks:

            if isinstance(task, StudyTask):

                # decrease 1 level if retention lower than 45%
                if task.get_retention_percent() < 0.45:
                    task.level_decrement()

                study_task_frame = self.create_task(self.study_tasks_scrollable_frame, task)
                study_task_frame.pack(fill="x", padx=5, pady=5)
                study_count += 1

            if isinstance(task, WorkTask):
                work_task_frame = self.create_task(self.work_tasks_scrollable_frame, task)
                work_task_frame.pack(fill="x", padx=5, pady=5)
                work_count += 1
            
            all_task_frame = self.create_task(self.all_tasks_scrollable_frame, task)
            all_task_frame.pack(fill="x", padx=5, pady=5)
                
        
        if study_count == 0 and tasks:
            label_study = customtkinter.CTkLabel(self.study_tasks_scrollable_frame, text="No Study tasks added yet.")
            label_study.pack(pady=10)
        
        if work_count == 0 and tasks:
            label_work = customtkinter.CTkLabel(self.work_tasks_scrollable_frame, text="No Work tasks added yet.")
            label_work.pack(pady=10)

        if self.selected_task and self.selected_task not in self.task_manager.get_tasks():
            self.selected_task = None
        
        self.update_details_panel()

    def save_refresh(self):
        
        self.task_manager.save_tasks()
        self.refresh_task()

    def select_task(self, task: Task):
        
        self.selected_task = task
        self.update_details_panel()

    def update_details_panel(self):
        
        self.review_button.grid_forget()
        self.edit_button.grid_forget()
        self.delete_button.grid_forget()
        
        if self.selected_task:
            self.details_name_label.configure(text=self.selected_task.name, font=customtkinter.CTkFont(size=18, weight="bold"))
            self.details_common_label.configure(text=self.selected_task.get_common_display())
            
            self.details_specific_label.configure(text=self.selected_task.get_details())
            
            if isinstance(self.selected_task, StudyTask):
                self.review_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

                if self.selected_task.is_due():
                    self.review_button.configure(fg_color="#FBC02D", hover_color="#F9A825", text_color="black")
                else:
                    self.review_button.configure(fg_color=customtkinter.ThemeManager.theme["CTkButton"]["fg_color"],
                                                 hover_color=customtkinter.ThemeManager.theme["CTkButton"]["hover_color"],
                                                 text_color=customtkinter.ThemeManager.theme["CTkButton"]["text_color"])
            
            self.edit_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
            self.delete_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
            self.details_button_frame.grid_columnconfigure(1, weight=1)
            
            
        else:
            self.details_name_label.configure(text="Select a task to see details.", font=customtkinter.CTkFont(size=14, weight="normal"))
            self.details_common_label.configure(text="")
            self.details_specific_label.configure(text="")
            
    def review_selected_task(self):
        
        if self.selected_task and isinstance(self.selected_task, StudyTask):
            self.selected_task.level_increment()
            self.save_refresh()

    def delete_selected_task(self):
        
        if self.selected_task:
            task_to_delete = self.selected_task
            self.selected_task = None
            self.task_manager.delete_task(task_to_delete)
            self.save_refresh()

# adding task window
class TaskAddToplevel(customtkinter.CTkToplevel):
    
    def __init__(self, master, task_manager: TaskManager, sr):
        super().__init__(master)
        
        self.task_manager = task_manager
        self.sr = sr

        self.title("Add New Task")
        self.geometry("400x450")
        self.transient(master)
        self.grid_columnconfigure(0, weight=1)

        self.label = customtkinter.CTkLabel(self, text="Add New Task", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=20)

        self.task_type_var = customtkinter.StringVar(value="Study")
        self.task_type_menu = customtkinter.CTkOptionMenu(self, values=["Study", "Work"], variable=self.task_type_var, command=self.on_task_type_change)
        self.task_type_menu.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.name_entry = customtkinter.CTkEntry(self, placeholder_text="Task Name")
        self.name_entry.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.duedate_entry = customtkinter.CTkEntry(self, placeholder_text="Due Date (YYYY-MM-DD)")
        self.duedate_entry.insert(0, (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'))

        self.note_entry = customtkinter.CTkEntry(self, placeholder_text="Note")
        self.note_entry.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        # --- Frame for task-specific fields ---
        self.specific_fields_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.specific_fields_frame.grid(row=5, column=0, padx=20, pady=10, sticky="ew")
        self.specific_fields_frame.grid_columnconfigure(0, weight=1)

        # --- WorkTask field ---
        self.priority_label = customtkinter.CTkLabel(self.specific_fields_frame, text="Priority:")
        self.priority_var = customtkinter.IntVar(value=0)
        self.priority_menu = customtkinter.CTkOptionMenu(self.specific_fields_frame, values=["Low (0)", "Medium (1)", "High (2)"], command=lambda p: self.priority_var.set(int(p.split(" ")[1].strip("()"))))
        
        # --- StudyTask field ---
        self.study_info_label = customtkinter.CTkLabel(self.specific_fields_frame, text="Review dates are set automatically.")
        
        self.add_button = customtkinter.CTkButton(self, text="Add Task", command=self.add_task)
        self.add_button.grid(row=6, column=0, padx=20, pady=20, sticky="ew")
        
        self.on_task_type_change("Study")
        
    def on_task_type_change(self, new_type: str):
        
        for widget in self.specific_fields_frame.winfo_children():
            widget.grid_forget()
        
        if new_type == "Work":
            self.duedate_entry.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
            self.priority_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
            self.priority_menu.grid(row=0, column=1, padx=5, pady=5, sticky="e")
        elif new_type == "Study":
            self.duedate_entry.grid_forget()
            self.study_info_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

    def add_task(self):
        
        name = self.name_entry.get()
        note = self.note_entry.get()
        task_type = self.task_type_var.get()

        if not name:
            show_error("Name is Required")
            return

        if task_type == "Study":
            new_task = StudyTask(name, note)
            
        else:
            due_date_str = self.duedate_entry.get()
            if not due_date_str:
                show_error("Due Date is required.")
                return
                
            try:
                # Validate date format
                datetime.datetime.strptime(due_date_str, "%Y-%m-%d")
            except ValueError:
                show_error("Date must be in YYYY-MM-DD format.")
                return
                
            priority = self.priority_var.get()
            new_task = WorkTask(name, due_date_str, note, priority)
        
        self.task_manager.add_task(new_task)
        self.sr()
        self.destroy()

# edit task window
class TaskEditToplevel(customtkinter.CTkToplevel):

    def __init__(self, master, task: Task, sr):
        super().__init__(master)
        
        self.task = task
        self.sr = sr

        self.title("Edit Task")
        self.geometry("400x550")
        self.transient(master)
        self.grid_columnconfigure(0, weight=1)

        self.label = customtkinter.CTkLabel(self, text="Edit Task", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=20)

        self.task_type_label = customtkinter.CTkLabel(self, text=f"Type: {self.task.get_task_type()}", font=customtkinter.CTkFont(size=12, slant="italic"))
        self.task_type_label.grid(row=1, column=0, padx=20, pady=(0, 10))

        self.name_note_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.name_note_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.name_note_frame.grid_columnconfigure(1, weight=1)

        self.name_label = customtkinter.CTkLabel(self.name_note_frame, text="Name:      ")
        self.name_entry = customtkinter.CTkEntry(self.name_note_frame, placeholder_text="Task Name")
        self.name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.name_entry.insert(0, self.task.name)

        self.note_label = customtkinter.CTkLabel(self.name_note_frame, text="Note:    ")
        self.note_entry = customtkinter.CTkEntry(self.name_note_frame, placeholder_text="Note")
        self.note_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.note_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.note_entry.insert(0, self.task.note)

        # --- Frame for task-specific fields ---

        

        self.specific_fields_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.specific_fields_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.specific_fields_frame.grid_columnconfigure(1, weight=1)

        if isinstance(self.task, WorkTask):
            self.duedate_label = customtkinter.CTkLabel(self.specific_fields_frame, text="Due Date:")
            self.duedate_entry = customtkinter.CTkEntry(self.specific_fields_frame, placeholder_text="Due Date (YYYY-MM-DD)")
            self.duedate_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
            self.duedate_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
            self.duedate_entry.insert(0, self.task.due_date_str)
            
            self.priority_label = customtkinter.CTkLabel(self.specific_fields_frame, text="Priority:")
            self.priority_var = customtkinter.IntVar(value=self.task.priority)
            
            priority_map = {0: "Low (0)", 1: "Medium (1)", 2: "High (2)"}
            self.priority_menu = customtkinter.CTkOptionMenu(
                self.specific_fields_frame, 
                values=["Low (0)", "Medium (1)", "High (2)"], 
                command=lambda p: self.priority_var.set(int(p.split(" ")[1].strip("()")))
            )
            self.priority_menu.set(priority_map.get(self.task.priority, "Low (0)"))
            
            self.priority_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
            self.priority_menu.grid(row=1, column=1, padx=5, pady=5, sticky="ew")


        
        self.save_button = customtkinter.CTkButton(self, text="Save Changes", command=self.save_task)
        self.save_button.grid(row=4, column=0, padx=20, pady=20, sticky="ew")
        
    def save_task(self):
        
        name = self.name_entry.get()
        note = self.note_entry.get()

        if not name:
            show_error("Name is Required")
            return

        self.task.name = name
        self.task.note = note

        if isinstance(self.task, WorkTask):
            due_date_str = self.duedate_entry.get()
            if not due_date_str:
                show_error("Due Date is required.")
                return
            
            try:
                new_due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d")
            except ValueError:
                show_error("Date must be in YYYY-MM-DD format.")
                return
                
            self.task.due_date = new_due_date
            self.task.priority = self.priority_var.get()
        
        self.sr()
        self.destroy()


def show_error(msg):
        # Show some error message
        CTkMessagebox(title="Error", message=msg, icon="cancel")