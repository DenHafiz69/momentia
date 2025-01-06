import os

import sqlite3
import cs50

from forms import RegistrationForm, LoginForm

from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, render_template, redirect, request, session, url_for, flash, g
from flask_session import Session

# Configure application
app  = Flask(__name__)

app.config['SECRET_KEY'] = '1c61ded0bfaa415caea6fe5916ebf59d'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"

Session(app)

DATABASE = "./data/data.db"

with sqlite3.connect(DATABASE) as conn:
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL)
    """)

    conn.commit()

db = cs50.SQL("sqlite:///data/data.db")

# The homepage of the website
@app.route('/')
def index():

    # Show the homepage
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
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
