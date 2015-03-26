from flask import (jsonify, render_template, redirect, url_for, request, g)
from flask.ext.login import (login_user, logout_user, current_user)
from app import app, db, lm, logic, mail
from app.forms import TeamForm, MemberForm
from app.models import Team, TeamMember, User
from flask_dance.contrib.github import github


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/login")
def login():
    return redirect(url_for("github.login"))


@app.route("/loginCallback")
def login_callback():
    resp = github.get("/user/emails")
    if resp.ok:
        email = resp.json()[0]['email']
        print("Trying to authenticate with email: %r" % email)
        user = User.query.filter_by(email=email).first()
        if user:
            login_user(user)
            return redirect(request.args.get('next') or url_for('index'))
    return redirect(url_for('logout'))


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


def _is_user_admin():
    return g.user.is_authenticated() and g.user.is_admin


@app.route('/flumride/submit', methods=['GET', 'POST'])
def flumride_submit():
    if not logic.is_submit_open() and not _is_user_admin():
        milliseconds = logic.get_milliseconds_until_submit_opens()
        return render_template("flumride/countdown.html",
                               milliseconds=milliseconds)

    if ((not logic.are_there_beds_left() or
         not logic.are_there_sittning_left()) and not _is_user_admin()):
        return render_template("flumride/submit_temp_closed.html")

    form = TeamForm()
    if form.validate_on_submit():
        team = _create_team(request)
        mail.send(team.email, team.price, team.name)
        return render_template("flumride/confirmation.html", team=team)
    else:
        number_of_non_sfs_left = logic.get_number_of_non_sfs_left()
        return render_template("flumride/submit.html", form=form,
                               number_of_non_sfs_left=number_of_non_sfs_left)


def _create_team(request):
    team = Team()
    form = TeamForm(request.form)
    form.populate_obj(team)
    db.session.add(team)
    db.session.commit()
    return team


@app.route('/flumride/number_of_non_sfs_left')
def flumride_number_of_non_sfs_left():
    number_of_non_sfs_left = logic.get_number_of_non_sfs_left()
    return jsonify(number_of_non_sfs_left=number_of_non_sfs_left)


@app.route('/flumride/member/<id>', methods=['GET', 'POST'])
def flumride_edit_member(id):
    if not _is_user_admin():
        return redirect(url_for('index'))

    member = TeamMember.get(id)
    print("person_number: %r" % member.person_number)
    assert member

    if request.method == 'POST':
        form = MemberForm(request.form)
        form.populate_obj(member)
        db.session.add(member)
        db.session.commit()
        return redirect(url_for('flumride_teams', team_id=member.team.id))
    else:
        form = MemberForm(obj=member)
        return render_template("flumride/edit_member.html", form=form)


@app.route('/flumride/teams', defaults={'team_id': None})
@app.route('/flumride/teams/<team_id>')
def flumride_teams(team_id):
    teams = db.session.query(Team)
    total = {
        'teams': teams.count(),
        'members': db.session.query(TeamMember).count(),
        'members_need_bed': TeamMember.need_bed_count(),
        'members_sittning': TeamMember.sitting_count(),
        'non_members_sfs': TeamMember.not_sfs_count()
    }
    return render_template("flumride/teams.html", teams=teams, total=total,
                           team_id=team_id)


@app.route('/contact')
def contact():
    return render_template("contact.html")
