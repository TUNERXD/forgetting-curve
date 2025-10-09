from data import TaskManager
# from gui import Program
from test import Program

def main():
    task_manager = TaskManager()
    app = Program(task_manager)
    app.run()

if __name__ == "__main__":
    main()