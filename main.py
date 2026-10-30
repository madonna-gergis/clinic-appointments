"""Doctor Appointment Booking System - built from class_diagram.md and sequence_diagram.md.

Run: python main.py   (Python 3, standard library only)
"""
from datetime import date, datetime, time, timedelta
from enum import Enum

N = 5  # R4: max upcoming (future Pending + Accepted) appointments per patient


class AppointmentStatus(Enum):
    Pending = "Pending"
    Accepted = "Accepted"
    Declined = "Declined"
    Cancelled = "Cancelled"


ACTIVE = (AppointmentStatus.Pending, AppointmentStatus.Accepted)


class AvailabilitySlot:
    def __init__(self, slotId, doctor, date, startTime, endTime):
        self.slotId = slotId
        self.doctor = doctor
        self.date = date
        self.startTime = startTime
        self.endTime = endTime
        self.appointments = []  # history; only one may be active at a time

    def start(self):
        return datetime.combine(self.date, self.startTime)

    def isAvailable(self):
        return not any(a.status in ACTIVE for a in self.appointments)

    def __str__(self):
        return f"{self.slotId} {self.date} {self.startTime:%H:%M}-{self.endTime:%H:%M}"


class Appointment:
    _next_id = 1

    def __init__(self, patient, slot):
        self.appointmentId = f"A{Appointment._next_id}"
        Appointment._next_id += 1
        self.requestedAt = datetime.now()
        self.status = AppointmentStatus.Pending
        self.patient = patient
        self.slot = slot
        self.doctor = slot.doctor

    def accept(self):
        if self.status != AppointmentStatus.Pending:
            raise ValueError(f"{self.appointmentId} is {self.status.value}, not Pending")
        self.status = AppointmentStatus.Accepted

    def decline(self):
        if self.status != AppointmentStatus.Pending:
            raise ValueError(f"{self.appointmentId} is {self.status.value}, not Pending")
        self.status = AppointmentStatus.Declined

    def countsTowardLimit(self, now):
        return self.status in ACTIVE and self.slot.start() > now


class Doctor:
    def __init__(self, doctorId, name):
        self.doctorId = doctorId
        self.name = name
        self.slots = []
        self.appointments = []

    def getAvailableSlots(self):
        return [s for s in self.slots if s.isAvailable()]

    def viewPendingRequests(self):
        return [a for a in self.appointments if a.status == AppointmentStatus.Pending]

    def acceptAppointment(self, appointment):
        self._checkOwner(appointment)
        appointment.accept()

    def declineAppointment(self, appointment):
        self._checkOwner(appointment)
        appointment.decline()

    def _checkOwner(self, appointment):
        if appointment.doctor is not self:
            raise PermissionError(f"{self.name} is not the doctor of {appointment.appointmentId}")


class Patient:
    def __init__(self, patientId, name):
        self.patientId = patientId
        self.name = name
        self.appointments = []

    def viewDoctorAvailability(self, doctor):
        return doctor.getAvailableSlots()

    def countUpcomingActiveAppointments(self, now):
        return sum(1 for a in self.appointments if a.countsTowardLimit(now))

    def requestAppointment(self, slot, now=None):
        now = now or datetime.now()
        if not slot.isAvailable():
            raise ValueError(f"slot {slot.slotId} not available")
        if self.countUpcomingActiveAppointments(now) >= N:
            raise ValueError(f"limit of {N} upcoming appointments reached")
        appointment = Appointment(self, slot)
        self.appointments.append(appointment)
        slot.appointments.append(appointment)
        slot.doctor.appointments.append(appointment)
        return appointment


def book(patient, slot):
    try:
        a = patient.requestAppointment(slot)
        print(f"  {patient.name} books {slot} -> {a.appointmentId} {a.status.value}")
        return a
    except ValueError as e:
        print(f"  {patient.name} books {slot} -> REJECTED ({e})")


def main():
    doctor = Doctor("D1", "Dr. Hany")
    other = Doctor("D2", "Dr. Mona")
    tomorrow = date.today() + timedelta(days=1)
    slots = [AvailabilitySlot(f"S{i}", doctor, tomorrow, time(8 + i), time(9 + i)) for i in range(1, 8)]
    doctor.slots = slots
    sara = Patient("P1", "Sara")
    omar = Patient("P2", "Omar")

    print(f"N = {N}")
    print("UC1 - available slots of", doctor.name)
    for s in sara.viewDoctorAvailability(doctor):
        print("  ", s)

    print("UC2 - booking")
    booked = [book(sara, s) for s in slots[:N]]
    book(sara, slots[N])          # 6th upcoming -> rejected by R4
    book(omar, slots[0])          # slot already taken -> rejected

    print("UC3 - doctor decisions")
    print("  pending:", [a.appointmentId for a in doctor.viewPendingRequests()])
    doctor.acceptAppointment(booked[0])
    doctor.declineAppointment(booked[1])
    print(f"  {booked[0].appointmentId} {booked[0].status.value}, {booked[1].appointmentId} {booked[1].status.value}")
    try:
        other.acceptAppointment(booked[2])
    except PermissionError as e:
        print("  REJECTED:", e)

    print("After decline: Sara has", sara.countUpcomingActiveAppointments(datetime.now()), "upcoming")
    book(sara, slots[N])          # declined one freed a place -> now allowed
    book(omar, slots[1])          # declined slot is available again


if __name__ == "__main__":
    main()
