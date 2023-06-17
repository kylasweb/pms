from datetime import date
from pydantic import BaseModel


class Payment(BaseModel):
    amount: float
    date: date
    payment_method: str
    transaction_id: str
    is_successful: bool
    property_id: str
    tenant_id: str
    rental_period_start: date
    rental_period_end: date
    rental_unit: str
    comments: str
