from fastapi import APIRouter


from fastapi import APIRouter, Depends, HTTPException, status, Path, Body
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Annotated
from ..Database.database import  SessionLocal
from Database import models
from .auth  import get_current_user
from models import Todos
from passlib.context import CryptContext

router=APIRouter(
    prefix='/user'
    ,tags=['user']
)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]

@router.get('/all_users')
async def users(db:db_dependency):
    users = db.query(models.Users).all()
    return users