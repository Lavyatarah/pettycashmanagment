#!/usr/bin/python3

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from models import Transaction, calculate_balance
import datetime
from models import db
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://lavy:Lavenia1@localhost/pettycash'
app.secret_key = os.getenv('SECRET_KEY')
db.init_app(app)

@app.route('/')
def index():
    transactions = Transaction.query.order_by(Transaction.date.desc()).all()
    balance = calculate_balance()
    return render_template('index.html', transactions=transactions, balance=balance)

@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        date_str = request.form['date']
        
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        description = request.form['description']
        amount = request.form['amount']
        category = request.form['category']

        if not date or not description or not amount or not category:
            return "Error: All fields are required."

        try:
            amount = float(amount)
        except ValueError:
            return "Error: Amount must be a number."

        new_transaction = Transaction(date=date, description=description, amount=amount, category=category)
        db.session.add(new_transaction)

        try:
            db.session.commit()
            flash("Transaction Successfully Created")  # Pass a string message to the flash function
        except Exception as e:
            db.session.rollback()
            return "Error in Adding Transaction: " + str(e)

    return render_template('add_transaction.html')

@app.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword')
    transactions = Transaction.query.filter(Transaction.description.contains(keyword)).all()
    return render_template('index.html', transactions=transactions)

@app.route('/filter', methods=['GET'])
def filter():
    category = request.args.get('category')
    start_date= request.args.get('start_date')
    end_date= request.args.get('end_date')
    balance = calculate_balance()

    query = Transaction.query
    if category:
        query = query.filter_by(category=category)

    if start_date and end_date:
        try:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d') + datetime.timedelta(days=1)
            query = query.filter(Transaction.date >= start_date, Transaction.date < end_date)
        except ValueError:
            return "Error: Invalid date format. Please use YYYY-MM-DD."

    transactions = query.order_by(Transaction.date.desc()).all()
    return render_template('index.html', transactions=transactions, balance=balance)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
