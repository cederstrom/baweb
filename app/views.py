from flask import redirect, render_template, request, url_for
from app import app, db
from app.forms import TeamForm
from app.models import Team, TeamMember
from app import logic
from app import mail


@app.route('/index')
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/flumride')
@app.route('/flumride/info')
def flumride_info():
    return render_template("flumride/info.html")


@app.route('/flumride/submit', methods=['GET', 'POST'])
def flumride_submit():
    if not logic.is_submit_open():
        milliseconds = logic.get_milliseconds_until_submit_opens()
        return render_template("flumride/countdown.html",
                               milliseconds=milliseconds)

    form = TeamForm()
    if form.validate_on_submit():
        team = Team()
        form = TeamForm(request.form)
        form.populate_obj(team)
        db.session.add(team)
        db.session.commit()
        mail.send(team.email, team.price, team.name)
        return render_template("flumride/confirmation.html", team=team)
    else:
        return render_template("flumride/submit.html", form=form)


@app.route('/flumride/teams')
def flumride_teams():
    teams = db.session.query(Team)
    total = {
        'teams': teams.count(),
        'members': db.session.query(TeamMember).count(),
        'members_need_bed': logic.get_members_need_bed_count(),
        'members_sittning': logic.get_members_sitting_count(),
        'non_members_sfs': logic.get_members_non_sfs_count()
    }
    return render_template("flumride/teams.html", teams=teams, total=total)


@app.route('/contact')
def contact():
    return render_template("contact.html")
