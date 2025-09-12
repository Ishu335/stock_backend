from database import Base
from sqlalchemy import Column, Integer, String, Boolean,ForeignKey,Numeric,DateTime

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

class Reward(Basa):
    __tablename__ = "rewards"
    id = Column(Integer, primary_key=True, index=True)
    user_id=
    stock_symbol =
    shares = Column(String, index=True)
    reward_ts = Column(String, index=True)
    created_ts = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))

class StockPrice(Base):
    __tablename__="stock_price"
    stock_symbol = Column(String, primary_key=True, index=True)
    price_in_inr = Column(Numeric(18, 4), nullable=False)
    updated_at = Column(DateTime, nullable=False)

class StockPriceHistory(Base):
    __tablename__ = "stock_price_history"

    id = Column(Integer, primary_key=True, index=True)
    stock_symbol = Column(String, nullable=False)
    price_in_inr = Column(Numeric(18, 4), nullable=False)
    captured_at = Column(DateTime, nullable=False)

class LedgerTransaction(Base):
    __tablename__ = "ledger_transactions"

    id = Column(Integer, primary_key=True, index=True)
    tx_type = Column(String, nullable=False)     
    reference_id = Column(Integer, nullable=True)  
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class LedgerEntry(Base):
    __tablename__ = "ledger_entries"

    id = Column(Integer, primary_key=True, index=True)
    tx_id = Column(Integer, ForeignKey("ledger_transactions.id"))
    account = Column(String, nullable=False)      
    direction = Column(String, nullable=False)    
    amount_in_inr = Column(Numeric(18, 4), nullable=False)
    shares = Column(Numeric(18, 6), nullable=True)
    stock_symbol = Column(String, nullable=True)
