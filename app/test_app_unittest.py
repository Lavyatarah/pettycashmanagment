import unittest
from .routes import app, create_tables
from .models import db
from .models import Transaction
import datetime

class TestPettyCashApp(unittest.TestCase):
    


    def setUp(self):
        app.config['TESTING'] = True
        test_transaction = Transaction(
            date=datetime(2023, 4, 16),
            description='Test Transaction',
            amount=100.00,
            category='travel'
        )
        
        db.session.add(test_transaction)
        db.session.commit()
        
        with app.app_context():
            db.create_all()
            create_tables()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_record_transaction(self):
        # Test successful recording of transactions
        with app.test_client() as client:
            response = client.post('/add_transaction', data={
                'date': '2023-04-16',
                'description': 'Test Transaction',
                'amount': 100.00,
                'category': 'travel'
            })
            self.assertEqual(response.status_code, 200)

        # Validate if transaction is recorded in the database
        with app.app_context():
            transaction = Transaction.query.filter_by(description='Test Transaction').first()
            self.assertIsNotNone(transaction)
            self.assertEqual(transaction.amount, 100.00)

        # Validate input data for required fields and data types
        with app.test_client() as client:
            response = client.post('/add_transaction', data={})
            self.assertIn(b'Error: All fields are required.', response.data)

            response = client.post('/add_transaction', data={
                'date': '2023-04-16',
                'description': 'Test Transaction',
                'amount': 'invalid',
                'category': 'travel'
            })
            self.assertIn(b'Error: Amount must be a number.', response.data)

    def test_view_transactions(self):
        # Test viewing all recorded transactions
        with app.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Transaction', response.data)

        # Test filtering by date
        with app.test_client() as client:
            response = client.get('/filter?start_date=2023-04-15&end_date=2023-04-17')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Transaction', response.data)

        # Test filtering by category
        with app.test_client() as client:
            response = client.get('/filter?category=travel')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Transaction', response.data)

    # Add more test methods for searching and running balance functionalities

if __name__ == '__main__':
    unittest.main()
