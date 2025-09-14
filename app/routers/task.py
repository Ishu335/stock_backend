from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from Database.database import  SessionLocal
from Database import models
from datetime import date
from sqlalchemy import func
from typing import Annotated

router=APIRouter(
    prefix='/Task'
    ,tags=['Task']
)   

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



def addLedger_with_fees(db: Session, reward: models.Reward, stock_price: float):
    inr_value = float(reward.shares) * float(stock_price)

    
    brokerage = inr_value * 0.01     # 1% brokerage
    stt = inr_value * 0.001          # 0.1% STT
    gst = brokerage * 0.18           # 18% GST on brokerage
    total_fees = brokerage + stt + gst

    
    ledger_tx = models.LedgerTransaction(
        tx_type="reward",
        reference_id=reward.id,
        created_at=date.today()
    )
    db.add(ledger_tx)
    db.flush()  

    
    debit_entry = models.LedgerEntry(
        tx_id=ledger_tx.id,
        account="EXPENSE:REWARDS(1% br0+0.1% STT,18% GST)",
        direction="debit",
        amount_in_inr=inr_value,
        shares=reward.shares,
        stock_symbol=reward.stock_symbol
    )

    credit_entry = models.LedgerEntry(
        tx_id=ledger_tx.id,
        account=f"ASSET:STOCK:{reward.stock_symbol}",
        direction="credit",
        amount_in_inr=inr_value,
        shares=reward.shares,
        stock_symbol=reward.stock_symbol
    )

    
    fees_debit = models.LedgerEntry(
        tx_id=ledger_tx.id,
        account="EXPENSE:FEES(GTS)",
        direction="debit",
        amount_in_inr=total_fees
    )

    
    fees_credit = models.LedgerEntry(
        tx_id=ledger_tx.id,
        account="CASH:BANK",
        direction="credit",
        amount_in_inr=total_fees
    )

    db.add_all([debit_entry, credit_entry, fees_debit, fees_credit])
    db.commit()
    db.refresh(ledger_tx)

    return {
        "ledger_id": ledger_tx.id,
        "inr_value": inr_value,
        "fees": {
            "brokerage": brokerage,
            "stt": stt,
            "gst": gst,
            "total_fees": total_fees
        }
    }



@router.post("/", status_code=status.HTTP_201_CREATED)
def add_reward(user: Request, db: Session = Depends(get_db)):

    rewarded_user = db.query(models.Users).filter(models.Users.id == user.user_id).first()
    if not rewarded_user:
        raise HTTPException(status_code=404, detail="No users found")

    stock = db.query(models.StockPrice).filter(models.StockPrice.stock_symbol == user.stock_symbol).first()
    if (not stock) or (stock.shares < user.shares):
        raise HTTPException(status_code=400, detail="Stock not available or insufficient shares")

    reward = models.Reward(
        user_id=user.user_id,
        stock_symbol=user.stock_symbol,
        shares=user.shares,
        reward_ts=date.today(),
        action_taken=user.incentives_for_actions,
        share_price=stock.price_in_inr,
        total_price=user.shares * stock.price_in_inr
    )
    db.add(reward)
    db.commit()
    db.refresh(reward)

    ledger_info = addLedger_with_fees(db, reward, stock.price_in_inr)

    stock.shares -= user.shares
    db.add(stock)
    db.commit()
    db.refresh(stock)

    return {
        "message": "Reward added successfully with fees",
        "reward_id": reward.id,
        "ledger_id": ledger_info["ledger_id"],
        "shares_rewarded": float(user.shares),
        "inr_value": ledger_info["inr_value"],
        "fees": ledger_info["fees"]
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
@router.get("/historical-inr/{userId}",status_code=status.HTTP_200_OK)
async def return_all_stock_user_today(db: db_dependency, userId: int):

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
@router.get("/portfolio/{userId}",status_code=status.HTTP_200_OK)
async def return_status(userId:int,db:db_dependency):
    particular_id = db.query(models.Portfolio).filter(models.Portfolio.id == userId).first()
    if not particular_id:   
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user found not have any Portfolio")
    return particular_id

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

from sqlalchemy import func  

@router.get("/stats/{userId}")
async def return_status(userId: int, db: Session = Depends(get_db)):
   
    portfolios = (
        db.query(models.Portfolio)
        .filter(models.Portfolio.user_id == userId)
        .all()
    )

    if not portfolios:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user does not have any Portfolio"
        )

    results = (
        db.query(models.Reward.stock_symbol, models.Reward.shares)
        .filter(models.Reward.user_id == userId)
        .filter(models.Reward.reward_ts == date.today())
        .filter(models.Reward.shares > 0)   
        .all()
    )
    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user has not been rewarded today"
        )

    
    shares_grouped = (
        db.query(
            models.Portfolio.stock_symbol,
            func.sum(models.Portfolio.shares).label("total_shares")
        )
        .filter(models.Portfolio.user_id == userId)
        .group_by(models.Portfolio.stock_symbol)
        .all()
    )

    shares_summary = {row.stock_symbol: float(row.total_shares) for row in shares_grouped}

    total_portfolio_value = sum(float(p.total_value) for p in portfolios)

    todays_rewards = [
        {"stock_symbol": r.stock_symbol, "shares": float(r.shares)} for r in results
    ]

    return {
        "user_id": userId,
        "todays_rewards": todays_rewards,
        "shares_by_stock": shares_summary,
        "total_portfolio_value_in_inr": total_portfolio_value,
    }

