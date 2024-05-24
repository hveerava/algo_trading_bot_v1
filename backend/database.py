from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

DATABASE_URL = "sqlite:///./financial_modeling.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)

class FinancialModel(Base):
    __tablename__ = "financial_models"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    revenue = Column(Float)
    expenses = Column(Float)
    profit = Column(Float)

class TradeHistory(Base):
    __tablename__ = "trade_history"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String)
    quantity = Column(Integer)
    order_type = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)