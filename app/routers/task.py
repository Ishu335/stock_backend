from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from pydantic import Field,BaseModel
from sqlalchemy.orm import Session
from typing import Annotated
from Database.database import  SessionLocal
from Database import models
from datetime import date

router=APIRouter(
    prefix='/Task'
    ,tags=['Task']
)   
# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class Request(BaseModel):
    user_id: int
    stock_symbol: str
    incentives_for_actions: str
    shares:int

async def add_portfolio_entry(db:db_dependency, user_id: int, stock_symbol: str, shares: float, average_price: float, current_price: float):
    # Calculate total value
    total_value = shares * current_price

    # Create Portfolio object
    new_portfolio = models.Portfolio(
        user_id=user_id,
        stock_symbol=stock_symbol,
        shares=shares,
        average_price=average_price,
        current_price=current_price,
        total_value=total_value
    )
    db.add(new_portfolio)
    db.commit()
    db.refresh(new_portfolio)
    return "added"

@router.post("/reward", status_code=status.HTTP_201_CREATED)
async def add_reward(user: Request, db: Session = Depends(get_db)):

    # Check if user exists
    rewarded_user = db.query(models.Users).filter(models.Users.id == user.user_id).first()
    if not rewarded_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
    
    particular_id = db.query(models.Portfolio)
    stockHistory = (
                db.query(models.StockPriceHistory)
                .filter(models.StockPriceHistory.current_price>0)
                .filter(models.StockPriceHistory.average_price>0)
                .filter(models.StockPriceHistory.shares>0)
                .filter(models.StockPriceHistory.stock_symbol==user.stock_symbol)
                )
    
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ",stockHistory ,"<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ",particular_id ,"<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    stock = db.query(models.StockPrice).filter(models.StockPrice.stock_symbol == user.stock_symbol).first()
    if (not stock) or (stock.shares < user.shares):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Stock not available or insufficient shares")
    
    # add_portfolio_entry(user.user_id,user.stock_symbol,user.shares,models.StockPriceHistory.average_price,models.StockPriceHistory.current_price)

    # Create reward without total_price (generated column)
    reward = models.Reward(
        user_id=user.user_id,
        stock_symbol=user.stock_symbol,
        shares=user.shares,
        reward_ts=date.today(),
        action_taken=user.incentives_for_actions,
        share_price=stock.share_price, # keep this
        total_price=user.shares*stock.share_price
    )

    # Deduct shares from stock
    stock.shares -= user.shares

    # Save to DB
    db.add(reward)
    db.commit()
    db.refresh(reward)
    db.refresh(stock)

    return {
        "message": "Reward added successfully",
        "reward_id": reward.id,
        "shares_rewarded": float(user.shares)
    }
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@router.get("/today-stocks/{userId}", status_code=status.HTTP_200_OK)
async def return_all_stock_user_today(userId: int, db: db_dependency):
    particular_id = db.query(models.Users).filter(models.Users.id == userId).first()
    if not particular_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user found")

    results = (
        db.query(models.Reward.stock_symbol, models.Reward.shares)
        .filter(models.Reward.user_id == userId)
        .filter(models.Reward.reward_ts == date.today())
        .filter(models.Reward.shares > 0)   
        .all()
    )

    todaysStock = [{"stock_symbol": r.stock_symbol, "shares": r.shares} for r in results]

    if not todaysStock:
        return {"message": "No stocks found for today", "stocks": []}

    return {"stocks": todaysStock}


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@router.get("/historical-inr/{userId}")
async def return_all_stock_user_today(db: db_dependency, userId: int):
    # Include total_price in the query
    results = (
        db.query(models.Reward.stock_symbol, models.Reward.shares, models.Reward.total_price)
        .filter(models.Reward.user_id == userId)
        .filter(models.Reward.reward_ts != date.today())
        .filter(models.Reward.shares > 0)
        .all()
    )
    total_inr = 0
    for record in results:
        total_inr += float(record.total_price)  # Now this works

    return {"Total Prices in INR": total_inr}

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@router.get("/portfolio/{userId}")
async def return_status(userId:int,db:db_dependency):
    particular_id = db.query(models.Portfolio).filter(models.Portfolio.id == userId).first()
    if not particular_id:   
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user found not have any Portfolio")
    return particular_id

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# @app.get("/stats/{userId}")
# async def return_status():
#     return {"message": "- Total shares rewarded today (grouped by stock symbol)."
#     "- Current INR value of the user's portfolio. "}




# @app.get("/stats/{userId}")
# async def return_status(userId:int,db:db_dependency):
#     particular_id = (
#         db.query(models.Portfolio.shares,models.Portfolio.)
#         .filter(models.Portfolio.user_id == userId).first()
#         )
#     if not particular_id:   
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user found not have any Portfolio")

#     return {"message": "- Total shares rewarded today (grouped by stock symbol)."
#     "- Current INR value of the user's portfolio. "}

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, nullable=False)
#     stock_symbol = Column(String, nullable=False)
#     shares = Column(Numeric, nullable=False)
#     average_price = Column(Numeric(18, 2))
#     current_price = Column(Numeric(18, 2))
#     total_value = Column(Numeric(18, 2))  # Optional: can compute manually
#     last_updated = Column(DateTime, default=date.today())