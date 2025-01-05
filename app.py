import os

from flask import Flask, render_template, redirect, request, session, url_for, flash
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
# conn = sqlite3.connect('data/database.db')
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Check if table not exist, then create table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL)
    """)

conn.commit()

# The homepage of the website
@app.route('/')
def index():

    # Show the homepage
    return render_template('index.html')

# Login when the user already in the database
# If not, go to the index page and tell the user to login
# Refer to this website 
# https://www.geeksforgeeks.org/login-and-registration-project-using-flask-and-mysql/
@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        cursor.execute('SELECT * FROM accounts WHERE username=? AND password=?', (username, password))
        account = cursor.fetchone()
        if account:
            session['username'] =account['username']
            flash('Logged in successfully!')
            return render_template('index.html', notification = notification)
        else:
            flash('Invalid credentials')
        
    return render_template('login.html')
        

# Logout the current user
@app.route('/logout')
def logout():
    
    # Forget any user_id
    session.clear()

    return redirect('/')

@app.route('/register', methods=['POST', 'GET'])
def register():

    if request.method == 'POST':

        username = request.form.get('username')
        password = generate_password_hash(request.form.get('password'))
        
        with conn:
            cursor.execute("INSERT INTO users (username, password) VALUES(?,?)",
            (username, password))

        return redirect('/')

    return render_template('register.html')

@app.route('/settings', methods=['POST', 'GET'])
def settings():
    return redirect('/')

if __name__ == '__main__':  
   app.run(debug=True)
