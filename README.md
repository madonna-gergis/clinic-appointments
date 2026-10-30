# Clinic Appointments Project

## Team Members
| ID | Name | Branch | PR Link |
|---|---|---|---|
| 20242251 | Madonna Gerges | madonna-gergis-patch-1 | [#1](https://github.com/madonna-gergis/clinic-appointments/pull/1) |
| 20240061 | Ahmed Yasser | sequence-diagram, implementation, readme-and-use-case-diagram | [#3](https://github.com/madonna-gergis/clinic-appointments/pull/3), [#4](https://github.com/madonna-gergis/clinic-appointments/pull/4), [#5](https://github.com/madonna-gergis/clinic-appointments/pull/5) |
| 20240123 | Bishoy Robert | beshoy | [#2](https://github.com/madonna-gergis/clinic-appointments/pull/2) |
| 20240096 | Andrew Wael | - | - (PR review) |

## Configuration
- N = 5

## Conflict Drill
Conflict Drill: Madonna Gerges, Ahmed Yasser, Bishoy Robert, Andrew Wael


## Stages
| Student ID | Full name | Assigned task | Branch | PR link |
|---|---|---|---|---|
| 20242251 | Madonna Gerges | Use Cases | main | committed to main |
| 20240123 | Bishoy Robert | Class Diagram | beshoy | [#2](https://github.com/madonna-gergis/clinic-appointments/pull/2) |
| 20240061 | Ahmed Yasser | Sequence Diagram | sequence-diagram | [#3](https://github.com/madonna-gergis/clinic-appointments/pull/3) |
| 20240061 | Ahmed Yasser | Implementation (took over from Andrew Wael) | implementation | [#4](https://github.com/madonna-gergis/clinic-appointments/pull/4) |
| 20240061 | Ahmed Yasser | Use Case Diagram + README links | readme-and-use-case-diagram | [#5](https://github.com/madonna-gergis/clinic-appointments/pull/5) |

## How to run
Requires Python 3 (standard library only, nothing to install).

```bash
python main.py              # demo of UC1-UC3
python -m unittest -v       # unit tests (test_main.py)
```

`main.py` follows `class_diagram.md` and `sequence_diagram.md`: same classes and method names. The demo shows a patient booking 5 slots (N = 5), the 6th being rejected, a taken slot being rejected, the doctor accepting/declining, and a declined appointment freeing a place.

## Non-functional requirements (R5-R7)
- **R5 Authorized access:** the console app stores no medical data. A real system would put patient records behind login + role checks (doctor/staff only). The code already refuses a doctor deciding on another doctor's appointment (`PermissionError`).
- **R6 Within 2 seconds:** `getAvailableSlots()` is an in-memory filter over one doctor's slots, which runs in microseconds. With a database: index slots by doctor and date.
- **R7 Mobile screens:** console output is short single lines. A web version would use a responsive layout (viewport meta tag, single-column CSS).
