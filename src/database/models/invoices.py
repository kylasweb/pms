from pydantic import BaseModel, Field
from datetime import date, datetime
from src.database.tools import create_invoice_number


class Customer(BaseModel):
    customer_id: str
    name: str
    email: str
    tel: str


class InvoicedItems(BaseModel):
    description: str
    multiplier: int
    amount: int

    @property
    def sub_total(self) -> int:
        return self.amount * self.multiplier


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
    service_name: str
    description: str
    currency: str
    customer: Customer
    discount: int = Field(default=0)
    tax_rate: int = Field(default=15)
    date_issued: date
    due_date: date
    items: list[InvoicedItems]

    @property
    def total_amount(self) -> int:
        return sum(item.sub_total for item in self.items)

    @property
    def total_taxes(self) -> int:
        return int(self.total_amount * (self.tax_rate / 100))

    @property
    def amount_payable(self) -> int:
        return self.total_amount - self.discount - self.total_taxes

    @property
    def days_remaining(self) -> int:
        today = datetime.now().date()
        return (self.due_date - today).days

    @property
    def notes(self) -> str:
        _notes = f"""
        <strong>Thank you for your business!</strong> Payment is expected within {self.days_remaining} days;
        please process this invoice within that time.
        There will be a 5% interest charge per month on late invoices.
        """
        return _notes
