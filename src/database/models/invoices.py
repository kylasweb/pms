from pydantic import BaseModel, Field
from datetime import date

from src.database.tools import create_invoice_number


class Invoice(BaseModel):
    """
    Represents an invoice.

    Attributes:
    - invoice_number (str): The invoice number.
    - tenant_id (str): The ID of the tenant associated with the invoice.
    - month (str): The month of the invoice.
    - amount (float): The amount of the invoice.
    - due_date (date): The due date of the invoice.
    - items (list[str]): A list of items included in the invoice.
    """

    invoice_number: str = Field(default_factory=create_invoice_number,
                                description="The invoice number.")
    tenant_id: str
    month: str
    amount: float
    due_date: date
    items: list[str]
