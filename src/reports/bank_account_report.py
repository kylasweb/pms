from pydantic import BaseModel, Field, Extra


class BankAccountPrintParser(BaseModel):
    account_holder: str
    account_number: str
    bank_name: str
    branch: str
    account_type: str

    class Config:
        extra = Extra.ignore

    def to_dict(self):
        return {
            "Account Holder": self.account_holder,
            "Account Number": self.account_number,
            "Bank Name": self.bank_name,
            "Branch": self.branch,
            "Account Type": self.account_type
        }
