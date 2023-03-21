from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, ratehr than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserTestCase(TestCase):
    """ Tests for routing for Users """

    def setUp(self):
        """ Clean up any existing users """

        User.query.delete()

        user = User(first_name='TestFirst', last_name='TestLast', image_url='https://i.redd.it/w3kr4m2fi3111.png')
        db.session.add(user)
        db.session.commit()

        self.id = user.id
    
    def tearDown(self):
        """ clean up any fouled transaction """

        db.session.rollback()

    def test_index(self):
        with app.test_client() as client:
            resp = client.get('/', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)

    def test_show_all_users(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestFirst', html)

    def test_create_user(self):
        with app.test_client() as client:
            test_data = {"first_name": "TestFirst2", "last_name": "TestLast2", "image_url": "https://i.redd.it/w3kr4m2fi3111.png"}
            resp = client.post('/users/new', data=test_data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestFirst2", html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestFirst", html)       

    def test_show_edit(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.id}/edit')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Edit", html)  
            
    def test_show_edit_user(self):
        with app.test_client() as client:
            test_data = {"first_name": "TestEditFirst", "last_name": "TestEditLast", "image_url": ""}
            resp = client.post(f'/users/{self.id}/edit', data=test_data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestEditFirst", html) 

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post(f'/users/{self.id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("TestFirst", html)
            