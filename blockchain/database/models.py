from sqlalchemy import Column, Integer, String, Float
from blockchain.database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    login = Column(String, unique=True)
    password = Column(String)
    balance = Column(Float)