import unittest
from datetime import date, datetime, time, timedelta

from main import N, AppointmentStatus, AvailabilitySlot, Doctor, Patient


def make_slots(doctor, day, count):
    doctor.slots = [AvailabilitySlot(f"S{i}", doctor, day, time(8, i), time(9, i)) for i in range(count)]
    return doctor.slots


class BookingTests(unittest.TestCase):
    def setUp(self):
        self.doctor = Doctor("D1", "Dr. Hany")
        self.patient = Patient("P1", "Sara")
        self.slots = make_slots(self.doctor, date.today() + timedelta(days=1), N + 2)

    def test_booked_slot_is_pending_and_no_longer_available(self):
        a = self.patient.requestAppointment(self.slots[0])
        self.assertEqual(a.status, AppointmentStatus.Pending)
        self.assertNotIn(self.slots[0], self.patient.viewDoctorAvailability(self.doctor))
        with self.assertRaises(ValueError):
            Patient("P2", "Omar").requestAppointment(self.slots[0])

    def test_limit_n(self):
        for s in self.slots[:N]:
            self.patient.requestAppointment(s)
        with self.assertRaises(ValueError):
            self.patient.requestAppointment(self.slots[N])

    def test_declined_does_not_count_and_frees_slot(self):
        booked = [self.patient.requestAppointment(s) for s in self.slots[:N]]
        self.doctor.declineAppointment(booked[0])
        self.assertTrue(self.slots[0].isAvailable())
        self.patient.requestAppointment(self.slots[N])  # no error

    def test_past_appointments_do_not_count(self):
        for s in self.slots[:N]:
            self.patient.requestAppointment(s)
        day_after = datetime.combine(date.today() + timedelta(days=2), time(0))
        self.assertEqual(self.patient.countUpcomingActiveAppointments(day_after), 0)

    def test_only_own_doctor_can_decide_and_only_once(self):
        a = self.patient.requestAppointment(self.slots[0])
        with self.assertRaises(PermissionError):
            Doctor("D2", "Dr. Mona").acceptAppointment(a)
        self.doctor.acceptAppointment(a)
        with self.assertRaises(ValueError):
            self.doctor.declineAppointment(a)


if __name__ == "__main__":
    unittest.main()
