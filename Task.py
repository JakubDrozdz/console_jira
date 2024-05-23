import csv
from TaskType import *
import itertools

class Task:
    __taskExtent = []

    def __init__(self, task_description: str, priority: str, type: TaskType, sprint_number: str, task_number: int = -1):
        if task_number == -1:
            self.task_number = len(Task.get_extent()) + 1
        else:
            self.task_number = task_number
        self.task_description = task_description
        self.priority = priority
        self.type = type
        self.sprint_number = sprint_number
        Task.__taskExtent.append(self)

    def __str__(self):
        return (f'Task number: {self.task_number}\n'
                f'Task description: {self.task_description}\n'
                f'Task priority: {self.priority}\n'
                f'Task type: {self.type}\n'
                f'Sprint number: {self.sprint_number}')

    @staticmethod
    def get_extent():
        return Task.__taskExtent

    @staticmethod
    def print_extent():
        print("All tasks:", end="\n\n")
        for task in Task.__taskExtent:
            print(task, end="\n\n")

    @staticmethod
    def write_extent():
        fieldnames = ["task_number", "task_description", "priority", "type", "sprint_number"]
        with open("tasks.csv", "w") as tasks_file:
            writer = csv.DictWriter(tasks_file, fieldnames, delimiter=";")
            writer.writeheader()
            for task in Task.__taskExtent:
                tasks_file.write(f'{task.task_number};{task.task_description};{task.priority};{task.type};{task.sprint_number}\n')

    @staticmethod
    def read_extent():
        with open("tasks.csv", "r") as tasks_file:
            reader = csv.DictReader(tasks_file, delimiter=";")
            for entry in reader:
                try:
                    Task(
                        task_number=int(entry["task_number"]),
                        task_description=str(entry["task_description"]),
                        priority=str(entry["priority"]),
                        type=TaskType(entry["type"]),
                        sprint_number=str(entry["sprint_number"])
                    )
                except:
                    print("Error while adding Task: " + entry)
