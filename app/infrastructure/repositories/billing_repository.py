# from app.infrastructure.db.models import BillingModel
# from app.domain.entities.billing import Billing
# from app.infrastructure.db.session import SessionLocal
# from sqlalchemy.orm import Session
# import logging

# logger = logging.getLogger(__name__)

# class BillingRepository:
#     def __init__(self, db_session: Session = SessionLocal):
#         self.db = db_session

#     def save(self, billing: BillingModel):
#         try:
#             self.db.add(billing)
#             self.db.commit()
#             self.db.refresh(billing)
#             return billing
#         except Exception as e:
#             self.db.rollback()
#             logger.error(f"Error saving billing: {str(e)}")
#             raise

#     def find_by_id(self, billing_id: str):
#         return self.db.query(BillingModel).filter(BillingModel.id == billing_id).first()

#     def find_by_appointment_id(self, appointment_id: str):
#         return self.db.query(BillingModel).filter(BillingModel.appointment_id == appointment_id).first()

#     def update_payment_status(self, billing_id: str, is_paid: bool):
#         try:
#             billing = self.find_by_id(billing_id)
#             if billing:
#                 billing.is_paid = is_paid
#                 self.db.commit()
#                 return billing
#             return None
#         except Exception as e:
#             self.db.rollback()
#             logger.error(f"Error updating payment status: {str(e)}")
#             raise

#     def get_all(self):
#         return self.db.query(BillingModel).all()
