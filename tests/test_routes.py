import unittest
from flask import json
from app import app, db
from app.models import User


class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_signup(self):
        response = self.client.post('/signup', data=json.dumps(dict(
            firstname='test',
            lastname='user',
            username='testuser',
            email='test@example.com',
            password_hash='testpassword'
        )), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.data)['message'],
            'Registered successfully'
            )

    def test_login(self):
        user = User(
            username='testuser',
            email='test@example.com',
            password_hash='testpassword'
            )
        db.session.add(user)
        db.session.commit()
        response = self.client.post('/login', data=json.dumps(dict(
            email='test@example.com',
            password_hash='testpassword'
        )), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.data)['message'],
            'Logged in successfully!'
            )

    def test_logout(self):
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.data)['message'],
            'Logged out successfully!'
            )

    def test_account_recovery(self):
        response = self.client.get('/account_recovery')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.data)['message'],
            'Account recovery page'
            )


if __name__ == '__main__':
    unittest.main()
