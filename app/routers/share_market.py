from fastapi import APIRouter, Depends, HTTPException, status
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


@router.get('/shares/current share',status_code=status.HTTP_200_OK)
async def current_share(db:db_dependency):
        if not db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
        return db.query(models.StockPrice).all()

@router.get('/shares',status_code=status.HTTP_200_OK)
<<<<<<< HEAD
async def all_share(db:db_dependency):
=======
async def share_Market(db:db_dependency):
>>>>>>> f73921be4b1a91f0aa2fd5402693bf8e2acd7b97
        if not db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
        return db.query(models.StockPriceHistory).all()



