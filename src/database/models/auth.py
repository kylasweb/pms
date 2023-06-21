

from pydantic import BaseModel, Field


class Auth(BaseModel):
    username: str
    password: str
    remember: str


class RegisterUser(BaseModel):
    username: str
    email: str
    password: str
    terms: str
