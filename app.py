import os

from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

import sqlite3

# Configure application
app  = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Connect to SQLite database
conn = sqlite3.connect('data/database.db')
cursor = conn.cursor()

# The homepage of the website
@app.route('/')
def index():

    # Show the homepage
    return render_template('index.html')

# Login when the user already in the database
# If not, go to the index page and tell the user to login
@app.route('/login', methods=['POST', 'GET'])
def login():

    # Forget any user_id
    session.clear()

    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        # Ensure username was submmited
        if not request.form.get('username'):
            return render_template('apology.html', error="must provide username")

        # Ensure password was submmited
        if not request.form.get('password'):
            return render_template('apology.html', error="must provide password")

        # Ensure password was submmited

        # Query database for username

# Logout the current user
@app.route('/logout')
def logout():
    
    # Forget any user_id
    session.clear()

    return redirect('/')

@app.route('/register')
def register():

    if request.method == 'POST':
        pass

    return render_template('register.html')


if __name__ == '__main__':  
   app.run(debug=True)  