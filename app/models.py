from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Transaction(db.Model):
    __tablename__ = 'transaction'  # Specify the table name explicitly
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    
class Users(db.Model):
    __tablename__ = 'users'  # Specify the table name explicitly
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String(100), nullable=False)


# def calculate_balance():
#     transactions = Transaction.query.all()
#     balance = 0
#     for transaction in transactions:
#         balance += transaction.amount
#     return balance
def calculate_balance():
    # Calculate the running balance
    balance = 0.0
    for transaction in Transaction.query.order_by(Transaction.date.asc()).all():
        balance += transaction.amount
        # transaction.balance = balance
    return round(balance, 2)