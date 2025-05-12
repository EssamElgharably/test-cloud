# from flask import Blueprint, request, jsonify
# from app.application.use_cases.book_appointment import BookAppointmentUseCase
# from app.infrastructure.repositories.appointment_repository import AppointmentRepository
# from app.infrastructure.repositories.user_repository import UserRepository
# from app.infrastructure.repositories.billing_repository import BillingRepository
# from app.domain.entities.appointment import Appointment
# from app.infrastructure.auth.jwt_handler import JWTHandler
# from app.domain.enums import AppointmentStatus
# from datetime import datetime
# from app.infrastructure.db.session import SessionLocal
# from app.infrastructure.db.models import BillingModel
# import uuid
# from functools import wraps
# from random import uniform, randint

# import jwt

# appointment_bp = Blueprint('appointments', __name__)
# appointment_repo = AppointmentRepository()
# user_repo = UserRepository()
# billing_repo = BillingRepository()
# jwt_handler = JWTHandler()

# # Helper to extract user from token
# def get_user_from_token():
#     token = request.headers.get("Authorization", "").replace("Bearer ", "")
#     if not token:
#         return None
#     try:
#         return jwt_handler.decode_token(token)
#     except Exception as e:
#         return None

# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = request.headers.get('Authorization')
#         if not token:
#             return jsonify({'error': 'Token is missing'}), 401
        
#         try:
#             token = token.split('Bearer ')[1]
#             payload = jwt_handler.decode_token(token)
#             request.user_id = payload['sub']  # Store user_id in request
#         except Exception as e:
#             return jsonify({'error': 'Invalid token'}), 401
        
#         return f(*args, **kwargs)
#     return decorated

# # Book Appointment - Patient
# @appointment_bp.route("/book", methods=["POST"])
# def book_appointment():
#     user = get_user_from_token()
#     if not user or user["role"] != "patient":
#         return jsonify({"error": "Unauthorized"}), 403

#     data = request.json
#     use_case = BookAppointmentUseCase(appointment_repo)
#     try:
#         appointment = use_case.execute(
#             patient_id=user["sub"],
#             doctor_id=data["doctor_id"],
#             date_time=data["date_time"]
#         )
#         return jsonify({"message": "Appointment booked", "appointment_id": appointment.id}), 201
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400

# # View All Appointments - Doctor/Staff
# @appointment_bp.route("/", methods=["GET"])
# def get_appointments():
#     user = get_user_from_token()
#     if not user or user["role"] not in ["doctor", "staff"]:
#         return jsonify({"error": "Unauthorized"}), 403

#     appointments = appointment_repo.get_all()
#     result = []
    
#     for a in appointments:
#         patient = user_repo.find_by_id(a.patient_id)
#         doctor = user_repo.find_by_id(a.doctor_id)
        
#         # Get billing info if appointment is attended
#         billing_info = None
#         if a.status == AppointmentStatus.ATTENDED:
#             billing = billing_repo.find_by_appointment_id(a.id)
#             if billing:
#                 billing_info = {
#                     "id": billing.id,
#                     "amount": billing.amount,
#                     "is_paid": billing.is_paid
#                 }
        
#         result.append({
#             "id": a.id,
#             "patient_id": a.patient_id,
#             "patient_name": patient.name if patient else "Unknown Patient",
#             "doctor_id": a.doctor_id,
#             "doctor_name": doctor.name if doctor else "Unknown Doctor",
#             "date_time": a.date_time.isoformat(),
#             "status": a.status.value if a.status else None,
#             "created_at": a.created_at.isoformat(),
#             "billing": billing_info
#         })
#     return jsonify(result), 200

# # Update Status - Doctor/Staff
# @appointment_bp.route("/<appointment_id>/status", methods=["PUT"])
# @token_required
# def update_status(appointment_id):
#     user = get_user_from_token()
#     if not user or user["role"] not in ["doctor", "staff"]:
#         return jsonify({"error": "Unauthorized"}), 403

#     try:
#         data = request.json
#         new_status = data.get("status")
        
#         # Convert status string to enum
#         try:
#             new_status_enum = AppointmentStatus[new_status]
#         except KeyError:
#             return jsonify({"error": "Invalid status value"}), 400

#         # Get the appointment
#         appointment = appointment_repo.find_by_id(appointment_id)
#         if not appointment:
#             return jsonify({"error": "Appointment not found"}), 404

#         # Update the appointment status
#         appointment.status = new_status_enum
#         appointment_repo.save(appointment)
        
#         return jsonify({
#             "message": f"Appointment status updated to {new_status}",
#             "status": new_status
#         }), 200
        
