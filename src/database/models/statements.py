from pydantic import BaseModel
from datetime import date


class Statement(BaseModel):
    statement_number: str
    month: str
    amount: float
    customer_id: str
    items: list[str]
    is_paid: bool
    payment_date: date
    generated_at: date
