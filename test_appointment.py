import unittest
from datetime import datetime, timedelta
from appointment import Person, Event


class TestAppointment(unittest.TestCase):
    start = datetime.fromisoformat("2021-07-08 16:00")

    def setUp(self):
        self.p1 = Person("Esh", "hi@esh.ph")
        self.p2 = Person("Doe", "hi@doe.ph")

    def test_create_appointment_shall_be_created(self):
        e1 = Event([self.p1, self.p2], self.start, "This is a meeting")
        self.assertTrue(e1.book())

        # with different date
        e2 = Event([self.p1], datetime.now())
        self.assertTrue(e2.book())

    def test_create_appointment_shall_not_be_created(self):
        e1 = Event([self.p1, self.p2], self.start)
        e1.book()

        self.assertFalse(Event([self.p2], self.start).book())
        self.assertFalse(Event([self.p1], self.start).book())

    def test_not_start_appointment_if_not_same_datetime(self):
        e1 = Event([self.p1, self.p2], self.start)
        e1.book()

        with self.assertRaises(Exception) as context:
            e1.start()

    def test_start_appointment_if_same_datetime(self):
        e1 = Event([self.p1, self.p2], datetime.now())
        e1.book()

        self.assertTrue(e1.start())


class TestShowSchedule(unittest.TestCase):
    start = datetime.fromisoformat("2021-07-07 16:00")

    def setUp(self):
        self.p1 = Person("Esh", "hi@esh.ph")
        self.p2 = Person("Jose", "hi@jose.ph")

    def test_get_upcoming_appointments(self):
        e1 = Event([self.p1, self.p2], datetime.now(), "Hey! long time no see!")
        e1.book()

        e2 = Event([self.p1, self.p2], self.start, "Hey! let's reschedule")
        e2.book()

        self.assertTrue(len(self.p1.get_appointments(upcoming=True)) == 1)

    def test_get_all_appointments(self):
        e1 = Event([self.p1, self.p2], datetime.now(), "Hey! long time no see!")
        e1.book()

        e2 = Event([self.p1, self.p2], self.start, "Hey! let's reschedule")
        e2.book()

        self.assertTrue(len(self.p1.get_appointments()) == 2)


class TestSuggestSchedule(unittest.TestCase):
    start = datetime.fromisoformat("2021-07-09 16:00")
    conflict_start = datetime.fromisoformat("2021-07-09 16:30")

    def setUp(self):
        self.p1 = Person("Esh", "hi@esh.ph")
        self.p2 = Person("Jose", "hi@jose.ph")

    def test_get_upcoming_appointments(self):
        e1 = Event([self.p1], self.start, "Hey! long time no see!")
        e1.book()

        e2 = Event([self.p1, self.p2], self.conflict_start, "Hey! long time no see!")
        self.assertEqual(e2.suggest_time(), (datetime.fromisoformat("2021-07-09 17:00"), datetime.fromisoformat("2021-07-09 18:00")))



class TestAvailability(unittest.TestCase):
    start = datetime.fromisoformat("2021-07-08 16:00")
    end = datetime.fromisoformat("2021-07-08 17:00")

    def setUp(self):
        self.p1 = Person("Esh", "hi@esh.ph")

    def test_check_availability_shall_be_true(self):
        self.p1.create_appointment((self.start, self.end))
        self.assertTrue(self.p1.check_availability((self.start + timedelta(hours=1), self.end + timedelta(hours=1))))

    def test_check_availability_prev_hour_shall_be_true(self):
        self.p1.create_appointment((self.start, self.end))
        self.assertTrue(self.p1.check_availability((self.start - timedelta(hours=1), self.end - timedelta(hours=1))))

    def test_check_availability_same_date_shall_be_false(self):
        self.p1.create_appointment((self.start, self.end))
        self.assertFalse(self.p1.check_availability((self.start, self.end)))

    def test_check_availability_half_hour_conflict_shall_be_false(self):
        self.p1.create_appointment((self.start, self.end))
        self.assertFalse(self.p1.check_availability((self.start + timedelta(hours=.5), self.end)))

