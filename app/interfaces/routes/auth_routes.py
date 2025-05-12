# from flask import Blueprint, request, jsonify
# from app.application.use_cases.register_user import RegisterUserUseCase
# from app.infrastructure.repositories.user_repository import UserRepository
# from app.application.services.auth_service import AuthService
# from app.infrastructure.auth.jwt_handler import JWTHandler
# from app.infrastructure.db.session import SessionLocal
# import re

# auth_bp = Blueprint('auth', __name__)
# user_repo = UserRepository()
# auth_service = AuthService()
# jwt_handler = JWTHandler()

# def is_valid_email(email):
#     # Basic email validation pattern
#     pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
#     return re.match(pattern, email) is not None

# # Register
# @auth_bp.route("/register", methods=["POST"])
# def register():
#     data = request.json
#     try:
#         if not is_valid_email(data.get("email", "")):
#             return jsonify({"error": "Invalid email format"}), 400
            
#         use_case = RegisterUserUseCase(user_repo, auth_service)
#         user = use_case.execute(
#             name=data["name"],
#             email=data["email"],
#             password=data["password"]
#         )
#         return jsonify({"message": "Registration successful! You can now login.", "user_id": user.id}), 201
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400

# # Login
# @auth_bp.route("/login", methods=["POST"])
# def login():
#     try:
#         data = request.json
        
#         # Validate required fields
#         if not data or "email" not in data or "password" not in data:
#             return jsonify({"error": "Email and password are required"}), 400
            
#         # Validate email format
#         if not is_valid_email(data["email"]):
#             return jsonify({"error": "Invalid email format"}), 400

#         # Convert email to lowercase for consistent comparison
#         email = data["email"].lower()

#         # Get user from database
#         with SessionLocal() as db_session:
#             user_repo.db = db_session
#             user = user_repo.find_by_email(email)
            
#             # Check if user exists
#             if not user:
#                 return jsonify({"error": "No account found with this email"}), 401
                
#             # Verify password
#             if not auth_service.verify_password(data["password"], user.hashed_password):
#                 return jsonify({"error": "Incorrect password"}), 401

#             # Create token
#             token = jwt_handler.create_token(user.id, user.role.value)
#             return jsonify({
#                 "access_token": token,
#                 "role": user.role.value,
#                 "user_id": user.id,
#                 "message": "Login successful"
#             }), 200
            
#     except Exception as e:
#         return jsonify({"error": f"Login failed: {str(e)}"}), 500

# # Get User Info
# @auth_bp.route("/user", methods=["GET"])
# def get_user_info():
#     token = request.headers.get('Authorization')
#     if not token:
#         return jsonify({'error': 'Token is missing'}), 401
    
#     try:
#         token = token.split('Bearer ')[1]
#         payload = jwt_handler.decode_token(token)
#         user = user_repo.find_by_id(payload['sub'])
        
#         if not user:
#             return jsonify({'error': 'User not found'}), 404
            
#         return jsonify({
#             'id': user.id,
#             'name': user.name,
#             'email': user.email,
#             'role': user.role.value
#         }), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 401
