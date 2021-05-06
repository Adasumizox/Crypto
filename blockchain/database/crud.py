from decimal import Decimal

import bcrypt
from sqlalchemy.orm import Session

import blockchain.database.models as models
import blockchain.database.schema as schema


def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id)


def get_user_by_login(db: Session, login: str):
    return db.query(models.User).filter(models.User.login == login)


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schema.User):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(user.password, salt)
    db_user = models.User(email=user.email, login=user.login, hashed_password=hashed, salt=salt, balance=Decimal(0))
    db.commit(db_user)
    db.refresh(db_user)
    return db_user
