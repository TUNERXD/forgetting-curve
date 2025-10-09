from datetime import datetime
from abc import ABC, abstractmethod

'''
The Forgetting Curve Formula
R = e^(-t/S)

R = memory retention
t = time since learning
S = Strength of learning
'''

class TaskManager(object):
    
    def __init__(self):
        self._assignments = []
        self._study_topics = []
        self._all_subjects = []

        # --- Sample Data ---
        self.set_assignments(name="Finish Python Homework", due_date="2025-10-10", priority=1)
        self.set_assignments(name="Finish Python Homework", due_date="2025-10-10", priority=1)
        self.set_study_topics("Calculus Review", 85)
        self.set_study_topics("Physics Kinematics", 92)

    def get_assignments(self):
        return self._assignments
    
    def set_assignments(self, name, due_date, priority):
        self._assignments.append(Assignment(name, due_date, priority))

    def get_study_topics(self):
        return self._study_topics
    
    def set_study_topics(self, name, retention):
        self._study_topics.append(Study(name, retention))


class Task(ABC):

    def __init__(self, name):
        self._name = name

    @property
    @abstractmethod
    def name(self):
        return self._name
    
    @name.setter
    @abstractmethod
    def name(self, new_name):
        self.name = new_name

class Study(Task):
    def __init__(self, name, retention):
        super().__init__(name)
        self._date = datetime.now().date()
        self._retention = retention
        self._next_review = self._date
        self._rep = 1

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, new_name):
        self._name  = new_name

    @property
    def retention(self):
        return self._retention
    
    @retention.setter
    def retention(self, new_retention):
        self._retention = new_retention

    @property
    def next_review(self):
        return self._next_review
    
    @next_review.setter
    def next_review(self, new_date):
        self._next_review = new_date

class Assignment(Task):
    def __init__(self, name, due_date, priority):
        super().__init__(name)
        self._due_date = due_date
        # self._subject = subject
        self._priority = priority

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, new_name):
        self._name  = new_name

    @property
    def due_date(self):
        return self._due_date
    
    @due_date.setter
    def due_date(self, new_date):
        self._due_date = new_date

    @property
    def priority(self):
        return self._priority
    
    @priority.setter
    def priority(self, new_priority):
        self._priority = new_priority

    # @property
    # def subject(self):
    #     return self._subject
    
    # @subject.setter
    # def subject(self, new_subject):
    #     self._subject = new_subject
