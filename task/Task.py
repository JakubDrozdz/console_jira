import csv

from exception.InvalidTaskInputException import InvalidTaskInputException
from sprint.Sprint import Sprint
from task.enum.TaskPriority import TaskPriority
from task.enum.TaskStatus import TaskStatus
from task.enum.TaskType import TaskType


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

    def edit(self):
        print("Current data:")
        print(self)
        print("\nChoose what you want to change:")
        print("1 - title")
        print("2 - description")
        print("3 - priority")
        print("4 - type")
        print("5 - status")

        user_input = input("Yout choice: ")
        try:
            user_input = int(user_input)
            if user_input <= 0 or user_input > 5:
                raise ValueError
        except ValueError:
            print("Invalid input")
            return

        match user_input:
            case 1:
                task_title = str(input("New task title: "))
                self.set_task_title(task_title)
            case 2:
                task_description = str(input("New task description: "))
                self.set_task_description(task_description)
            case 3:
                print("Choose new task priority from following: ")
                for value in TaskPriority:
                    print(f"\t{value}")
                priority = TaskPriority(input("New task priority: "))
                self.set_task_priority(priority)
            case 4:
                print("Choose new task type from following: ")
                for value in TaskType:
                    print(f"\t{value}")
                task_type = TaskType(input("New task type: "))
                self.set_task_type(task_type)
            case 5:
                print("New task status from following: ")
                for value in TaskStatus:
                    print(f"\t{value}")
                task_status = TaskStatus(input("Enter new task status: "))
                self.set_task_status(task_status)

    @staticmethod
    def get_extent():
        return list(Task.__taskExtent)

    @staticmethod
    def get_task(task_number: int):
        tasks_filtered = filter(lambda task: task.task_number == task_number, Task.__taskExtent)
        task = next(tasks_filtered, None)
        if task is None:
            raise InvalidTaskInputException("No task with number " + str(task_number))
        return task

    @staticmethod
    def print_extent():
        print("All tasks:", end="\n\n")
        for task in Task.__taskExtent:
            print(task, end="\n\n")

    @staticmethod
    def print_filtered_extent():
        print("Choose filter:")
        print("1 - by priority")
        print("2 - by type")
        print("3 - by status")
        print("4 - by sprint")

        user_input = input("Yout choice: ")
        try:
            user_input = int(user_input)
            if user_input <= 0 or user_input > 4:
                raise ValueError
        except ValueError:
            print("Invalid input")
            return

        tasks = set()
        match user_input:
            case 1:
                print("Choose task priority from following: ")
                for value in TaskPriority:
                    print(f"\t{value}")
                priority = TaskPriority(input("Task priority: "))
                tasks = set(filter(lambda task: task.priority == priority, Task.__taskExtent))
            case 2:
                print("Choose task type from following: ")
                for value in TaskType:
                    print(f"\t{value}")
                type = TaskType(input("Task type: "))
                tasks = set(filter(lambda task: task.type == type, Task.__taskExtent))
            case 3:
                print("Choose task status from following: ")
                for value in TaskStatus:
                    print(f"\t{value}")
                status= TaskStatus(input("Task status: "))
                tasks = set(filter(lambda task: task.task_status == status, Task.__taskExtent))
            case 4:
                print("Choose task status from following: ")
                for value in Sprint.get_extent():
                    print(f"\t{value.get_sprint_number()}")
                sprint_number = Sprint.get_sprint(input("Sprint number: "))
                tasks = set(filter(lambda task: task.sprint_number == sprint_number, Task.__taskExtent))

        print("Tasks:", end="\n\n")
        for task in tasks:
            print(task, end="\n\n")

    @staticmethod
    def write_extent():
        fieldnames = ["task_number", "task_title", "task_description", "priority", "type", "status", "sprint_number"]
        with open("task/tasks.csv", "w") as tasks_file:
            writer = csv.DictWriter(tasks_file, fieldnames, delimiter=";")
            writer.writeheader()
            for task in Task.__taskExtent:
                tasks_file.write(f'{task.task_number};{task.task_title};{task.task_description};{task.priority};{task.type};{task.task_status};{task.sprint_number.get_sprint_number()}\n')

    @staticmethod
    def read_extent():
        with open("task/tasks.csv", "r") as tasks_file:
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
