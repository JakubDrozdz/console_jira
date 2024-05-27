import csv

from exception.InvalidTaskInputException import InvalidTaskInputException
from Sprint import Sprint
from TaskPriority import TaskPriority
from TaskStatus import TaskStatus
from TaskType import TaskType


class Task:

    __taskExtent = []

    def __init__(self, task_description: str, task_title: str, priority: TaskPriority, type: TaskType, status: TaskStatus, sprint_number: Sprint, task_number: int = -1):
        self.task_number = None
        self.task_title = None
        self.task_description = None
        self.priority = None
        self.type = None
        self.sprint_number = None
        self.task_status = None

        self.set_task_number(task_number)
        self.set_task_title(task_title)
        self.set_task_description(task_description)
        self.set_task_priority(priority)
        self.set_task_type(type)
        self.set_task_sprint_number(sprint_number)
        self.set_task_status(status)
        Task.__taskExtent.append(self)

    def __str__(self):
        return (f'Task number: {self.task_number}\n'
                f'Task title: {self.task_title}\n'
                f'Task description: {self.task_description}\n'
                f'Task priority: {self.priority}\n'
                f'Task type: {self.type}\n'
                f'Task status: {self.task_status}\n'
                f'Sprint number: {self.sprint_number.get_sprint_number()}')

    def set_task_number(self, task_number: int):
        if task_number == -1:
            self.task_number = max(task.task_number for task in Task.get_extent()) + 1 if Task.get_extent() else 1
        else:
            self.task_number = task_number

    def set_task_title(self, task_title: str):
        self.task_title = task_title

    def set_task_description(self, task_description: str):
        if task_description is None or not task_description.strip():
            raise InvalidTaskInputException("Task description cannot be null nor empty")
        self.task_description = task_description

    def set_task_priority(self, priority: TaskPriority):
        self.priority = priority

    def set_task_type(self, type: TaskType):
        self.type = type

    def set_task_sprint_number(self, sprint_number: Sprint):
        self.sprint_number = sprint_number

    def set_task_status(self, status: TaskStatus):
        self.task_status = status

    @staticmethod
    def get_extent():
        return list(Task.__taskExtent)

    @staticmethod
    def print_extent():
        print("All tasks:", end="\n\n")
        for task in Task.__taskExtent:
            print(task, end="\n\n")

    @staticmethod
    def write_extent():
        fieldnames = ["task_number", "task_title", "task_description", "priority", "type", "status", "sprint_number"]
        with open("tasks.csv", "w") as tasks_file:
            writer = csv.DictWriter(tasks_file, fieldnames, delimiter=";")
            writer.writeheader()
            for task in Task.__taskExtent:
                tasks_file.write(f'{task.task_number};{task.task_title};{task.task_description};{task.priority};{task.type};{task.task_status};{task.sprint_number.get_sprint_number()}\n')

    @staticmethod
    def read_extent():
        with open("tasks.csv", "r") as tasks_file:
            reader = csv.DictReader(tasks_file, delimiter=";")
            for entry in reader:
                try:
                    Task(
                        task_number=int(entry["task_number"]),
                        task_title=str(entry["task_title"]),
                        task_description=str(entry["task_description"]),
                        priority=TaskPriority(entry["priority"]),
                        type=TaskType(entry["type"]),
                        status=TaskStatus(entry["status"]),
                        sprint_number=Sprint.get_sprint(entry["sprint_number"])
                    )
                except:
                    print("Error while adding Task: " + entry)

    @staticmethod
    def remove_from_extent(task_number: int):
        filtered_tasks = list(filter(lambda task: task.task_number == task_number, Task.__taskExtent))
        if len(filtered_tasks) != 1:
            raise ValueError
        Task.__taskExtent.remove(filtered_tasks[0])
        print("Task removed")