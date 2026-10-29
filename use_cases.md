# Use Cases - Doctor Appointment Booking System

## 1. UC1: View Doctor Availability
- **Actor:** Patient
- **Description:** The patient views the available days and times when a doctor is free for consultation.
- **Trigger:** Patient opens the appointment scheduling interface.
- **Main Flow:**
  1. System displays a list of doctors and their available dates/time slots.
  2. Patient selects a preferred date and time.
- **Related Requirement:** R1[cite: 8]

## 2. UC2: Book an Appointment
- **Actor:** Patient
- **Description:** The patient books an appointment during an available time slot, provided they haven't exceeded the limit $N = 5$[cite: 8].
- **Trigger:** Patient chooses an available time slot and requests booking.
- **Main Flow:**
  1. Patient selects an open time slot.
  2. System checks the patient's active upcoming appointments (Pending + Accepted) against the limit $N = 5$[cite: 8].
  3. If under the limit, the system creates the appointment with a "Pending" status.
  4. System confirms the booking request to the patient.
- **Alternative Flow:**
  - If active upcoming appointments reach $N = 5$, the system rejects the booking request[cite: 8].
- **Related Requirement:** R2, R4[cite: 8]

## 3. UC3: Accept or Decline Appointment Request
- **Actor:** Doctor
- **Description:** The doctor reviews pending appointment requests and decides to either accept or decline them.
- **Trigger:** Doctor views the list of pending patient appointment requests.
- **Main Flow:**
  1. Doctor selects a pending appointment request.
  2. Doctor chooses to either Accept or Decline the request.
  3. System updates the appointment status accordingly (Accepted or Declined)[cite: 8].
- **Related Requirement:** R3[cite: 8]