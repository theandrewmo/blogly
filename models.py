"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

#initialize variable and store what runs from SQLAlchemy()
db = SQLAlchemy()

# function that connects to database, associates this flask app with db variable
def connect_db(app):
    db.app = app
    db.init_app(app)

# Models 

class User(db.Model):
    """ User """

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String(30),
                           nullable = False)
    
    last_name = db.Column(db.String(30))

    image_url = db.Column(db.String(500))

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

