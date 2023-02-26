import typing as t
from fastapi import APIRouter, Depends, HTTPException
from ..database import SessionLocal, engine
from sqlalchemy.orm import Session
from ..models import user
from ..models.update_fields import UpdateFieldModel
from ..dependency import get_db
import hashlib

router: APIRouter = APIRouter(
    prefix="/users"
)

@router.get("/")
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> t.Dict:
    users: t.Dict = {}
    
    for user_object in user.query_all_users(db, skip, limit):
        users.update({
            user_object.id: {
                "username": user_object.username,
                "streak": user_object.streak,
                "streak_min": user_object.streak_min,
            }
        })
    
    return {"users": users}

@router.post("/new")
def new_user(user_data: user.UserModel, db: Session = Depends(get_db)) -> t.Dict:
    if user.query_user_by_email(db, user_data.email):
        raise HTTPException(400, "Email already registered")
    
    if user.query_user_by_username(db, user_data.username):
        raise HTTPException(400, "Username already registered")
    
    new_user_data: user.User = user.create_user(db, user_data)
    return {
            "user": {
                "id": new_user_data.id,
                "username": new_user_data.username,
                "email": new_user_data.email,
                "streak": new_user_data.streak,
                "streak_min": new_user_data.streak_min,
                "amount_completed": new_user_data.amount_completed,
                "gems": new_user_data.gems,
                "tasks": new_user_data.tasks
        }
    }

@router.put("/{user_id}/update")
def update_user_fields(user_id: int, updatefield: UpdateFieldModel, db: Session = Depends(get_db)) -> t.Dict:
    user_data: user.User = user.query_user_by_id(db, user_id)
    
    if user_data == None:
        raise HTTPException(404, f"User with id {user_id} could not be found")
    
    if updatefield.field == "email":
        user.update_user_value(db, user_id, {'email': updatefield.value})
    
    elif updatefield.field == "username":
        user.update_user_value(db, user_id, {'username': updatefield.value})
    
    elif updatefield.field == "salt":
        user.update_user_value(db, user_id, {'salt': updatefield.value})
        
    elif updatefield.field == "hashed_password":
        user.update_user_value(db, user_id, {'hashed_password': updatefield.value})
    
    elif updatefield.field == "streak":
        user.update_user_value(db, user_id, {'streak': updatefield.value})
    
    elif updatefield.field == "streak_min":
        user.update_user_value(db, user_id, {'streak_min': updatefield.value})
    
    elif updatefield.field == "amount_completed":
        user.update_user_value(db, user_id, {'amount_completed': updatefield.value})
    
    elif updatefield.field == "gems":
        user.update_user_value(db, user_id, {'gems': updatefield.value})
    
    else:
        raise HTTPException(404, f"Unknown Field '{field}'")
    
    return {"success": True}

@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)) -> t.Dict:
    user_data: user.User = user.query_user_by_id(db, user_id)
    
    if user_data == None:
        return HTTPException(404, f"User with id {user_id} could not be found")
    
    return {
        "user": {
            "id": user_data.id,
            "username": user_data.username,
            "email": user_data.email,
            "streak": user_data.streak,
            "gems": user_data.gems,
            "streak_min": user_data.streak_min,
            "amount_completed": user_data.amount_completed,
            "tasks": user_data.tasks
        }
    }

@router.get("/query-email/{email}")
def get_user_by_email(email: str, db: Session = Depends(get_db)) -> t.Dict:
    user_data: user.User = user.query_user_by_email(db, email)
    
    if user_data == None:
        raise HTTPException(404, f"User with email {email} could not be found")
    
    return {
        "user": {
            "id": user_data.id,
            "username": user_data.username,
            "email": user_data.email,
            "streak": user_data.streak,
            "gems": user_data.gems,
            "streak_min": user_data.streak_min,
            "amount_completed": user_data.amount_completed,
            "tasks": user_data.tasks
        }
    }

@router.get("/query-username/{username}")
def get_user_by_username(username: str, db: Session = Depends(get_db)) -> t.Dict:
    user_data: user.User = user.query_user_by_username(db, username)
    
    if user_data == None:
        raise HTTPException(404, f"User with username {username} could not be found")
    
    return {
        "user": {
            "id": user_data.id,
            "username": user_data.username,
            "email": user_data.email,
            "streak": user_data.streak,
            "gems": user_data.gems,
            "streak_min": user_data.streak_min,
            "amount_completed": user_data.amount_completed,
            "tasks": user_data.tasks
        }
    }

@router.post("/auth")
def auth_user(auth_data: user.UserAuthModel, db: Session = Depends(get_db)) -> t.Dict:
    user_data: user.User = user.query_user_by_email(db, auth_data.email)
    
    if user_data == None:
        raise HTTPException(404, f"User with email {auth_data.email} could not be found")
    
    key: bytes = hashlib.pbkdf2_hmac('sha256', auth_data.password.encode('utf-8'), user_data.salt, 100000)
    
    if user_data.hashed_password == key:
        return {
            "user": {
                "id": user_data.id,
                "username": user_data.username,
                "email": user_data.email,
                "streak": user_data.streak,
                "streak_min": user_data.streak_min,
                "amount_completed": user_data.amount_completed,
                "gems": user_data.gems,
                "tasks": user_data.tasks
            }
        }
    
    return {
        "error": "Incorrect username or password"
    }