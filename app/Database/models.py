import datetime
from Database.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Numeric, DateTime, func
from sqlalchemy.orm import relationship

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)   
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    # One-to-many relationship  
    rewards = relationship("Reward", back_populates="user")


class Reward(Base):
    __tablename__ = "rewards"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    stock_symbol = Column(String, index=True, nullable=False)
    shares = Column(Numeric(18, 6), nullable=False)   # FIXED
    reward_ts = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)  # FIXED
    idempotency_key = Column(String, nullable=True)
    created_ts = Column(DateTime, default=datetime.datetime.utcnow, nullable=False) # FIXED

    # Back reference to Users
    user = relationship("Users", back_populates="rewards")


class StockPrice(Base):
    __tablename__ = "stock_prices"   # FIXED to match SQL schema

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
    tx_type = Column(String, nullable=False)     # e.g., 'reward', 'purchase'
    reference_id = Column(Integer, nullable=True)  
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class LedgerEntry(Base):
    __tablename__ = "ledger_entries"

    id = Column(Integer, primary_key=True, index=True)
    tx_id = Column(Integer, ForeignKey("ledger_transactions.id"))
    account = Column(String, nullable=False)      # e.g., 'CASH:BANK', 'ASSET:STOCK:RELIANCE'
    direction = Column(String, nullable=False)    # 'debit' or 'credit'
    amount_in_inr = Column(Numeric(18, 4), nullable=False)
    shares = Column(Numeric(18, 6), nullable=True)
    stock_symbol = Column(String, nullable=True)
