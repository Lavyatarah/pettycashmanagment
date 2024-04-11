# from . import db
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

class Transaction():
    __tablename__ = 'transaction'  # Specify the table name explicitly
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    description = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)
