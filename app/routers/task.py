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

<<<<<<< HEAD


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
=======

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

>>>>>>> f73921be4b1a91f0aa2fd5402693bf8e2acd7b97

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
<<<<<<< HEAD
        raise HTTPException(status_code=404, detail="No users found")

    stock = db.query(models.StockPrice).filter(models.StockPrice.stock_symbol == user.stock_symbol).first()
    if (not stock) or (stock.shares < user.shares):
        raise HTTPException(status_code=400, detail="Stock not available or insufficient shares")
=======
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")

    stock = db.query(models.StockPrice).filter(models.StockPrice.stock_symbol == user.stock_symbol).first()
    if (not stock) or (stock.shares < user.shares):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Stock not available or insufficient shares")
>>>>>>> f73921be4b1a91f0aa2fd5402693bf8e2acd7b97

    reward = models.Reward(
        user_id=user.user_id,
        stock_symbol=user.stock_symbol,
        shares=user.shares,
        reward_ts=date.today(),
        action_taken=user.incentives_for_actions,
<<<<<<< HEAD
        share_price=stock.price_in_inr,
        total_price=user.shares * stock.price_in_inr
    )
=======
        share_price=stock.share_price,
        total_price=user.shares * stock.share_price
    )

    stock.shares -= user.shares

>>>>>>> f73921be4b1a91f0aa2fd5402693bf8e2acd7b97
    db.add(reward)
    db.commit()
    db.refresh(reward)

    ledger_info = addLedger_with_fees(db, reward, stock.price_in_inr)

    stock.shares -= user.shares
    db.add(stock)
    db.commit()
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
        "message": "Reward added successfully with fees",
        "reward_id": reward.id,
<<<<<<< HEAD
        "ledger_id": ledger_info["ledger_id"],
        "shares_rewarded": float(user.shares),
        "inr_value": ledger_info["inr_value"],
        "fees": ledger_info["fees"]
=======
        "shares_rewarded": user.shares
>>>>>>> f73921be4b1a91f0aa2fd5402693bf8e2acd7b97
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
<<<<<<< HEAD
@router.get("/historical-inr/{userId}",status_code=status.HTTP_200_OK)
async def return_all_stock_user_today(db: db_dependency, userId: int):

=======
@router.get("/historical-inr/{userId}")
async def past_record(db: db_dependency, userId: int):
>>>>>>> f73921be4b1a91f0aa2fd5402693bf8e2acd7b97
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
<<<<<<< HEAD
@router.get("/portfolio/{userId}",status_code=status.HTTP_200_OK)
async def return_status(userId:int,db:db_dependency):
    particular_id = db.query(models.Portfolio).filter(models.Portfolio.id == userId).first()
=======
@router.get("/portfolio/{userId}")
async def user_portfolio(userId:int,db:db_dependency):
    particular_id = db.query(models.Portfolio).filter(models.Portfolio.user_id == userId).all()
>>>>>>> f73921be4b1a91f0aa2fd5402693bf8e2acd7b97
    if not particular_id:   
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user found not have any Portfolio")
    return particular_id

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

<<<<<<< HEAD
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

=======
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

>>>>>>> f73921be4b1a91f0aa2fd5402693bf8e2acd7b97
