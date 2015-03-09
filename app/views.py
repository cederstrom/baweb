from flask import flash, redirect, render_template, request, url_for
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
        team = Team()
        form = TeamForm(request.form)
        form.populate_obj(team)
        db.session.add(team)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('flumride_teams'))
    else:
        return render_template("flumride/submit.html", form=form)


@app.route('/flumride/teams')
def flumride_teams():
    teams = db.session.query(Team)
    members = db.session.query(TeamMember)

    total = {
        'teams': teams.count(),
        'members': members.count(),
        'members_need_bed': members.filter(TeamMember.need_bed.is_(True)).count(),
        'members_sittning': members.filter(TeamMember.sittning.is_(True)).count(),
        'members_sfs': members.filter(TeamMember.sfs.is_(False)).count()
    }
    return render_template("flumride/teams.html", teams=teams, total=total)


@app.route('/contact')
def contact():
    return render_template("contact.html")
