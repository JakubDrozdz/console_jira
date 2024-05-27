from datetime import *

from Task import *
from exception.NoSprintPresentException import NoSprintPresentException


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
    print("2 - edit task")
    print("3 - remove task")
    print("4 - list tasks")
    print("5 - list filtered tasks")
    print("6 - add sprint")
    print("7 - list sprints")
    print("0 - exit")


def invoke_option(user_input):
    match user_input:
        case 1:
            add_task()
        case 2:
            edit_task()
        case 3:
            remove_task()
        case 4:
            Task.print_extent()
        case 5:
            try:
                Task.print_filtered_extent()
            except NoSprintPresentException as ex:
                print(ex.message + "\nOperation cancelled")
            except ValueError:
                print("Wrong data! Operation cancelled")
        case 6:
            try:
                create_sprint()
            except ValueError:
                print("Invalid date format")
        case 7:
            Sprint.list_sprints()


def add_task():
    try:
        task_title = str(input("Enter task title "))
        task_description = str(input("Enter task description: "))
        print("Choose task priority from following: ")
        for value in TaskPriority:
            print(f"\t{value}")
        priority = TaskPriority(input("Enter task priority: "))
        print("Choose task type from following: ")
        for value in TaskType:
            print(f"\t{value}")
        task_type = TaskType(input("Enter task type: "))
        print("Choose task status from following: ")
        for value in TaskStatus:
            print(f"\t{value}")
        task_status = TaskStatus(input("Enter task status: "))
        sprint = choose_sprint()
        Task(task_title=task_title, task_description=task_description, priority=priority, type=TaskType(task_type), status=TaskStatus(task_status), sprint_number=sprint)
    except ValueError:
        print("Wrong data!\nAborting operation")
    except InvalidTaskInputException as ex:
        print(ex.message + "\nAborting operation")
    except NoSprintPresentException as ex:
        print(ex.message + "\nAborting operation")


def remove_task():
    user_input = input("Enter task number: ")
    try:
        user_input = int(user_input)
        Task.remove_from_extent(user_input)
    except ValueError:
        print("Invalid input")


def choose_sprint():
    print("Choose sprint number from following: ")
    for sprint in Sprint.get_active_sprints():
        print(f"\t{sprint.get_sprint_number()}")
    return Sprint.get_sprint(input("Enter sprint number: "))


def create_sprint():
    print("Details of next sprint:")
    print("Sprint number: " + str(Sprint.calculate_sprint_number()))
    start_date = Sprint.calculate_start_date()
    print("Sprint start date: " + str(start_date))
    end_date = datetime.strptime(input("Enter end date(yyyy-mm-dd) (sprint max length is 2 - 4 weeks):"), "%Y-%m-%d").date()
    end_date = Sprint.calculate_end_date(end_date=end_date, start_date=start_date)
    print("Sprint end date: " + str(end_date))
    accepted = input("Pres Y to accept or other key to reject:")
    if accepted.lower() == "y":
        Sprint(end_date)
        print("Sprint created")
    else:
        print("Sprint not created")

def edit_task():
    user_input = input("Enter task number: ")
    try:
        user_input = int(user_input)
        task = Task.get_task(user_input)
        task.edit()
    except ValueError:
        print("Invalid input")
    except InvalidTaskInputException as ex:
        print(ex.message + "\nAborting operation")
