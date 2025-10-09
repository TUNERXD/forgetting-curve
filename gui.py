from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import customtkinter as ctk
from matplotlib import *

# TODO: Add Task
# TODO: Edit Task
# TODO: Save & Load Task
# TODO: Calculate Next Review
# TODO: Matplotlib Graph

class Program:

    def __init__(self, task_manager):
        self.task_manager = task_manager
        self.root = Tk()
        self.root.title("Dashboard")

        # --- UI LAYOUT ---
        top_frame = Frame(self.root,)
        top_frame.pack(pady=5, padx=5)

        bottom_frame = Frame(self.root)
        bottom_frame.pack(pady=5, padx=5)

        # --- Left top: Assignments ---
        today_task = Frame(top_frame, padding=10)
        today_task.grid(row=0, column=0)

        # --- Middle: Menu Buttons ---
        menu = Frame(top_frame, padding=10)
        menu.grid(row=0, column=1)

        # --- Right top: Study ---
        today_topic = Frame(top_frame, padding=10)
        today_topic.grid(row=0, column=2)

        # --- Bottom: Graph ---
        graph_frame = Frame(bottom_frame, padding=10)
        graph_frame.pack()

        # --- ASSIGNMENTS TREEEVIEW ---
        self.today_tree = Treeview(today_task, columns=("Assignment", "Priority"), show="headings")
        self.today_tree.heading("Assignment", text="Assignment")
        self.today_tree.heading("Priority", text="Priority")
        self.today_tree.column("Assignment", width=150, minwidth=50, stretch=YES)
        self.today_tree.column("Priority", width=150, minwidth=50, stretch=YES)
        self.today_tree.pack(fill="both", expand=True, pady=5)

        self.populate_assignments()

        # Scrollbar for Assignment
        today_scroll = Scrollbar(today_task, orient="vertical", command=self.today_tree.yview)
        self.today_tree.configure(yscrollcommand=today_scroll.set)
        self.today_tree.grid(row=0, column=0, sticky="nsew")
        today_scroll.grid(row=0, column=1, sticky="ns")

        # Binding
        today_task.grid_rowconfigure(0, weight=1)
        today_task.grid_columnconfigure(0, weight=1)
        self.today_tree.bind("<Button-1>", self.today_task_click)

        add_task = Button(menu, text="Add Task", command=self.add_task_window)
        add_task.pack(fill='x', pady=5, padx=5)
        edit_task = Button(menu, text="All Tasks")
        edit_task.pack(fill='x', pady=5, padx=5)
        sync = Button(menu, text="Save")
        sync.pack(fill='x', pady=5, padx=5)

        # --- STUDY TREEVIEW ---
        self.topic_tree = Treeview(today_topic, columns=("Topic", "Retention"), show="headings")
        self.topic_tree.heading("Topic", text="Topic")
        self.topic_tree.heading("Retention", text="Retention")
        self.topic_tree.column("Topic", width=150, minwidth=50, stretch=YES)
        self.topic_tree.column("Retention", width=150, minwidth=50, stretch=YES)
        self.topic_tree.pack(fill="both", expand=True, pady=5)

        self.populate_study()

        # Scrollbar for Study
        today_topic_scroll = Scrollbar(today_topic, orient="vertical", command=self.topic_tree.yview)
        self.topic_tree.configure(yscrollcommand=today_topic_scroll.set)
        self.topic_tree.grid(row=0, column=0, sticky="nsew")
        today_topic_scroll.grid(row=0, column=1, sticky="ns")
        today_topic.grid_rowconfigure(0, weight=1)
        today_topic.grid_columnconfigure(0, weight=1)
        self.topic_tree.bind("<Button-1>", self.today_topic_click)

        # Bind double-click event to the topic tree for editing
        # self.topic_tree.bind("<Double-1>", self.on_topic_double_click)
        # self.today_tree.bind("<Double-1>", self.on_assignment_double_click)


        # --- Placeholder for Graph ---
        canvas = Canvas(graph_frame, width=820, height=300, bg="white")
        canvas.pack(side="left", fill="both", expand=True)


    def run(self):
        self.root.mainloop()

    def populate_assignments(self):
        for assignment in self.task_manager.get_assignments():
            self.today_tree.insert("", "end", values=(assignment.name, assignment.priority))

    def populate_study(self):
        for topics in self.task_manager.get_study_topics():
            self.topic_tree.insert("", "end", values=(topics.name, topics.retention))

    # def on_topic_double_click(self, event):

    def all_tasks_window(self):
        pass

    def add_task_window(self):
        add_win = Toplevel(self.root)
        add_win.title("topic")
        add_win.geometry("400x300")

        # Combo box Assignment/Study
        Label(add_win, text="Task:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        task_choice = StringVar()
        taskchosen = Combobox(add_win, width = 27, textvariable = task_choice)

        taskchosen['values'] = ("<< Select >>", "Assignment", "Study Topic")
        taskchosen.grid(row = 0, column = 1 )
        taskchosen.current(0)

        # Name Entry
        Label(add_win, text="Name:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        name_entry = Entry(add_win, width=30)
        name_entry.grid(row=1, column=1, padx=10, pady=5)

        if task_choice == "Assignment":

            # Combo box Priority
            Label(add_win, text="Priority:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
            priority_choice = IntVar()
            prioritychosen = Combobox(add_win, width = 27, textvariable = priority_choice)

            prioritychosen['values'] = (0, 1, 2, 3, 4 ,5)
            prioritychosen.grid(row =2, column = 1)
            prioritychosen.current(0)

            # Due date
            Label(add_win, text="Due Date:").grid(row=2, column=0, padx=10, pady=5, sticky="w")

            def confirm_add():
                task_type = task_choice
                name = name_entry.get()

                priority = priority_choice

            


        

        add_button = Button(add_win, text="Add Task", command=confirm_add)
        add_button.grid(row=4, column=0, columnspan=2, pady=10)


    def today_topic_click(self, event):
        new_win = Toplevel(self.root)
        new_win.title("topic")
        new_win.geometry("400x300")

        topic_details = Label(new_win, text="This will contain Topic detail")
        topic_details.pack(padx=10, pady=10)

        complete_button = Button(new_win, text="Complete review")
        complete_button.pack()
    

    def today_task_click(self, event):
        new_win = Toplevel(self.root)
        new_win.title("Task")
        new_win.geometry("400x300")

        task_details = Label(new_win, text="This will contain Topic detail")
        task_details.pack(padx=10, pady=10)
        
        complete_button = Button(new_win, text="Complete task")
        complete_button.pack(pady=5)

    def edit_click(self):
        new_win = Toplevel(self.root)
    
    def sync_click(self):
        new_win = Toplevel(self.root)