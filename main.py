from console_jira import *
from task.Task import *

if __name__ == '__main__':
    Sprint.read_extent()
    Task.read_extent()
    try:
        app()
    finally:
        Sprint.write_extent()
        Task.write_extent()
