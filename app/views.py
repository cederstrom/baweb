from flask import (render_template, flash, redirect, url_for, request, g)
from flask.ext.login import (login_user, logout_user, current_user)
from app import app, db, lm, oid
from app.forms import TeamForm
from app.models import Team, TeamMember, User
from app import logic, mail


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/login')
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    return oid.try_login('https://www.google.com/accounts/o8/id',
                         ask_for=['email'])


@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        return redirect(url_for('logout'))
    login_user(user)
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.before_request
def before_request():
    g.user = current_user


@app.route('/sporrtNews')
@app.route('/baStory')
@app.route('/index')
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/flumride')
@app.route('/flummen')
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
        'members_need_bed': TeamMember.need_bed_count(),
        'members_sittning': TeamMember.sitting_count(),
        'non_members_sfs': TeamMember.not_sfs_count()
    }
    return render_template("flumride/teams.html", teams=teams, total=total)


@app.route('/contact')
def contact():
    return render_template("contact.html")
