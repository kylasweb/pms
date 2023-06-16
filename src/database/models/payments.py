from datetime import datetime
from pydantic import BaseModel


class Payment(BaseModel):
    amount: float
    date: datetime.date
    payment_method: str
