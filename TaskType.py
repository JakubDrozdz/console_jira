from enum import Enum

class TaskType(Enum):
    TASK = "Task"
    DEFECT = "Defect"
    STORY = "Story"
    EPIC = "Epic"

    def __str__(self):
        return self.value
