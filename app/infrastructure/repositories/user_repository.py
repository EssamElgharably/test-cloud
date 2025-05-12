# from app.infrastructure.db.models import UserModel
# from app.domain.entities.user import User
# from app.infrastructure.db.session import get_db
# from sqlalchemy.orm import Session
# from app.domain.enums import UserRole
# import logging

# logger = logging.getLogger(__name__)

# class UserRepository:
#     def __init__(self, db_session: Session = None):
#         self.db = db_session or get_db()

#     def save(self, user: User):
#         try:
#             db_user = UserModel(
#                 id=user.id,
#                 name=user.name,
#                 email=user.email,
#                 hashed_password=user.hashed_password,
#                 role=user.role,
#                 specialization=user.specialization,
#                 created_at=user.created_at
#             )
#             self.db.add(db_user)
#             self.db.commit()
#             self.db.refresh(db_user)
#             logger.info(f"User saved successfully: {user.email}")
#             return db_user
#         except Exception as e:
#             self.db.rollback()
#             logger.error(f"Error saving user: {str(e)}")
#             raise

#     def find_by_email(self, email: str):
#         try:
#             logger.debug(f"Looking up user by email: {email}")
#             user = self.db.query(UserModel).filter(UserModel.email == email).first()
#             if user:
#                 logger.debug(f"Found user: {user.email}")
#             else:
#                 logger.debug(f"No user found with email: {email}")
#             return user
#         except Exception as e:
#             logger.error(f"Error finding user by email: {str(e)}")
#             raise

#     def find_by_id(self, user_id: str):
#         try:
#             logger.debug(f"Looking up user by ID: {user_id}")
#             return self.db.query(UserModel).filter(UserModel.id == user_id).first()
#         except Exception as e:
#             logger.error(f"Error finding user by ID: {str(e)}")
#             raise

#     def find_doctors_by_specialization(self, specialization: str):
#         try:
#             logger.debug(f"Looking up doctors with specialization: {specialization}")
#             doctors = self.db.query(UserModel).filter(
#                 UserModel.role == UserRole.DOCTOR,
#                 UserModel.specialization == specialization
#             ).all()
#             logger.debug(f"Found {len(doctors)} doctors")
#             return doctors
#         except Exception as e:
#             logger.error(f"Error finding doctors by specialization: {str(e)}")
#             raise
