# from flask import Blueprint, request, jsonify
# from app.application.use_cases.generate_billing import GenerateBillingUseCase
# from app.infrastructure.repositories.billing_repository import BillingRepository
# from app.infrastructure.repositories.appointment_repository import AppointmentRepository
# from app.infrastructure.auth.jwt_handler import JWTHandler
# from app.infrastructure.repositories.user_repository import UserRepository

# billing_bp = Blueprint('billing', __name__)
# billing_repo = BillingRepository()
# appointment_repo = AppointmentRepository()
# user_repo = UserRepository()
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

# # Generate Billing - Staff
# @billing_bp.route("/generate", methods=["POST"])
# def generate_billing():
#     user = get_user_from_token()
#     if not user or user["role"] != "staff":
#         return jsonify({"error": "Unauthorized"}), 403

#     data = request.json
#     appointment = appointment_repo.find_by_id(data["appointment_id"])
#     if not appointment:
#         return jsonify({"error": "Appointment not found"}), 404

#     use_case = GenerateBillingUseCase(billing_repo)
#     try:
#         billing = use_case.execute(
#             appointment_id=data["appointment_id"],
#             amount=data["amount"],
#             created_by=user["sub"]
#         )
#         return jsonify({"message": "Billing generated", "billing_id": billing.id, "amount": billing.amount}), 201
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400

# # View Billing - Staff/Doctor
# @billing_bp.route("/<billing_id>", methods=["GET"])
# def get_billing(billing_id):
#     user = get_user_from_token()
#     if not user or user["role"] not in ["doctor", "staff"]:
#         return jsonify({"error": "Unauthorized"}), 403

#     billing = billing_repo.find_by_id(billing_id)
#     if not billing:
#         return jsonify({"error": "Billing not found"}), 404

#     result = {
#         "id": billing.id,
#         "appointment_id": billing.appointment_id,
#         "amount": billing.amount,
#         "is_paid": billing.is_paid,
#         "created_by": billing.created_by,
#         "created_at": billing.created_at.isoformat()
#     }
#     return jsonify(result), 200

# @billing_bp.route("/<billing_id>/pay", methods=["PUT"])
# def update_payment_status(billing_id):
#     user = get_user_from_token()
#     if not user or user["role"] != "staff":
#         return jsonify({"error": "Unauthorized"}), 403

#     try:
#         billing = billing_repo.find_by_id(billing_id)
#         if not billing:
#             return jsonify({"error": "Billing record not found"}), 404

#         billing_repo.update_payment_status(billing_id, True)
#         return jsonify({"message": "Payment status updated successfully"}), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
