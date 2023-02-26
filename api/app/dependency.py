import typing as t
from .database import SessionLocal

def get_db():
    db: SessionLocal = SessionLocal()
    try:
        yield db
    finally:
        db.close()