from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import Field
from sqlalchemy.orm import Session
from typing import Annotated
from Database.database import  SessionLocal
from Database import models


router=APIRouter(
    prefix='/share market'
    ,tags=['share market']
)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.get('/shares',status_code=status.HTTP_200_OK)
async def create_users(db:db_dependency):
        if not db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
        return db.query(models.StockPriceHistory).all()


