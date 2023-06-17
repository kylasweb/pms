import uuid
from pydantic import BaseModel, Field
from enum import Enum


class UserType(str, Enum):
    ADMIN = 'admin'
    TENANT = 'tenant'


class User(BaseModel):
    """
    Represents the details of a user.

    Attributes:
    - user_id (str): The ID of the user.
    - company_id (str): The ID of the company associated with the user.
    - is_tenant (bool): Indicates if the user is a tenant.
    - tenant_id (str): The ID of the tenant associated with the user.
    - user_type (UserType): The type of user.
    - username (str): The username of the user.
    - password (str | None): The password of the user.
    - email (str): The email address of the user.
    - full_name (str): The full name of the user.
    - contact_number (str): The contact number of the user.
    """
    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    company_id: str
    is_tenant: bool
    tenant_id: str
    user_type: UserType
    username: str
    password: str = None
    email: str
    full_name: str
    contact_number: str
