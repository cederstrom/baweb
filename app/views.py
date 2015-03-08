from flask import flash, render_template, redirect, url_for
from app import app, db
from .forms import TeamForm
from .models import Team, TeamMember


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/flumride')
@app.route('/flumride/info')
def flumride_info():
    return render_template("flumride/info.html")


@app.route('/flumride/submit', methods=['GET', 'POST'])
def flumride_submit():
    form = TeamForm()
    if form.validate_on_submit():

        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('flumride_teams'))
    else:
        return render_template("flumride/submit.html", form=form)


@app.route('/flumride/teams')
def flumride_teams():
    return render_template("flumride/teams.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")
