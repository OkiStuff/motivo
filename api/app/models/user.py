import typing as t
from sqlalchemy import Column, Boolean, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship, Session
from ..database import Base
from pydantic import BaseModel
import os
import hashlib

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    ntfy_topic = Column(String, unique=True)
    salt = Column(String)
    hashed_password = Column(String)
    streak = Column(Integer, default=0)
    streak_min = Column(Float, default=0.8)
    amount_completed = Column(Float)
    gems = Column(Integer, default=0)
    
    tasks = relationship("Task", back_populates="owner")

class UserModel(BaseModel):
    email: str
    username: str
    password: str
    streak_min: float
    
    class Config:
        json_encorders = {bytes: lambda bs: bs.hex()}

class UserAuthModel(BaseModel):
    email: str
    password: str

def query_user_by_id(db: Session, id: int) -> User:
    return db.query(User).filter(User.id == id).first()

def query_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

def query_user_by_username(db: Session, username: str) -> User:
    return db.query(User).filter(User.username == username).first()

def query_all_users(db: Session, skip: int = 0, limit: int = 100) -> t.List[User]:
    return db.query(User).offset(skip).limit(limit).all()

def update_user_value(db: Session, user_id: int, updated: t.Dict) -> None:
    db.query(User).filter(User.id == user_id).update(updated)
    db.commit()

def create_user(db: Session, user: UserModel) -> User:
    salt: bytes = os.urandom(32)
    key: bytes = hashlib.pbkdf2_hmac('sha256', user.password.encode('utf-8'), salt, 100000)
    db_user: User = User(email=user.email, hashed_password=key, salt=salt, streak_min=user.streak_min, username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user