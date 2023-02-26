import typing as t
from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

engine: Engine = create_engine(
    "sqlite:///./db/db.db", connect_args={"check_same_thread": False}
)

SessionLocal: Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base: declarative_base = declarative_base()