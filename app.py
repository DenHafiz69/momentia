import os

from flask import Flask, render_template, redirect, request, session, url_for, flash, g
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

import sqlite3
import cs50

# Configure application
app  = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
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

# Login when the user already in the database
# If not, go to the index page and tell the user to login
@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        rows = db.execute("""
            SELECT * FROM users
            WHERE username = ?
        """, username)[0]

        if rows:
            user_id = rows['id']
            username = rows['username']
            password_hash = rows['password']

            try:
                check_password_hash(password_hash, password)
            except:
                flash("Password does not match.")
            
            session["user_id"] = user_id

            return redirect("/")
            
        else:
            flash("Invalid credentials.")
        
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

        rows = db.execute("""
            SELECT * FROM users
            WHERE username=?
        """, (username))

        if rows:
            flash("User already exist.")
        else:
            db.execute("""
                INSERT INTO users (username, password)
                VALUES(?,?)
            """, username, password)

            return redirect('/')

    return render_template('register.html')

@app.route('/settings', methods=['POST', 'GET'])
def settings():
    return redirect('/')

if __name__ == '__main__':

    app.run(debug=True)
