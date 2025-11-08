import datetime
import math
from abc import ABC, abstractmethod
import pickle
import os

INTERVALS_IN_DAYS = [1, 3, 7, 14, 30, 60, 120] 
SAVE_FILE = "tasks.pkl"

class TaskManager(object):
    
    def __init__(self):
        self.__tasks = []

    def add_task(self, task):
        self.__tasks.append(task)

    def delete_task(self, task):
        if task in self.__tasks:
            self.__tasks.remove(task)
            
    def get_tasks(self):
        
        def sort_key(task):
            '''
            1) Due study
            2) Due Work Priority high -> medium -> low
            3) Work Priority high -> medium -> low
            4) fall back
            '''
    
            if isinstance(task, StudyTask):
                if task.is_due():
                    return (1, task.due_date)
                else:
                    
                    return (9, task.due_date)
            
            elif isinstance(task, WorkTask):

                if task.is_due():
                    sort_group = 5 - task.priority
                    return (sort_group, task.due_date)
                else:

                    sort_group = 8 - task.priority
                    return (sort_group, task.due_date)
            
            else:
                
                return (10, task.created_at)

        self.__tasks.sort(key=sort_key)
        return self.__tasks
        
    def save_tasks(self, filename=SAVE_FILE):
        
        try:
            with open(filename, "wb") as f:
                pickle.dump(self, f)
            print("Tasks saved successfully.")
        except Exception as e:
            print(f"Error saving tasks: {e}")

    @staticmethod
    def load_tasks(filename=SAVE_FILE):
        if os.path.exists(filename):
            try:
                with open(filename, "rb") as f:
                    manager = pickle.load(f)
                    print("Tasks loaded successfully.")
                    return manager
            except (pickle.UnpicklingError, EOFError, AttributeError, ImportError, IndexError) as e:
                print(f"Error loading tasks file. Creating a new one. Error: {e}")
                return TaskManager()
        else:
            print("No save file found. Starting new TaskManager.")
            return TaskManager()


class Task(ABC):
    
    def __init__(self, name, note):
        self.__name = name
        self.__note = note
        self.__created_at = datetime.datetime.now()
        self.__due_date = datetime.datetime.now()
        self.__due_date_str = self.__due_date.strftime("%Y-%m-%d")
            

    @property
    def created_at(self):
        return self.__created_at

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, new_name):
        self.__name = new_name

    @property
    def due_date(self):
        return self.__due_date
        
    @property
    def due_date_str(self):
        return self.__due_date_str
    
    @due_date.setter
    def due_date(self, new_date: datetime.datetime):
        self.__due_date = new_date
        self.__due_date_str = new_date.strftime("%Y-%m-%d")
        
    @property
    def note(self):
        return self.__note
        
    @note.setter
    def note(self, new_note):
        self.__note = new_note

    @abstractmethod
    def get_details(self) -> str:
        pass
        
    @abstractmethod
    def get_task_type(self) -> str:
        pass

    @abstractmethod
    def is_due(self):
        pass
    
    def get_common_display(self) -> str:
        return f"Due: {self.__due_date_str}\nNote: {self.__note}"

class StudyTask(Task):

    def __init__(self, name, note):
        super().__init__(name, note)
        self.__decrease = False
        self.__last_review = datetime.datetime.now()
        self.__level = 0

        self.due_date = self.__last_review

    @property
    def level(self):
        return self.__level
    
    def level_increment(self):

        if self.__level < len(INTERVALS_IN_DAYS):
            self.__level += 1
            days_to_add = INTERVALS_IN_DAYS[self.__level - 1]
            
            self.__last_review = datetime.datetime.now()
            self.due_date = self.__last_review + datetime.timedelta(days=days_to_add)

            self.__decrease = False
        else:
            self.__last_review = datetime.datetime.now()
            self.due_date = self.__last_review + datetime.timedelta(days=INTERVALS_IN_DAYS[-1])
    
    def level_decrement(self):
        if not self.__decrease:
            if self.__level - 1 < 0:
                self.__level = 0
            else:
                self.__level -= 1
            self.__decrease = True
        
    @property
    def last_review(self):
        return self.__last_review
        
    def is_due(self) -> bool:
        return self.__level == 0 or datetime.datetime.now() >= self.due_date

    def get_details(self) -> str:
        review_status = "Now" if self.is_due() else self.due_date.strftime('%Y-%m-%d')
        return f"Level: {self.level}\nNext Review: {review_status}"
        
    def get_task_type(self) -> str:
        return "Study"
        
    def get_retention_percent(self) -> float:

        t = ((datetime.datetime.now() - self.__last_review).total_seconds())/ 86400

        if self.__level == 0:
            s = INTERVALS_IN_DAYS[0]
        elif self.__level >= len(INTERVALS_IN_DAYS):
            s = INTERVALS_IN_DAYS[-1]
        else:
            s = INTERVALS_IN_DAYS[self.__level - 1]

        retention = math.e ** -(t / (4*s))
        return max(0.0, retention)


class WorkTask(Task):
    
    def __init__(self, name, due_date_str, note, priority: int = 0):
        super().__init__(name, note)
        
        try:
            self.due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d")
        except ValueError:
            self.due_date = datetime.datetime.now() + datetime.timedelta(days=1)
            
        self.__priority = priority

    @property
    def priority(self):
        return self.__priority
    
    @priority.setter
    def priority(self, new_priority):
        self.__priority = new_priority
    
    def get_details(self) -> str:
        priority_map = {0: "Low", 1: "Medium", 2: "High"}
        return f"Priority: {priority_map.get(self.priority, 'Low')}"
        
    def get_task_type(self) -> str:
        return "Work"
    
    def is_due(self):
        return datetime.datetime.now() >= self.due_date