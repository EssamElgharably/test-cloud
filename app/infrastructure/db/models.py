from sqlalchemy import Column, String, DateTime, Enum, Boolean, Float, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from app.domain.enums import AppointmentStatus, UserRole

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    specialization = Column(String, nullable=True)  # For doctors
    created_at = Column(DateTime, default=datetime.now)

class AppointmentModel(Base):
    __tablename__ = "appointments"
    id = Column(String, primary_key=True)
    patient_id = Column(String, ForeignKey("users.id"))
    doctor_id = Column(String, ForeignKey("users.id"))
    date_time = Column(DateTime, nullable=False)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.BOOKED)
    created_at = Column(DateTime, default=datetime.now)

class BillingModel(Base):
    __tablename__ = "billings"
    id = Column(String, primary_key=True)
    appointment_id = Column(String, ForeignKey("appointments.id"))
    amount = Column(Integer)
    is_paid = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
