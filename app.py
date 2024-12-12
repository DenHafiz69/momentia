from flask import Flask, render_template, redirect

app  = Flask(__name__)

# The homepage of the website
@app.route("/")
def index():
    return render_template("index.html")