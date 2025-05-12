class Billing:
    def __init__(self, id: str, appointment_id: str, amount: int, is_paid: bool, created_at):
        self.id = id
        self.appointment_id = appointment_id
        self.amount = amount
        self.is_paid = is_paid
        self.created_at = created_at