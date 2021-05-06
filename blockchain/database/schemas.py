from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    login: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    balance: float

    class Config:
        orm_mode = True
