from pydantic import BaseModel


class Statement(BaseModel):
    statement_number: str
    month: str
    amount: float
