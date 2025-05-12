# from flask import Blueprint, jsonify, request
# from app.infrastructure.repositories.user_repository import UserRepository
# from app.domain.enums import UserRole
# from app.infrastructure.auth.jwt_handler import JWTHandler
# from functools import wraps

# doctor_bp = Blueprint('doctors', __name__)
# user_repo = UserRepository()
# jwt_handler = JWTHandler()

# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = request.headers.get('Authorization')
#         if not token:
#             return jsonify({'error': 'Token is missing'}), 401
        
#         try:
#             token = token.split('Bearer ')[1]
#             jwt_handler.decode_token(token)
#         except Exception as e:
#             return jsonify({'error': 'Invalid token'}), 401
        
#         return f(*args, **kwargs)
#     return decorated

# @doctor_bp.route('', methods=['GET'])
# @token_required
# def get_doctors():
#     specialization = request.args.get('specialization')
#     if not specialization:
#         return jsonify({'error': 'Specialization is required'}), 400
        
#     doctors = user_repo.find_doctors_by_specialization(specialization)
#     return jsonify([{
#         'id': doctor.id,
#         'name': doctor.name,
#         'specialization': doctor.specialization
#     } for doctor in doctors]), 200 