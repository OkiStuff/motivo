import typing as t
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import engine, Base
from .models import task, user
from .routers import tasks, users

Base.metadata.create_all(bind=engine)

app: FastAPI = FastAPI(title="Motivo API")
app.include_router(tasks.router)
app.include_router(users.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

@app.get("/")
def root() -> t.Dict:
    return {
        "description": "root"
    }