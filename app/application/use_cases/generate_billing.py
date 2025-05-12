from app.domain.entities.billing import Billing
from datetime import datetime
import uuid

class GenerateBillingUseCase:
    def __init__(self, billing_repository):
        self.billing_repository = billing_repository


    def execute(self, appointment_id, amount, created_by):
        billing = Billing(
            id=str(uuid.uuid4()),
            appointment_id=appointment_id,
            amount=amount,
            is_paid=False,
            created_by=created_by,
            created_at=datetime.now()
        )

        self.billing_repository.save(billing)
        return billing