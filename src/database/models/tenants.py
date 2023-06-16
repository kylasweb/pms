from pydantic import BaseModel


class Tenant(BaseModel):
    name: str
    tenant_id: str
    email: str
