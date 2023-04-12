"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag
# from config import Config

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
    """ Shows homepage with most recent posts (limit 5) """

    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()

    return render_template('homepage.html', recent_posts=recent_posts)

@app.route('/users')
def show_all_users():
    """ shows all users """

    users = User.query.order_by(User.last_name).order_by(User.first_name).all()

    return render_template('users.html', users=users)

@app.route('/users/new')
def show_form():
    """ shows form to create user """

    return render_template('create_user.html')

@app.route('/users/new', methods=["POST"])
def create_user():
    """ create new user """

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    if not image_url:
        image_url = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    if new_user:
        flash('new user added successfully')

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """ Shows user details for user """

    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id).all()

    return render_template('details.html', user=user, posts=posts)

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
    if user:
        flash('user edited successfully')

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """ Deletes user and reroutes to /users """

    user = User.query.get_or_404(user_id)

    User.query.filter_by(id=user.id).delete()
    db.session.commit()
    if user:
        flash('user deleted successfully')

    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new')
def show_add_post(user_id):
    """ Shows form to add new post """

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template('add_post.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_new_post(user_id):
    """ Handles add new post """

    title = request.form['title']
    content = request.form['content']
    tags = request.form.getlist('tag')

    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    for tag in tags:
        new_post_tag = PostTag(post_id=new_post.id,tag_id=int(tag))
        db.session.add(new_post_tag)
    
    db.session.commit()

    flash('new post added successfully')

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """ Shows post detail """

    post = Post.query.get_or_404(post_id)
    post_tags = PostTag.query.filter_by(post_id=post_id).all()

    return render_template('post_details.html', post=post, post_tags=post_tags)

@app.route('/posts/<int:post_id>/edit')
def show_post_edit_form(post_id):
    """ Shows edit form for post editing """

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template('edit_post.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def handle_post_edit(post_id):
    """ Handles post editing """

    title = request.form['title']
    content = request.form['content']
    tags = request.form.getlist('tag')

    post = Post.query.filter_by(id=post_id).one_or_none()
    if title:
        post.title = title
    if content:
        post.content = content
    db.session.commit()

    current_tags = []

    for post_tag in post.post_tags:
        current_tags.append(post_tag.tag_id)
        if str(post_tag.tag_id) not in tags:
            PostTag.query.filter_by(post_id=post_id, tag_id=post_tag.tag_id).delete()

    for tag in tags:
        if int(tag) not in current_tags:
            post_tag = PostTag(post_id=post_id, tag_id=int(tag))  
            db.session.add(post_tag) 
    
    db.session.commit()

    flash('post edited successfully')

    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """ Handles post delete """

    post = Post.query.get(post_id)
    user = post.users.id
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    flash('post deleted successfully')

    return redirect(f'/users/{user}')

@app.errorhandler(404)
def page_not_found(e):
    """ Shows custom 404 page """

    return render_template('404.html')

@app.route('/tags')
def show_tags():
    """ Shows all tags """

    tags = Tag.query.all()

    return render_template('all_tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag_details(tag_id):
    """ Shows tag details """

    tag = Tag.query.get_or_404(tag_id)
    post_tags = PostTag.query.filter_by(tag_id=tag_id).all()

    return render_template('tag_details.html', tag=tag, post_tags=post_tags)

@app.route('/tags/new')
def show_add_tag_form():
    """ Shows add tag form """

    return render_template('add_tag.html')

@app.route('/tags/new', methods=['POST'])
def add_tag():
    """ Handles add tag form """

    name = request.form['name']
    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def show_tag_edit_form(tag_id):
    """ Shows tag edit form """

    tag = Tag.query.filter_by(id=tag_id).one_or_none()

    return render_template('edit_tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def handle_tag_edit(tag_id):
    """ Handles tag editing """

    name = request.form['name']

    tag = Tag.query.filter_by(id=tag_id).one_or_none()
    if name:
        tag.name = name
    db.session.commit()
    flash('post edited successfully')

    return redirect(f'/tags/{tag_id}')

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """ Handles tag delete """

    Tag.query.filter_by(id=tag_id).delete()
    db.session.commit()
    flash('tag deleted successfully')

    return redirect('/tags')