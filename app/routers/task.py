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
    shares: int


async def add_portfolio_entry(
    db: db_dependency, user_id: int, stock_symbol: str, shares: float,
    average_price: float, current_price: float
):
    total_value = shares * current_price

    portfolio_entry = (
        db.query(models.Portfolio)
        .filter(models.Portfolio.user_id == user_id)
        .filter(models.Portfolio.stock_symbol == stock_symbol)
        .first()
    )

    if portfolio_entry:
        portfolio_entry.shares += shares
        portfolio_entry.average_price = (
            (portfolio_entry.average_price * portfolio_entry.shares) + (average_price * shares)
        ) / (portfolio_entry.shares + shares)  
        portfolio_entry.current_price = current_price
        portfolio_entry.total_value = portfolio_entry.shares * current_price
    else:
            portfolio_entry = models.Portfolio(
            user_id=user_id,
            stock_symbol=stock_symbol,
            shares=shares,
            average_price=average_price,
            current_price=current_price,
            total_value=total_value
        )
    db.add(portfolio_entry)
    db.commit()
    db.refresh(portfolio_entry)
    return portfolio_entry


@router.post("/reward", status_code=status.HTTP_201_CREATED)
async def add_reward(user: Request, db: Session = Depends(get_db)):

    rewarded_user = db.query(models.Users).filter(models.Users.id == user.user_id).first()
    if not rewarded_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")

    stock = db.query(models.StockPrice).filter(models.StockPrice.stock_symbol == user.stock_symbol).first()
    if (not stock) or (stock.shares < user.shares):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Stock not available or insufficient shares")

    reward = models.Reward(
        user_id=user.user_id,
        stock_symbol=user.stock_symbol,
        shares=user.shares,
        reward_ts=date.today(),
        action_taken=user.incentives_for_actions,
        share_price=stock.share_price,
        total_price=user.shares * stock.share_price
    )

    stock.shares -= user.shares

    db.add(reward)
    db.commit()
    db.refresh(reward)
    db.refresh(stock)

    stock_history = (
        db.query(models.StockPriceHistory)
        .filter(models.StockPriceHistory.stock_symbol == user.stock_symbol)
        .order_by(models.StockPriceHistory.captured_at.desc())  
        .first()
    )

    if stock_history:
        await add_portfolio_entry(
            db=db,
            user_id=user.user_id,
            stock_symbol=user.stock_symbol,
            shares=user.shares,
            average_price=float(stock_history.average_price),
            current_price=float(stock_history.current_price)
        )

    return {
        "message": "Reward added successfully",
        "reward_id": reward.id,
        "shares_rewarded": user.shares
    }

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@router.get("/today-stocks/{userId}", status_code=status.HTTP_200_OK)
async def stock_user_today(userId: int, db: db_dependency):
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
async def past_record(db: db_dependency, userId: int):
    results = (
        db.query(models.Reward.stock_symbol, models.Reward.shares, models.Reward.total_price)
        .filter(models.Reward.user_id == userId)
        .filter(models.Reward.reward_ts != date.today())
        .filter(models.Reward.shares > 0)
        .all()
    )
    total_inr = 0
    for record in results:
        total_inr += float(record.total_price)  

    return {"Total Prices in INR": total_inr}

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@router.get("/portfolio/{userId}")
async def user_portfolio(userId:int,db:db_dependency):
    particular_id = db.query(models.Portfolio).filter(models.Portfolio.user_id == userId).all()
    if not particular_id:   
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user found not have any Portfolio")
    return particular_id

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@router.get("/stats/{userId}")
async def shares_reward_today(userId:int,db:db_dependency):
    particular_id = (
        db.query(models.Reward.total_price,models.Reward.stock_symbol,models.Reward.shares)
        .filter(models.Reward.user_id == userId)
        .filter(models.Reward.stock_symbol !=None)
        .filter(models.Reward.shares>0)
        .filter(models.Reward.reward_ts==date.today())
        .all()
        )
    if not particular_id:   
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user not have Rewared")
    
    total={}
    todayProfit=0
    for i in particular_id:

        todayProfit+=i.total_price
        
        if i.stock_symbol in total:
            total[i.stock_symbol] += float(i.total_price)
        else:
            total[i.stock_symbol] = float(i.total_price)

    valueCurrentPrice = db.query(models.Portfolio.current_price).filter(models.Portfolio.user_id == userId).all()
    totalValue=0
    for i in valueCurrentPrice:
        totalValue+=i.current_price

    dateToday=date.today()
    return {
            f"Total Reward Shares on Today {dateToday}{total}",
            f"Total Profit : {todayProfit}",
            f"Current INR Value of Portfolio: {totalValue}"
            }

