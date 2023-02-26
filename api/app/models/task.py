import typing as t
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Session
from ..database import Base
from pydantic import BaseModel

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    short_description = Column(String)
    long_description = Column(String)
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="tasks")

class TaskModel(BaseModel):
    short_description: str
    long_description: str
    owner_id: int

def create_task(db: Session, task: TaskModel) -> Task:
    db_task: Task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def query_task_by_id(db: Session, task_id: int) -> Task:
    return db.query(Task).filter(Task.id == task_id).first()

def task_to_dict(task: Task) -> t.Dict:
    return {
        "task": {
            "id": task.id,
            "short_description": task.short_description,
            "long_description": task.long_description,
            "completed": task.completed,
            "owner_id": task.owner_id
        } 
    }

def update_task_value(db: Session, task_id: int, updated: t.Dict) -> None:
    db.query(Task).filter(Task.id == task_id).update(updated)
    db.commit()