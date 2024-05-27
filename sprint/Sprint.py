from datetime import datetime, timedelta, date
import csv

from exception.NoSprintPresentException import NoSprintPresentException


class Sprint:
    __sprintExtent = []

    def __init__(self, end_date: datetime.date, sprint_number: str = None, start_date: datetime.date = None):
        self.sprint_number = None
        self.start_date = None
        self.end_date = None
        if sprint_number is not None and start_date is not None:
            self.set_start_date(start_date)
            self.set_end_date(end_date)
            self.set_sprint_number(sprint_number)
        else:
            self.set_start_date()
            self.set_end_date(end_date)
            self.set_sprint_number()
        Sprint.__sprintExtent.append(self)

    def __str__(self):
        return (f"{self.sprint_number}, start: {self.start_date}, end: {self.end_date}")

    def set_sprint_number(self, sprint_number: str = None):
        if sprint_number is None:
            self.sprint_number = "S" + str(self.calculate_sprint_number())
        else:
            self.sprint_number = sprint_number

    def get_sprint_number(self):
        return self.sprint_number

    @staticmethod
    def calculate_sprint_number():
        curr_number = max(
            int(sprint.sprint_number[1:]) for sprint in Sprint.__sprintExtent) if Sprint.__sprintExtent else 0
        return curr_number + 1

    def set_start_date(self, start_date: datetime.date = None):
        if start_date is None:
            self.start_date = self.calculate_start_date()
        else:
            self.start_date = start_date

    @staticmethod
    def calculate_start_date():
        return max(sprint.end_date for sprint in Sprint.get_extent()) + timedelta(days=1) \
            if Sprint.get_extent() else date.today()

    def set_end_date(self, end_date: datetime.date):
        self.end_date = end_date

    @staticmethod
    def calculate_end_date(start_date: datetime.date, end_date: datetime.date):
        if (end_date - start_date).days < 14:
            return start_date + timedelta(days=14)
        elif (end_date - start_date).days > 28:
            return start_date + timedelta(days=28)
        return end_date

    @staticmethod
    def get_extent():
        return list(Sprint.__sprintExtent)

    @staticmethod
    def get_sprint(sprint_number: str):
        sprints_filtered = filter(lambda sprint: sprint.sprint_number == sprint_number, Sprint.get_extent())
        sprint = next(sprints_filtered, None)
        if sprint is None:
            raise NoSprintPresentException("No sprint with number " + sprint_number)
        return sprint

    @staticmethod
    def write_extent():
        fieldnames = ["sprint_number", "start_date", "end_date"]
        with open("sprint/sprints.csv", "w") as sprint_file:
            writer = csv.DictWriter(sprint_file, fieldnames, delimiter=";")
            writer.writeheader()
            for sprint in Sprint.__sprintExtent:
                sprint_file.write(
                    f'{sprint.sprint_number};{sprint.start_date};{sprint.end_date}\n')

    @staticmethod
    def read_extent():
        with open("sprint/sprints.csv", "r") as tasks_file:
            reader = csv.DictReader(tasks_file, delimiter=";")
            for entry in reader:
                try:
                    Sprint(
                        sprint_number=str(entry["sprint_number"]),
                        start_date=datetime.strptime(entry["start_date"],
                                          "%Y-%m-%d").date(),
                        end_date=datetime.strptime(entry["end_date"],
                                          "%Y-%m-%d").date(),
                    )
                except:
                    print("Error while adding Sprint: " + entry)

    @staticmethod
    def get_active_sprints():
        sprints_filtered = filter(lambda sprint: sprint.end_date >= date.today(), Sprint.get_extent())
        sprints = set()
        for sprint in sprints_filtered:
            sprints.add(sprint)
        return sprints

    @staticmethod
    def get_inactive_sprints():
        sprints_filtered = filter(lambda sprint: sprint.end_date < date.today(), Sprint.get_extent())
        sprints = set()
        for sprint in sprints_filtered:
            sprints.add(sprint)
        return sprints

    @staticmethod
    def list_sprints():
        print("Active sprints:")
        for sprint in sorted(Sprint.get_active_sprints(), key=lambda s: s.sprint_number, reverse=True):
            print(sprint)
        print("Inactive sprints:")
        for sprint in sorted(Sprint.get_inactive_sprints(), key=lambda s: s.sprint_number, reverse=True):
            print(sprint)
