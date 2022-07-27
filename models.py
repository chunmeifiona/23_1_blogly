"""Models for Blogly."""
from email.policy import default
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DEFAULT_IMAGE_URL = 'https://media.istockphoto.com/photos/young-boy-in-red-superhero-cape-and-mask-picture-id174488272?b=1&k=20&m=174488272&s=170667a&w=0&h=L6x0NdJ9W4gQ1GDDb9pk0ch-ouVBXduVgev36G9XCOU='
def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    def __repr__(self):
        u = self
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name}"

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.Text, default=DEFAULT_IMAGE_URL)
