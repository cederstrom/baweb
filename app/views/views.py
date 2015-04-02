from flask import render_template
from app import app


@app.route('/sporrtNews')
@app.route('/baStory')
@app.route('/index')
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")
