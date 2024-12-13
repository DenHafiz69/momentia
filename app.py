from flask import Flask, render_template, redirect, request
import flask_login

app  = Flask(__name__)
login_manaer = flask_login.LoginManager()
login_manaer.init_app(app)

# The homepage of the website
@app.route('/')
def index():
    return render_template('index.html')

# Login when the user already in the database
# If not, go to the index page and tell the user to login