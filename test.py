from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
TEST_IMAGE_URL = 'https://media.istockphoto.com/photos/young-boy-in-red-superhero-cape-and-mask-picture-id174488272?b=1&k=20&m=174488272&s=170667a&w=0&h=L6x0NdJ9W4gQ1GDDb9pk0ch-ouVBXduVgev36G9XCOU='

db.drop_all()
db.create_all()

class UserTestCase(TestCase):
    """Tests for user routes"""

    def setUp(self):
        User.query.delete()

        user = User(first_name = "Ashely", last_name = "Wang")
        db.session.add(user)
        db.session.commit()

        self.user = user
    
    def tearDown(self):
        db.session.rollback()
    
    def test_show_all_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Ashely', html)

    def test_show_add_user_form(self):
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Create a user</h1>', html)
            
    def test_add_user(self):
        with app.test_client() as client:
            new_user = {"first_name":"Aaron", "last_name":"Lee", "image_url":TEST_IMAGE_URL}
            resp = client.post("/users/new",data = new_user, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Aaron', html)

    def test_user_detail(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(self.user.first_name, html)

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post(f"/users/{self.user.id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(self.user.first_name, html)