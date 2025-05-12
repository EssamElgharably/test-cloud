from enum import Enum

class UserRole(Enum):
    PATIENT = "patient"
    DOCTOR = "doctor"
    STAFF = "staff"

class AppointmentStatus(Enum):
    BOOKED = "booked"
    ATTENDED = "attended"
    MISSED = "missed"
    CANCELED = "canceled"