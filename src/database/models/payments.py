from datetime import date
from pydantic import BaseModel, Field

from src.database.tools import create_transaction_id


class Payment(BaseModel):
    transaction_id: str = Field(default_factory=create_transaction_id, description="Transaction ID")
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
