from enum import Enum

class TaskPriority(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    High = "High"
    CRITICAL = "Critical"

    def __str__(self):
        return self.value
