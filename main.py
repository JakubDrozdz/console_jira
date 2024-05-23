from console_jira import *
from Task import *
from TaskType import *

if __name__ == '__main__':
    Task.read_extent()
    try:
        app()
    finally:
        Task.write_extent()
