from datetime import datetime, timedelta


class Sprint:
    __sprintExtent = set()

    def __init__(self, end_date: datetime.date):
        self.sprint_number = None
        self.start_date = None
        self.end_date = None

        self.set_sprint_number()
        self.set_start_date()
        self.set_end_date(end_date)
        Sprint.__sprintExtent.add(self)

    def set_sprint_number(self):
        self.sprint_number = "S01"

    def set_start_date(self):
        self.start_date = max(sprint.start_date for sprint in Sprint.get_extent()) + timedelta(days=1)\
            if Sprint.get_extent() else datetime.today()

    def set_end_date(self, end_date: datetime.date):
        self.end_date = end_date if (end_date - self.start_date).days >= 14 else self.start_date + timedelta(days=14)


    @staticmethod
    def get_extent():
        return set(Sprint.__sprintExtent)
