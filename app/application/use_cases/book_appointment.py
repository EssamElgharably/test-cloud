from app.domain.entities.appointment import Appointment
from app.domain.enums import AppointmentStatus
from datetime import datetime
import uuid

class BookAppointmentUseCase:
    def __init__(self, appointment_repository):
        self.appointment_repository = appointment_repository
        
    def execute(self, patient_id, doctor_id, date_time):
        appointment = Appointment(
            id=str(uuid.uuid4()),
            patient_id=patient_id,
            doctor_id=doctor_id,
            date_time=date_time,
            status=AppointmentStatus.BOOKED.value,
            created_at=datetime.now()  
        )
        
        self.appointment_repository.save(appointment)
        return appointment  