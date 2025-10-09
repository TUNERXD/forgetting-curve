import customtkinter as ctk



class Program():

    def __init__(self, task_manager):
        self.task_manager = task_manager
        self.root = ctk.CTk()
        self.root.title("Dashboard")
        ctk.set_appearance_mode("dark")

        # --- UI LAYOUT ---
        top_frame = ctk.CTkFrame(self.root,)
        top_frame.pack(pady=5, padx=5)

        bottom_frame = ctk.CTkFrame(self.root)
        bottom_frame.pack(pady=5, padx=5)

        # --- Left top: Assignments ---
        today_task = ctk.CTkScrollableFrame(top_frame)
        today_task.grid(row=0, column=0)

        # --- Middle: Menu Buttons ---
        menu = ctk.CTkFrame(top_frame,)
        menu.grid(row=0, column=1)

        # --- Right top: Study ---
        today_topic = ctk.CTkScrollableFrame(top_frame)
        today_topic.grid(row=0, column=2)

        # --- Bottom: Graph ---
        graph_frame = ctk.CTkFrame(bottom_frame)
        graph_frame.pack()

        
        

    def run(self):
        self.root.mainloop()