import typing as t
from fastapi import APIRouter, Depends, HTTPException
from ..database import SessionLocal, engine
from sqlalchemy.orm import Session
from ..models import task
from ..dependency import get_db

router: APIRouter = APIRouter(
	prefix="/tasks"
)

@router.post("/new")
def new_task(task_data: task.TaskModel, db: Session = Depends(get_db)) -> t.Dict:
	return task.task_to_dict(task.create_task(db, task_data))

@router.get("/{task_id}")
def get_task_by_id(task_id: int, db: Session = Depends(get_db)) -> t.Dict:
	task_data: task.Task = task.query_task_by_id(db, task_id)
	
	if task_data == None:
		raise HTTPException(404, f"Task with id {task_id} could not be found")
	
	return task.task_to_dict(task_data)

@router.get("/delete/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)) -> t.Dict:
	task_data: task.Task = task.query_task_by_id(db, task_id)
	
	if task_data == None:
		raise HTTPException(404, f"Task with id {task_id} could not be found")
	
	db.delete(task_data)
	db.commit()
	
	return task.task_to_dict(task_data)

@router.get("/complete/{task_id}")
def complete_task(task_id: int, db: Session = Depends(get_db)) -> t.Dict:
	task_data: task.Task = task.query_task_by_id(db, task_id)
	
	if task_data == None:
		raise HTTPException(404, f"Task with id {task_id} could not be found")
	
	db.query(task.Task).filter(task.Task.id == task_id).update({'completed': True})
	db.commit()
	
	return task.task_to_dict(task_data)

@router.get("/reset/{task_id}")
def reet_task(task_id: int, db: Session = Depends(get_db)) -> t.Dict:
	task_data: tas.Task = task.query_task_by_id(db, task_id)
	
	if task_data == None:
		raise HTTPException(404, f"Task with id {task_id} could not be found")
	
	db.query(task.Task).filter(task.Task.id == task_id).update({'completed': False})
	db.refresh(task_data)
	
	return task.task_to_dict(task_data)