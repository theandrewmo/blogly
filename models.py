"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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

    def __repr__(self):
        return f'<User {self.first_name} {self.last_name} {self.image_url}>'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

class Post(db.Model):
    """  Post """

    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    title = db.Column(db.String(30),
                      nullable = False)
    
    content = db.Column(db.String(5000))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete="CASCADE"))
    
    users = db.relationship('User', backref='posts')

    post_tags = db.relationship('PostTag', backref='post')

    tags = db.relationship('Tag', secondary='posttags', backref='tagposts')

    def friendly_created_at(self):
        return self.created_at.strftime('%b %d, %Y %I:%M %p')

    def __repr__(self):
        return f'<Post {self.title} {self.content} {self.users} {self.created_at}>'

class Tag(db.Model):
    """ Tag """

    __tablename__ = 'tags'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    name = db.Column(db.String(30),
                     nullable=False,
                     unique=True)
    
    post_tags = db.relationship('PostTag', backref='tag')
    
    def __repr__(self):
        return f'<Tag {self.name}>'
    
class PostTag(db.Model):
    """ PostTag """

    __tablename__ = 'posttags'

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id', ondelete='CASCADE'),
                        primary_key=True)

    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.id', ondelete='CASCADE'),
                       primary_key=True)  

    def __repr__(self):
        return f'<PostTag {self.post_id} {self.tag_id}>'                  
    
