# #!/usr/bin/python3

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import Transaction

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pettycash.db'
db = SQLAlchemy(app)

@app.route('/')
def index():
    """transactions = Transaction.query.order_by(Transaction.date.desc()).all()"""
    return render_template('index.html')

@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        date = request.form['date']
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
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_transaction.html')

@app.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword')
    transactions = Transaction.query.filter(Transaction.description.contains(keyword)).all()
    return render_template('index.html', transactions=transactions)

@app.route('/filter', methods=['GET'])
def filter():
    category = request.args.get('category')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = Transaction.query

    if category:
        query = query.filter_by(category=category)

    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d') + datetime.timedelta(days=1)
            query = query.filter(Transaction.date >= start_date, Transaction.date < end_date)
        except ValueError:
            return "Error: Invalid date format. Please use YYYY-MM-DD."

    transactions = query.order_by(Transaction.date.desc()).all()
    return render_template('index.html', transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True)
