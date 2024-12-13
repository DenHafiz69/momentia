from flask import Flask, render_template, redirect, request

app  = Flask(__name__)

# The homepage of the website
@app.route('/')
def index():
    return render_template('index.html')


# User that is not logged in would see this and the login only
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')