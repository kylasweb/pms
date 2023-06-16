from pydantic import BaseModel


class Invoice(BaseModel):
    invoice_number: str
    month: str
    amount: float
