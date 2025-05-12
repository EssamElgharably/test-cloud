# from app.infrastructure.db.models import AppointmentModel
# from app.domain.entities.appointment import Appointment
# from app.infrastructure.db.session import SessionLocal
# from sqlalchemy.orm import Session
# from app.domain.enums import AppointmentStatus
# import logging

# logger = logging.getLogger(__name__)

# class AppointmentRepository:
#     def __init__(self, db_session: Session = SessionLocal):
#         self.db = db_session

#     def save(self, appointment: Appointment):
#         try:
#             if isinstance(appointment, AppointmentModel):
#                 # If it's already a model instance, just save it
#                 self.db.add(appointment)
#                 self.db.commit()
#                 self.db.refresh(appointment)
#                 return appointment
                
#             # Check if appointment already exists
#             existing = self.find_by_id(appointment.id)
#             if existing:
#                 # Update existing appointment
#                 existing.patient_id = appointment.patient_id
#                 existing.doctor_id = appointment.doctor_id
#                 existing.date_time = appointment.date_time
#                 existing.status = appointment.status
#                 existing.created_at = appointment.created_at
#                 self.db.commit()
#                 self.db.refresh(existing)
#                 return existing
            
#             # Create new appointment
#             db_appointment = AppointmentModel(
#                 id=appointment.id,
#                 patient_id=appointment.patient_id,
#                 doctor_id=appointment.doctor_id,
#                 date_time=appointment.date_time,
#                 status=appointment.status,
#                 created_at=appointment.created_at
#             )
#             self.db.add(db_appointment)
#             self.db.commit()
#             self.db.refresh(db_appointment)
#             return db_appointment
#         except Exception as e:
#             self.db.rollback()
#             logger.error(f"Error saving appointment: {str(e)}")
#             raise

#     def find_by_id(self, appointment_id: str):
#         return self.db.query(AppointmentModel).filter(AppointmentModel.id == appointment_id).first()

#     def get_all(self):
#         return self.db.query(AppointmentModel).all()

#     def find_by_patient_id(self, patient_id: str):
#         try:
#             return self.db.query(AppointmentModel).filter(AppointmentModel.patient_id == patient_id).all()
#         except Exception as e:
#             logger.error(f"Error finding appointments by patient ID: {str(e)}")
#             raise

#     def find_by_doctor_id(self, doctor_id: str):
#         try:
#             return self.db.query(AppointmentModel).filter(AppointmentModel.doctor_id == doctor_id).all()
#         except Exception as e:
#             logger.error(f"Error finding appointments by doctor ID: {str(e)}")
#             raise
