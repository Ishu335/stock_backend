from fastapi import APIRouter, Depends, HTTPException, status, Path, Body
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Annotated
from Database.database import  SessionLocal
from Database import models
from datetime import datetime


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

class CreateUserRequest(BaseModel):
    name: str=Field(description="Dexter Morgen")
    email: str=Field(description="adc@gmail.com")
    password: str=Field(description="Pass@123")
    


@router.put('/create_user',status_code=status.HTTP_204_NO_CONTENT)
async def create_users(db:db_dependency,created_user:CreateUserRequest):
    users = db.query(models.Users).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
    created_user=models.Users(
                                    name=created_user.name,
                                    email=created_user.email,
                                    password=created_user.password,
                                    is_active=True,
                                    created_at=datetime.now()
                            )
    db.add(created_user)
    db.commit()
    return "Done"

