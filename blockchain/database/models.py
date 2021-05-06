from pydantic import BaseModel
from decimal import Decimal


class UserBase(BaseModel):
    email: str
    login: str
    balance: Decimal


class UserCreate(UserBase):
    password: str
    salt: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True