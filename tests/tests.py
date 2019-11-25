import unittest
from app import app
from app.models import db, User


class UsersTests(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5433/tempdb'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app = app.test_client()

        # Connect to Database
        db.app = app
        db.init_app(app)
        db.drop_all()
        db.create_all()

    # executed after each test
    def tearDown(self):
        db.session.close()
        db.drop_all()

    def register(self, data):
        return self.app.post('/users/register', data=data, follow_redirects=True)

    def login(self, email, password):
        return self.app.post(
            '/users/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def test_valid_registration(self):
        self.app.get('/users/register', follow_redirects=True)
        response = self.register(data=dict(fname="Leizle", lname="Ho",
                                           username="leizleho",
                                           email="leizleho@yahoo.com",
                                           password="12345",
                                           pass_confirm="12345"))
        self.assertIn(b'User registration is complete', response.data)

    def test_valid_login(self):
        self.app.get('/users/register', follow_redirects=True)
        response = self.register(data=dict(fname="Leizle", lname="Ho",
                                           username="leizleho",
                                           email="leizleho@yahoo.com",
                                           password="12345",
                                           pass_confirm="12345"))
        self.app.get('/users/login', follow_redirects=True)
        response = self.login('leizleho@yahoo.com', '12345')
        self.assertIn(b'Logged in successfully.', response.data)
        self.assertIn(b'Leizle Ho', response.data)

    def test_invalid_login(self):
        self.app.get('/users/register', follow_redirects=True)
        response = self.register(data=dict(fname="Leizle", lname="Ho",
                                           username="leizleho",
                                           email="leizleho@yahoo.com",
                                           password="12345",
                                           pass_confirm="12345"))
        self.app.get('/users/login', follow_redirects=True)
        response = self.login('lalala@yahoo.com', '12345')
        self.assertNotIn(b'Logged in successfully.', response.data)
        self.assertNotIn(b'Lala La ', response.data)


if __name__ == "__main__":
    unittest.main()
