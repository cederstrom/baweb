from flask import render_template
from app import app
from .forms import TeamForm


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/flumride')
@app.route('/flumride/info')
def flumride_info():
    return render_template("flumride/info.html")


@app.route('/flumride/submit')
def flumride_submit():
    form = TeamForm()
    # form.members.min_entries = 1
    # form.members.max_entries = 10
    return render_template("flumride/submit.html", form=form)


@app.route('/flumride/teams')
def flumride_teams():
    return render_template("flumride/teams.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")
