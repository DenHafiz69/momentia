import os

from flask import Flask, render_template, redirect, request, session, url_for, flash, g
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

import sqlite3

# Configure application
app  = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

DATABASE = './data/data.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
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
@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
            account = cursor.fetchone()
            if account:
                session['username'] =account['username']
                flash('Logged in successfully!')
                
                return render_template('index.html')
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
        
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()

            # Check if the user exist or not
            try: 
                user = cursor.execute("SELECT * FROM USERS WHERE username=?", (username))
            except:
                # If the user does not exist, insert the value
                cursor.execute("INSERT INTO users (username, password) VALUES(?,?)", (username, password))
                conn.commit()

            return redirect('/')

    return render_template('register.html')

@app.route('/settings', methods=['POST', 'GET'])
def settings():
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
