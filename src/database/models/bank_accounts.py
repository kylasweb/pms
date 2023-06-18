from pydantic import BaseModel, Field
from typing import List


class BankTransaction(BaseModel):
    description: str
    amount: float


class BusinessBankAccount(BaseModel):
    account_number: str = Field(..., description="The unique identification number assigned to the account")
    account_name: str = Field(..., description="The name associated with the account")
    bank_name: str = Field(..., description="The name of the bank where the account is held")
    bank_branch: str = Field(..., description="The specific branch of the bank where the account is held")
    account_type: str = Field(..., description="The type of account, such as checking or savings")
    balance: int = Field(0, ge=0, description="The current balance in the account")
    transactions: List[BankTransaction] = Field([], description="List of transactions associated with the account")
    statement_period: str = Field("", description="The time period covered by the bank statement")
    overdraft_protection: bool = Field(False, description="Indicates whether the account has overdraft protection")
    overdraft_limit: int = Field(0, ge=0,
                                   description="The maximum amount that can be overdrafted from the account")
    interest_rate: float = Field(0.0, ge=0.0, description="The interest rate earned on the account balance")
    account_manager: str = Field("",
                                 description="The designated account manager responsible for overseeing the account")

    class Config:
        schema_extra = {
            "example": {
                "account_number": "123456789",
                "account_name": "ABC Rentals",
                "bank_name": "Example Bank",
                "bank_branch": "Main Branch",
                "account_type": "Checking",
                "balance": 100000,
                "transactions": [
                    {
                        "description": "Rent Payment in Cents",
                        "amount": 50000
                    },
                    {
                        "description": "Maintenance Expense in Cents",
                        "amount": -10000
                    }
                ],
                "statement_period": "2023-06",
                "overdraft_protection": False,
                "overdraft_limit": 0,
                "interest_rate": 0.25,
                "account_manager": "John Smith"
            }
        }
