from console_jira import *
from Task import *
from TaskType import *

if __name__ == '__main__':
    Task.read_extent()
    #Task.print_extent()
    t1 = Task(task_description="test desc", priority="high", type=TaskType.TASK, sprint_number="S01")
    Task.print_extent()
    #t2 = Task(2, "test desc 2", "medium", "S01")
    #Task.print_extent()
    Task.write_extent()
