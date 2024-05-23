from Task import *


def app():
    is_app_running = True
    while is_app_running:
        show_menu()

        user_input = input("Choose an option: ")
        try:
            user_input = int(user_input)
            if user_input < 0:
                raise ValueError
        except ValueError:
            print("Invalid input")
            is_app_running = False
            continue

        if user_input == 0:
            is_app_running = False
            print("Goodbye!")
            continue
        invoke_option(user_input)


def show_menu():
    print("1 - add task")
    print("2 - remove task")
    print("3 - list tasks")
    print("0 - exit")


def invoke_option(user_input):
    match user_input:
        case 1:
            add_task()
        case 2:
            remove_task()
        case 3:
            Task.print_extent()


def add_task():
    Task(task_description="test desc", priority="high", type=TaskType.TASK, sprint_number="S01")


def remove_task():
    user_input = input("Enter task number: ")
    try:
        user_input = int(user_input)
        Task.remove_from_extent(user_input)
    except ValueError:
        print("Invalid input")
