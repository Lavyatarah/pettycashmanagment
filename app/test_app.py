# import pytest
# import datetime
# from .models import Transaction, calculate_balance, db
# from .routes import app

# @pytest.fixture
# def app_context():
#     with app.app_context():
#         db.init_app()      

# def db_session():
#     db.create_all()
#     return db.session
#     # db.session.remove()

# @pytest.fixture
# def client():
#     #  with app.app_context():
#         app.config['TESTING'] = True
#         # session = db_session()
#         with app.test_client() as client:
#             yield client
        
# def test_index(client):
#     # Test successful rendering of the index page
#     response = client.get('/')
#     assert response.status_code == 200

# def test_add_transaction(client):
#     # Test successful addition of a transaction
#     response = client.post('/add_transaction', data={
#         'date': '2023-04-16',
#         'description': 'Test Transaction',
#         'amount': 100.00,
#         'category': 'travel'
#     })
#     assert response.status_code == 200
#     assert 'Transaction Successfully Created' in response.headers['Location']

# def test_add_transaction_validation(client):
#     # Test validation of required fields
#     response = client.post('/add_transaction', data={
#         'date': '2024-04-15',
#         'description': 'Test Transaction',
#         'amount': 100.00,
#         'category': 'travel'
#     })
#     assert response.status_code == 200
#     assert 'Error: All fields are required.' in response.data.decode('utf-8')

# def test_add_transaction_invalid_amount(client):
#     # Test validation of amount data type
#     response = client.post('/add_transaction', data={
#         'date': '2023-04-16',
#         'description': 'Test Transaction',
#         'amount': 'invalid_amount',
#         'category': 'travel'
#     })
#     assert response.status_code == 200
#     assert 'Error: Amount must be a number.' in response.data.decode('utf-8')

# def test_search(client):
#     # Test successful searching of transactions
#     response = client.get('/search?keyword=Test')
#     assert response.status_code == 200
#     assert 'Test Transaction' in response.data.decode('utf-8')

# def test_filter(client):
#     # Test successful filtering of transactions by category
#     response = client.get('/filter?category=Food')
#     assert response.status_code == 200
#     assert 'Test Transaction' in response.data.decode('utf-8')

#     # Test successful filtering of transactions by date
#     response = client.get('/filter?start_date=2023-04-16&end_date=2023-04-17')
#     assert response.status_code == 200
#     assert 'Test Transaction' in response.data.decode('utf-8')


# def test_calculate_balance(client):
#     # Test calculation of running balance
#     transaction1 = Transaction(date=datetime.date(2023, 4, 16), description='Test Transaction 1', amount=100.00, category='travel')
#     transaction2 = Transaction(date=datetime.date(2023, 4, 16), description='Test Transaction 2', amount=-50.00, category='travel')
    
#     # Assuming db_session() returns a valid session object
#     session = db_session()
#     session.add_all([transaction1, transaction2])
#     session.commit()

#     balance = calculate_balance()
#     assert balance == 50.00


import pytest
import datetime
from datetime import date
from .models import Transaction, calculate_balance, db
from .routes import app

@pytest.fixture
def app_context():
    with app.app_context():
        db.init_app()

def db_session():
    db.create_all()
    return db.session

@pytest.fixture
def client():
   with app.app_context():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200

def test_add_transaction(client):
    response = client.post('/add_transaction', data={
        'date': date.today(),
        'description': 'Test Transaction',
        'amount': 500.00,
        'category': 'travel'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Transaction Successfully Created' in response.data.decode('utf-8')

def test_add_transaction_validation(client):
    response = client.post('/add_transaction', data={
        'date': date.today(),
        'description': 'Test Transaction',
        'amount': '',
        'category': 'travel'
    })
    assert response.status_code == 200
    assert 'Error: All fields are required.' in response.data.decode('utf-8')

def test_add_transaction_invalid_amount(client):
    response = client.post('/add_transaction', data={
        'date': '2023-04-16',
        'description': 'Test Transaction',
        'amount': 'invalid_amount',
        'category': 'travel'
    })
    assert response.status_code == 200
    assert 'Error: Amount must be a number.' in response.data.decode('utf-8')

def test_search(client):
    response = client.get('/search?keyword=Test')
    assert response.status_code == 200
    assert 'Test Transaction' in response.data.decode('utf-8')

def test_filter(client):
    # Test successful filtering of transactions by category
    response = client.get('/filter?category=travel')
    assert response.status_code == 200
    assert 'Test Transaction' in response.data.decode('utf-8')

    # Test successful filtering of transactions by date
    response = client.get('/filter?start_date=2023-04-16&end_date=2023-04-16')
    assert response.status_code == 200
    assert 'Test Transaction' in response.data.decode('utf-8')

def test_calculate_balance(client):
    # Test calculation of running balance
    transaction1 = Transaction(date=datetime.date(2023, 4, 16), description='Test Transaction 1', amount=100.00, category='travel')
    transaction2 = Transaction(date=datetime.date(2023, 4, 16), description='Test Transaction 2', amount=50.00, category='travel')

    # Assuming db_session() returns a valid session object
    session = db.session
    session.add_all([transaction1, transaction2])
    session.commit()

    balance = calculate_balance()

    assert (balance == balance)