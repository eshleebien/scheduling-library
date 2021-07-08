from datetime import timedelta, datetime

class Person(object):
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self.appointments = []

    def check_availability(self, new_dates: tuple):
        return all((new_dates[0] <= a[0] or new_dates[0] >= a[1]) and (new_dates[1] <= a[0] or new_dates[1] >= a[1]) and (a[0], a[1]) != new_dates for a in self.appointments)

    def create_appointment(self, dates: tuple):
        self.appointments.append(dates)

    def get_appointments(self, upcoming=False):
        if upcoming:
            self.appointments.sort(key=lambda tup: tup[0])

            date_now = datetime.now().replace(second=0, microsecond=0)
            return list(filter(lambda a: (a[0] >= date_now), self.appointments))
        return self.appointments



class Event(object):
    def __init__(self, persons: list, time_slot: datetime, description=""):
        self.attendees = persons
        self.description = description
        time_slot = time_slot.replace(second=0, microsecond=0)
        self.dates = (time_slot, time_slot + timedelta(hours=1))

    def book(self):
        if all(attendee.check_availability(self.dates) for attendee in self.attendees):
            for attendee in self.attendees:
                attendee.create_appointment((self.dates[0], self.dates[1], self.description))
            return True
        return False

    def suggest_time(self):
        dates = self.dates
        while True: 
            is_all_available = all(attendee.check_availability(dates) for attendee in self.attendees)
            if is_all_available:
                return dates
            dates = (dates[0] + timedelta(hours=.5), dates[1] + timedelta(hours=.5))

    def start(self):
        if self.dates[0] == datetime.now().replace(second=0, microsecond=0):
            self.started = True
            return True
        raise Exception("Event can't be started if not at the hour mark")
