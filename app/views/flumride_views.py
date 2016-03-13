from flask import jsonify, render_template, redirect, url_for, request
from app import app, db, logic, mail
from app.decorators import login_required
from app.forms import TeamForm, MemberForm
from app.models import Team, TeamMember


@app.route('/flumride')
@app.route('/flumride/')
@app.route('/flummen')
@app.route('/flummen/')
@app.route('/flumride/info')
@app.route('/flumride/info/')
def flumride_info():
    return render_template("flumride/info.html")


@app.route('/flumride/submit', methods=['GET', 'POST'])
def flumride_submit():
    if not logic.is_submit_open():
        milliseconds = logic.get_milliseconds_until_submit_opens()
        return render_template("flumride/countdown.html",
                               milliseconds=milliseconds)

    if not logic.are_there_beds_left() or not logic.are_there_sittning_left():
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


@app.route('/flumride/members')
def flumride_members():
    members = TeamMember.query.order_by(TeamMember.person_number).all()
    return render_template("flumride/members.html", members=members)


@app.route('/flumride/member/<id>', methods=['GET', 'POST'])
@login_required
def flumride_edit_member(id):
    member = TeamMember.get(id)
    assert member

    if request.method == 'POST':
        form = MemberForm(request.form)
        form.populate_obj(member)
        db.session.add(member)
        db.session.commit()
        return redirect(url_for('flumride_teams', _anchor=member.team.id))
    else:
        form = MemberForm(obj=member)
        return render_template("flumride/edit_member.html", form=form,
                               title='Editera medlem')


@app.route('/flumride/team/<id>/add-member', methods=['GET', 'POST'])
@login_required
def flumride_add_member(id):
    team = Team.get(id)
    assert team

    if request.method == 'POST':
        member = TeamMember()
        form = MemberForm(request.form)
        form.populate_obj(member)
        member.team = team
        db.session.add(member)
        db.session.commit()
        return redirect(url_for('flumride_teams', _anchor=member.team.id))
    else:
        form = MemberForm()
        return render_template("flumride/edit_member.html", form=form,
                               title='Lägg till medlem')


@app.route('/flumride/team/<id>/set-has-payed', methods=['POST'])
@login_required
def flumride_set_has_payed(id):
    team = Team.get(id)
    team.has_payed = True
    db.session.commit()
    resp = jsonify(has_payed=True)
    resp.status_code = 200
    return resp


@app.route('/flumride/teams')
def flumride_teams():
    teams = db.session.query(Team)
    has_payed_arg = request.args.get('has_payed')
    if has_payed_arg is not None:
        has_payed = has_payed_arg == 'True'
        teams = teams.filter_by(has_payed=has_payed)
    total = {
        'teams': teams.count(),
        'members': db.session.query(TeamMember).count(),
        'members_need_bed': TeamMember.need_bed_count(),
        'members_sittning': TeamMember.sitting_count(),
        'non_members_sfs': TeamMember.not_sfs_count()
    }
    return render_template("flumride/teams.html", teams=teams, total=total,
                           has_payed=has_payed_arg)


@app.route('/flumride/team/<id>', methods=['GET', 'POST'])
@login_required
def flumride_edit_team(id):
    team = Team.get(id)
    assert team

    if request.method == 'POST':
        form = TeamForm(request.form)
        team.name = form.name.data
        team.email = form.email.data
        team.city = form.city.data
        team.slogan = form.slogan.data
        team.has_payed = form.has_payed.data
        db.session.commit()
        return redirect(url_for('flumride_teams', _anchor=team.id))
    else:
        form = TeamForm(obj=team)
        return render_template("flumride/edit_team.html", form=form)