#     except Exception as e:
#         print(f"Error updating appointment status: {str(e)}")  # Add logging
#         return jsonify({"error": str(e)}), 500

# @appointment_bp.route('', methods=['POST'])
# @token_required
# def create_appointment():
#     data = request.json
#     user_id = request.user_id  # Get user_id from token
#     db = SessionLocal()

#     try:
#         # Validate doctor exists
#         doctor = user_repo.find_by_id(data['doctor_id'])
#         if not doctor:
#             return jsonify({'error': 'Doctor not found'}), 404

#         # Parse and validate date_time
#         try:
#             date_time = datetime.fromisoformat(data['date_time'].replace('Z', '+00:00'))
#         except ValueError:
#             return jsonify({'error': 'Invalid date format'}), 400

#         # Create appointment
#         appointment = Appointment(
#             id=str(uuid.uuid4()),
#             patient_id=user_id,
#             doctor_id=data['doctor_id'],
#             date_time=date_time,
#             created_at=datetime.now(),
#             status=AppointmentStatus.BOOKED
#         )

#         # Save appointment
#         appointment_repo.save(appointment)
        
#         # Create billing record with random integer amount between 40-60
#         amount = randint(40, 60)
        
#         # Create billing record in database
#         billing = BillingModel(
#             id=str(uuid.uuid4()),
#             appointment_id=appointment.id,
#             amount=amount,
#             is_paid=False,
#             created_at=datetime.now()
#         )
#         billing_repo.save(billing)
        
#         return jsonify({
#             'message': 'Appointment booked successfully',
#             'appointment_id': appointment.id,
#             'billing_amount': amount
#         }), 201

#     except Exception as e:
#         db.rollback()
#         return jsonify({'error': str(e)}), 400
#     finally:
#         db.close()

# @appointment_bp.route('', methods=['GET'])
# @token_required
# def get_patient_appointments():
#     user_id = request.user_id
#     appointments = appointment_repo.find_by_patient_id(user_id)
    
#     return jsonify([{
#         'id': apt.id,
#         'doctor_id': apt.doctor_id,
#         'date_time': apt.date_time.isoformat(),
#         'status': apt.status.value if apt.status else None,
#         'created_at': apt.created_at.isoformat()
#     } for apt in appointments]), 200

# # Get Doctor's Appointments
# @appointment_bp.route('/doctor', methods=['GET'])
# @token_required
# def get_doctor_appointments():
#     user_id = request.user_id
    
#     # Verify user is a doctor
#     doctor = user_repo.find_by_id(user_id)
#     if not doctor or doctor.role.value != 'doctor':
#         return jsonify({'error': 'Unauthorized'}), 403
    
#     appointments = appointment_repo.find_by_doctor_id(user_id)
    
#     # Get patient information for each appointment
#     result = []
#     for apt in appointments:
#         patient = user_repo.find_by_id(apt.patient_id)
#         result.append({
#             'id': apt.id,
#             'patient_id': apt.patient_id,
#             'patient_name': patient.name if patient else 'Unknown Patient',
#             'date_time': apt.date_time.isoformat(),
#             'status': apt.status.value if apt.status else None,
#             'created_at': apt.created_at.isoformat()
#         })
    
#     return jsonify(result), 200

# # Update Appointment Time - Doctor
# @appointment_bp.route("/<appointment_id>/time", methods=["PUT"])
# @token_required
# def update_appointment_time(appointment_id):
#     user_id = request.user_id
    
#     # Verify user is a doctor or staff
#     user = user_repo.find_by_id(user_id)
#     if not user or user.role.value not in ['doctor', 'staff']:
#         return jsonify({'error': 'Unauthorized'}), 403
    
#     try:
#         data = request.json
#         new_date_time = datetime.fromisoformat(data['date_time'].replace('Z', '+00:00'))
        
#         # Get the appointment
#         appointment = appointment_repo.find_by_id(appointment_id)
#         if not appointment:
#             return jsonify({'error': 'Appointment not found'}), 404
            
#         # If user is a doctor, verify this is their appointment
#         if user.role.value == 'doctor' and appointment.doctor_id != user_id:
#             return jsonify({'error': 'Unauthorized'}), 403
            
#         # Verify appointment is still in BOOKED status
#         if appointment.status != AppointmentStatus.BOOKED:
#             return jsonify({'error': 'Can only modify BOOKED appointments'}), 400
        
#         # Update appointment time
#         appointment.date_time = new_date_time
#         appointment_repo.save(appointment)
        
#         return jsonify({
#             'message': 'Appointment time updated successfully',
#             'new_date_time': new_date_time.isoformat()
#         }), 200
        
#     except ValueError:
#         return jsonify({'error': 'Invalid date format'}), 400
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
