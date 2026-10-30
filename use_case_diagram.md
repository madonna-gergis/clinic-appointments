# Use Case Diagram — Doctor Appointment Booking System

Drawn from `use_cases.md` (UC1–UC3). Actors are Patient and Doctor. N = 5.

```mermaid
flowchart LR
    P([Patient])
    D([Doctor])

    subgraph System["Doctor Appointment Booking System"]
        UC1["UC1 View doctor availability (R1)"]
        UC2["UC2 Book an appointment (R2, R4: max 5 upcoming)"]
        UC3["UC3 Accept or decline appointment request (R3)"]
    end

    P --- UC1
    P --- UC2
    UC3 --- D
```

- Actors stand outside the system box; use cases are inside it.
- R5–R7 are non-functional, so they are not use cases (see README).
