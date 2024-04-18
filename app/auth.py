from flask import Blueprint, redirect, url_for, request, flash, render_template
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db, Transaction

auth = Blueprint('auth', __name__)

def calculate_balance():
    transactions = Transaction.query.all()
    balance = sum(transaction.amount for transaction in transactions)
    return round(balance, 2)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        return redirect(url_for('auth.transactions'))

    return render_template('login.html')

# @auth.route('/signup', methods=['GET','POST'])
# def signup():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         name = request.form.get('name')
#         password = request.form.get('password')
        
#         user = User.query.filter_by(email=email).first()
#         if user:
#             flash('Email address already exists')
#             # return render_template('login.html')
#             return redirect(url_for('auth.signup'))

#         new_user = User(email=email, username=name, password=generate_password_hash(password, method='pbkdf2:sha256'))
#         db.session.add(new_user)
#         db.session.commit()
#         flash('Account created successfully! Please log in.')
#         return redirect(url_for('auth.login'))  # Redirect to login after successful signup

#     return render_template('signup.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))

        new_user = User(email=email, username=name, password=generate_password_hash(password, method='pbkdf2:sha256'))
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! Please log in.')
        return redirect(url_for('auth.login'))  # Redirect to login after successful signup

    return render_template('signup.html')

@auth.route('/transactions')
@login_required
def transactions():
    transactions = Transaction.query.order_by(Transaction.date.desc()).all()
    balance = calculate_balance()
    return render_template('transactions.html', transactions=transactions, balance=balance)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
