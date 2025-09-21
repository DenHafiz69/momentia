import os

from dotenv import load_dotenv
from datetime import datetime

from forms import RegistrationForm, LoginForm, PostForm, EditPostForm, SettingsForm

from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, render_template, redirect, request, session, url_for, flash, g, abort
from flask_session import Session
from flask_wtf import CSRFProtect

from modules.database import (insert_user, select_user, select_user_by_email, select_user_by_id,
                            insert_post, select_all_posts, select_post_by_id, select_posts_by_user,
                            update_post, delete_post, update_user)

# take environment variables from .env.
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SESSION_TYPE'] = "filesystem"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./data/database.db'

# Initialize Flask-Session
Session(app)

# Initialize CSRF protection
csrf = CSRFProtect(app)

# The homepage of the website
@app.route('/')
def index():
    # Get all posts from database
    posts = select_all_posts()
    
    # Convert posts to format expected by template
    formatted_posts = []
    for post in posts:
        formatted_posts.append({
            'id': post.id,
            'title': post.title,
            'author': post.author,
            'date_posted': post.date_posted.strftime('%B %d, %Y') if hasattr(post.date_posted, 'strftime') else str(post.date_posted),
            'content': post.content
        })
    
    # Show the homepage
    return render_template('index.html', posts=formatted_posts)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # Find user by email
        user = select_user_by_email(form.email.data)
        if user and check_password_hash(user.password, form.password.data):
            # Set session variables
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login failed. Please check your email and password.', 'danger')

    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Check if username already exists
        existing_user = select_user(form.username.data)
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'danger')
            return render_template('register.html', title='Register', form=form)
        
        # Check if email already exists
        existing_email = select_user_by_email(form.email.data)
        if existing_email:
            flash('Email already exists. Please use a different email address.', 'danger')
            return render_template('register.html', title='Register', form=form)

        # Hash the password
        hashed_password = generate_password_hash(form.password.data)

        # Insert user into database
        try:
            insert_user(form.username.data, form.email.data, hashed_password)
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('An error occurred while creating your account. Please try again.', 'danger')
            return render_template('register.html', title='Register', form=form)

    return render_template('register.html', title='Register', form=form)

# Logout the current user
@app.route('/logout')
def logout():
    
    # Forget any user_id
    session.clear()

    return redirect('/')

# Create a new post
@app.route('/post/new', methods=['GET', 'POST'])
def new_post():
    if 'user_id' not in session:
        flash('You need to be logged in to create a post.', 'warning')
        return redirect(url_for('login'))
    
    form = PostForm()
    if form.validate_on_submit():
        try:
            insert_post(form.title.data, form.content.data, session['user_id'])
            flash('Your post has been created!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash('An error occurred while creating your post. Please try again.', 'danger')
    
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

# View a specific post
@app.route('/post/<int:post_id>')
def post(post_id):
    post = select_post_by_id(post_id)
    if not post:
        abort(404)
    
    formatted_post = {
        'id': post.id,
        'title': post.title,
        'author': post.author,
        'author_id': post.author_id,
        'date_posted': post.date_posted.strftime('%B %d, %Y') if hasattr(post.date_posted, 'strftime') else str(post.date_posted),
        'content': post.content
    }
    
    return render_template('post.html', title=post.title, post=formatted_post)

# Edit a post
@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    post = select_post_by_id(post_id)
    if not post:
        abort(404)
    
    if 'user_id' not in session:
        flash('You need to be logged in to edit posts.', 'warning')
        return redirect(url_for('login'))
    
    if post.author_id != session['user_id']:
        flash('You can only edit your own posts.', 'danger')
        return redirect(url_for('post', post_id=post_id))
    
    form = EditPostForm()
    if form.validate_on_submit():
        try:
            update_post(post_id, form.title.data, form.content.data)
            flash('Your post has been updated!', 'success')
            return redirect(url_for('post', post_id=post_id))
        except Exception as e:
            flash('An error occurred while updating your post. Please try again.', 'danger')
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    
    return render_template('create_post.html', title='Edit Post', form=form, legend='Edit Post')

# Delete a post
@app.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post_route(post_id):
    post = select_post_by_id(post_id)
    if not post:
        abort(404)
    
    if 'user_id' not in session:
        flash('You need to be logged in to delete posts.', 'warning')
        return redirect(url_for('login'))
    
    if post.author_id != session['user_id']:
        flash('You can only delete your own posts.', 'danger')
        return redirect(url_for('post', post_id=post_id))
    
    try:
        delete_post(post_id)
        flash('Your post has been deleted!', 'success')
    except Exception as e:
        flash('An error occurred while deleting your post. Please try again.', 'danger')
    
    return redirect(url_for('index'))

# View user's posts
@app.route('/user/<username>')
def user_posts(username):
    user = select_user(username)
    if not user:
        abort(404)
    
    posts = select_posts_by_user(user.id)
    
    # Convert posts to format expected by template
    formatted_posts = []
    for post in posts:
        formatted_posts.append({
            'id': post.id,
            'title': post.title,
            'author': post.author,
            'date_posted': post.date_posted.strftime('%B %d, %Y') if hasattr(post.date_posted, 'strftime') else str(post.date_posted),
            'content': post.content
        })
    
    return render_template('user_posts.html', posts=formatted_posts, user=user)

@app.route('/settings', methods=['POST', 'GET'])
def settings():
    if 'user_id' not in session:
        flash('You need to be logged in to access settings.', 'warning')
        return redirect(url_for('login'))

    form = SettingsForm()
    user = select_user_by_id(session['user_id'])

    if form.validate_on_submit():
        # Check if username already exists (but not for current user)
        existing_user = select_user(form.username.data)
        if existing_user and existing_user.id != session['user_id']:
            flash('Username already exists. Please choose a different username.', 'danger')
            return render_template('settings.html', title='Settings', form=form)

        # Check if email already exists (but not for current user)
        existing_email = select_user_by_email(form.email.data)
        if existing_email and existing_email.id != session['user_id']:
            flash('Email already exists. Please use a different email address.', 'danger')
            return render_template('settings.html', title='Settings', form=form)

        # Update user in database
        try:
            update_user(session['user_id'], form.username.data, form.email.data)
            # Update session with new username
            session['username'] = form.username.data
            flash('Your settings have been updated!', 'success')
            return redirect(url_for('settings'))
        except Exception as e:
            flash('An error occurred while updating your settings. Please try again.', 'danger')

    elif request.method == 'GET':
        # Pre-populate form with current user data
        form.username.data = user.username
        form.email.data = user.email

    return render_template('settings.html', title='Settings', form=form)

if __name__ == '__main__':
    app.run(debug=True)
