from datetime import date
from pydantic import BaseModel


class Payment(BaseModel):
    transaction_id: str
    tenant_id: str
    property_id: str
    amount: float
    date: date
    payment_method: str
    is_successful: bool
    rental_period_start: date
    rental_period_end: date
    rental_unit: str
    comments: str
