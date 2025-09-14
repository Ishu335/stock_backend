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
    
@router.put('/create_user',status_code=status.HTTP_201_CREATED)
async def create_users(db:db_dependency,user_request:CreateUserRequest):
    existing_user = db.query(models.Users).filter(models.Users.email == user_request.email).first()
    if existing_user:       
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    new_user = models.Users(
        name=user_request.name,
        email=user_request.email,
        password=user_request.password,  
        created_at=datetime.now()
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)   

    return {
        "message": "User created successfully",
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email
        }
    }

