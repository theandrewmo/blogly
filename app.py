"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.debug = True
app.config['SECRET_KEY'] = 'very-secret'

toolbar = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# pass app into function from models
connect_db(app)
db.create_all()

@app.route('/')
def index():
    """ Shows index page with all users in db """

    # users = User.query.all()

    # return render_template('base.html', users=users)
    return redirect('/users')

@app.route('/users')
def show_all_users():
    """ shows all users """

    users = User.query.order_by(User.last_name).order_by(User.first_name).all()

    return render_template('users.html', users=users)

@app.route('/users/new')
def show_form():
    """ shows form to create new user"""

    return render_template('create_user.html')

@app.route('/users/new', methods=["POST"])
def create_user():
    """ creates a new user """

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    if not image_url:
        image_url = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """ Shows user details for user """

    user = User.query.get_or_404(user_id)

    return render_template('details.html', user=user)

@app.route('/users/<int:user_id>/edit')
def show_edit(user_id):
    """ Shows page to edit user """

    user = User.query.get_or_404(user_id)

    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def show_edit_user(user_id):
    """ Handles edit user form """

    user = User.query.get_or_404(user_id)
  
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    if first_name: 
        user.first_name=first_name
    if last_name:
        user.last_name=last_name
    if image_url:
        user.image_url=image_url
    
    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """ Deletes user and reroutes to /users """

    user = User.query.get_or_404(user_id)

    User.query.filter_by(id=user.id).delete()
    db.session.commit()

    return redirect('/users')



