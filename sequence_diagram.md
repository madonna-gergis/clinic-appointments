# Sequence Diagram — Book an Appointment

Built from `class_diagram.md` (Stage 2) and `use_cases.md` UC1–UC3. Every message below is a method that exists in the class diagram. N = 5.

## Mermaid Sequence Diagram

```mermaid
sequenceDiagram
    actor P as Patient
    participant D as Doctor
    participant S as AvailabilitySlot
    participant A as Appointment

    Note over P,D: UC1 — View doctor availability (R1)
    P->>P: viewDoctorAvailability(doctor)
    P->>D: getAvailableSlots()
    loop each offered slot
        D->>S: isAvailable()
        S-->>D: true / false
    end
    D-->>P: List of available slots

    Note over P,A: UC2 — Book an appointment (R2, R4)
    P->>P: requestAppointment(slot)
    P->>S: isAvailable()
    S-->>P: true / false
    alt slot is not available
        P-->>P: rejected: "slot not available"
    else slot is available
        P->>P: countUpcomingActiveAppointments(now)
        loop each of the patient's appointments
            P->>A: countsTowardLimit(now)
            A-->>P: true if future and Pending/Accepted
        end
        alt count >= N (5)
            P-->>P: rejected: "limit of 5 upcoming appointments reached"
        else count < N
            P->>A: new Appointment(patient, slot) status = Pending
            A-->>P: appointment (Pending)
        end
    end

    Note over D,A: UC3 — Accept or decline request (R3)
    D->>D: viewPendingRequests()
    alt doctor accepts
        D->>D: acceptAppointment(appointment)
        D->>A: accept()
        A-->>D: status = Accepted
    else doctor declines
        D->>D: declineAppointment(appointment)
        D->>A: decline()
        A-->>D: status = Declined (slot becomes available again)
    end
```

## What we checked against the class diagram

| Message in the sequence | Class diagram method |
| --- | --- |
| `viewDoctorAvailability(doctor)` | `Patient.viewDoctorAvailability(doctor)` |
| `getAvailableSlots()` | `Doctor.getAvailableSlots()` |
| `isAvailable()` | `AvailabilitySlot.isAvailable()` |
| `requestAppointment(slot)` | `Patient.requestAppointment(slot)` |
| `countUpcomingActiveAppointments(now)` | `Patient.countUpcomingActiveAppointments(now)` |
| `countsTowardLimit(now)` | `Appointment.countsTowardLimit(now)` |
| `viewPendingRequests()` | `Doctor.viewPendingRequests()` |
| `acceptAppointment` / `declineAppointment` | `Doctor.acceptAppointment(appointment)` / `Doctor.declineAppointment(appointment)` |
| `accept()` / `decline()` | `Appointment.accept()` / `Appointment.decline()` |

- The slot is checked **before** the N limit, and the limit is checked **before** the appointment is created (order matters).
- Both rejection branches (`slot not available`, `limit reached`) are shown with `alt / else`, plus the accept / decline branch for the doctor.
- Answers are dashed arrows (`-->>`) going back to the caller.
