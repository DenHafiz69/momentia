import os

from datetime import datetime

from forms import RegistrationForm, LoginForm

from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, render_template, redirect, request, session, url_for, flash, g
from flask_session import Session
from flask_wtf import CSRFProtect

from modules.database import insert_user, select_user, select_user_by_email

app = Flask(__name__)
app.config['SECRET_KEY'] = '1c61ded0bfaa415caea6fe5916ebf59d'
app.config['SESSION_TYPE'] = "filesystem"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./data/database.db'

# Initialize Flask-Session
Session(app)

# Initialize CSRF protection
csrf = CSRFProtect(app)

posts = [
    {
        'author': 'Den Hafiz',
        'title': 'This is a post',
        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque rhoncus et magna non suscipit. Aliquam porttitor dolor velit, eu rutrum nulla accumsan ut. Morbi enim augue, scelerisque vitae orci eget, finibus pretium leo. Integer pulvinar laoreet pretium.',
        'date_posted': '5th January 2024'
    },
    {
        'author': 'Nor Syazni',
        'title': 'Second post',
        'content': 'Nullam interdum, ante nec tempor bibendum, nisl mi ornare neque, ut malesuada felis nisi ac erat. Mauris et facilisis sapien. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Quisque tincidunt purus elit, pretium rhoncus purus commodo nec. Curabitur pellentesque tempus eros vel vestibulum. Ut sed finibus arcu. Vestibulum non quam elit.',
        'date_posted': '2nd January 2024'
    }
]

# The homepage of the website
@app.route('/')
def index():

    # Show the homepage
    return render_template('index.html', posts=posts)

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



@app.route('/settings', methods=['POST', 'GET'])
def settings():
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
