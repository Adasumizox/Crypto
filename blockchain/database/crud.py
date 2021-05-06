from decimal import Decimal

import bcrypt
from sqlalchemy.orm import Session

from blockchain.database import models
from blockchain.database import schemas


def get_user(db: Session, user_id: int):
    """

    :param db: Database session
    :param user_id: id of user that we want to fetch
    :return: model of user
    """
    return db.query(models.User).filter(models.User.id == user_id)


def get_user_by_login(db: Session, login: str):
    """

    :param db: Database session
    :param login: login of user that we want to fetch
    :return: model of user
    """
    return db.query(models.User).filter(models.User.login == login)


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """

    :param db: Database session
    :param skip: Offset of users that we want to skip
    :param limit: Number of users that we want to fetch
    :return: model of user
    """
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    """

    :param db: Database session
    :param user: Model of user
    :return: Created user
    """
    #Not implemented yet
    hashed_password = user.password
    db_user = models.User(email=user.email, login=user.login, password=hashed_password, balance=float(0))
    db.commit()
    db.refresh(db_user)
    return db_user
