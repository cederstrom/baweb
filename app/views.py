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
    return render_template(
        "flumride/info.html", submit_open=logic.is_submit_open())


@app.route('/flumride/submit', methods=['GET', 'POST'])
def flumride_submit():
    if not logic.is_submit_open():
        return redirect(url_for('flumride_info'))

    form = TeamForm()
    if form.validate_on_submit():
        team = Team()
        form = TeamForm(request.form)
        form.populate_obj(team)
        db.session.add(team)
        db.session.commit()
        mail.send(team.email, team.get_price(), team.name)
        return render_template("flumride/confirmation.html", team=team)
    else:
        return render_template("flumride/submit.html", form=form)


@app.route('/flumride/teams')
def flumride_teams():
    teams = db.session.query(Team)
    members = db.session.query(TeamMember)

    total = {
        'teams': teams.count(),
        'members': members.count(),
        'members_need_bed':
            members.filter(TeamMember.need_bed.is_(True)).count(),
        'members_sittning':
            members.filter(TeamMember.sittning.is_(True)).count(),
        'members_sfs': members.filter(TeamMember.sfs.is_(False)).count()
    }
    return render_template("flumride/teams.html", teams=teams, total=total)


@app.route('/contact')
def contact():
    return render_template("contact.html")
