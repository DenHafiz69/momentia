import os

from datetime import datetime

from forms import RegistrationForm, LoginForm

from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, render_template, redirect, request, session, url_for, flash, g
from flask_session import Session

from modules.database import insert_user, select_user

app = Flask(__name__)
app.config['SECRET_KEY'] = '1c61ded0bfaa415caea6fe5916ebf59d'
app.config['SESSION_TYPE'] = "filesystem"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./data/database.db'

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
        flash(f'Login successful.', 'success')
        return redirect(url_for('index'))

    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index'))

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
