# -*- coding: utf-8 -*-
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
        return render_template("flumride/countdown.html", milliseconds=milliseconds)

    remaining_tickets_for_type = [logic.get_number_of_tickets_for_this_type_left(ind) for ind, ticket in enumerate(app.config['FLUMRIDE']['ticket_types'])]
    number_of_non_sfs_left = logic.get_number_of_non_sfs_left()

    if sum(remaining_tickets_for_type) <= 0 or logic.has_submit_closed():
        return render_template("flumride/submit_temp_closed.html")

    form = TeamForm(request.form)
    error_message = "None"
    form.Meta.csrf = False

    if request.method == 'POST':
        person_numbers = [member_form.data['person_number'] for member_form in form.members]

        if form.validate():
            duplicate_name = Team.query.filter_by(name=form.name.data).first()
            duplicate_person_number = any(TeamMember.query.filter_by(person_number=pn).first() for pn in person_numbers if pn)


            if duplicate_name:
                form.name.errors.append('Det finns redan ett lag med detta namn.')
                error_message = "Det finns redan ett lag med detta namn."

            if duplicate_person_number:
                form.errors['person_number'] = ['Det finns redan en användare med detta personnummer.']
                error_message = "Det finns redan en användare med detta personnummer."

            if not duplicate_name and not duplicate_person_number:
                team = Team()
                form.populate_obj(team)
                db.session.add(team)
                db.session.commit()
                mail.send(team.email, team.price, team.name)
                return render_template("flumride/confirmation.html", team=team)
        else:
            print("Form validation errors: ", form.errors)
            error_message = "Gör om, gör rätt."

        return render_template("flumride/submit.html", form=form, number_of_non_sfs_left=number_of_non_sfs_left, remaining_tickets_for_type=remaining_tickets_for_type, error_message=error_message)
    else:
        return render_template("flumride/submit.html", form=form, number_of_non_sfs_left=number_of_non_sfs_left, remaining_tickets_for_type=remaining_tickets_for_type)


@app.route('/flumride/number_of_non_sfs_left')
def flumride_number_of_non_sfs_left():
    number_of_non_sfs_left = logic.get_number_of_non_sfs_left()
    return jsonify(number_of_non_sfs_left=number_of_non_sfs_left)


@app.route('/flumride/members')
def flumride_members():
    members = TeamMember.query.order_by(TeamMember.person_number).all()
    print('members', members)
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
    ticket_info = [{'type': ticket_type['name'], 'count': TeamMember.ticket_count_by_type(index)} for index, ticket_type in enumerate(app.config['FLUMRIDE']['ticket_types'])]
    total = {
        'teams': teams.count(),
        'members': db.session.query(TeamMember).count(),
        'ticket_info': ticket_info,
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
