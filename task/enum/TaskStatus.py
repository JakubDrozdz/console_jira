from enum import Enum

class TaskStatus(Enum):
    OPEN = "Open"
    IN_PROGRESS = "In progress"
    IN_REVIEW = "In review"
    CLOSED = "Closed"

    def __str__(self):
        return self.value
