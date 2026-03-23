# -*- coding: utf-8 -*-
from flask import jsonify, render_template, redirect, url_for, request
from app import app, db, logic, mail
from app.decorators import login_required
from app.forms import TeamForm, AdminMemberForm
from app.models import Team, TeamMember
from sqlalchemy.exc import IntegrityError
import csv
import io
from flask import Response


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

    form = AdminMemberForm(request.form if request.method == 'POST' else None, obj=member)
    form.team_id.choices = [(team.id, team.name) for team in Team.query.order_by(Team.name).all()]

    if request.method == 'POST' and form.validate():
        form.populate_obj(member)

        selected_team = Team.get(form.team_id.data)
        if selected_team:
            member.team = selected_team

        db.session.add(member)
        db.session.commit()
        return redirect(url_for('flumride_teams', _anchor=str(member.team.id)))

    if request.method == 'GET':
        form.team_id.data = member.team.id

    if request.method == 'DELETE':
        db.session.delete(member)
        db.session.commit()
        return redirect(url_for('flumride_teams', _anchor=str(member.team.id)))

    return render_template(
        "flumride/edit_member.html",
        form=form,
        title='Editera medlem',
        member=member
    )

@app.route('/flumride/member/<id>/delete', methods=['POST'])
@login_required
def flumride_delete_member(id):
    member = TeamMember.get(id)
    if not member:
        return redirect(url_for('flumride_teams'))

    team_id = member.team.id if member.team else None

    db.session.delete(member)
    db.session.commit()

    if team_id:
        return redirect(url_for('flumride_teams', _anchor=str(team_id)))
    else:
        return redirect(url_for('flumride_teams'))

@app.route('/flumride/team/<id>/add-member', methods=['GET', 'POST'])
@login_required
def flumride_add_member(id):
    team = Team.get(id)
    assert team

    form = AdminMemberForm(request.form if request.method == 'POST' else None)
    form.team_id.choices = [(t.id, t.name) for t in Team.query.order_by(Team.name).all()]

    if request.method == 'POST':
        member = TeamMember()
        form.populate_obj(member)

        selected_team = Team.get(form.team_id.data)
        if selected_team:
            member.team = selected_team
        else:
            member.team = team

        try:
            db.session.add(member)
            db.session.commit()
            return redirect(url_for('flumride_teams', _anchor=str(member.team.id)))

        except IntegrityError as e:
            db.session.rollback()

            if 'team_member.person_number' in str(e.orig):
                form.person_number.errors = list(form.person_number.errors) + [
                    'Det finns redan en medlem med detta personnummer.'
                ]
                return render_template(
                    "flumride/edit_member.html",
                    form=form,
                    title='Lägg till medlem',
                    member=None
                )

            raise

    else:
        form.team_id.data = team.id
        return render_template(
            "flumride/edit_member.html",
            form=form,
            title='Lägg till medlem',
            member=None
        )

@app.route('/flumride/team/<id>/set-has-payed', methods=['POST'])
@login_required
def flumride_set_has_payed(id):
    team = Team.get(id)
    team.has_payed = True
    db.session.commit()
    resp = jsonify(has_payed=True)
    resp.status_code = 200
    return resp

def _get_filtered_teams():
    teams = db.session.query(Team)
    has_payed_arg = request.args.get('has_payed')

    if has_payed_arg is not None and has_payed_arg != '-':
        has_payed = has_payed_arg == 'True'
        teams = teams.filter_by(has_payed=has_payed)

    return teams, has_payed_arg

@app.route('/flumride/teams')
def flumride_teams():
    teams, has_payed_arg = _get_filtered_teams()
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


@app.route('/flumride/export/team/csv')
@login_required
def flumride_export_team_csv():
    teams, _ = _get_filtered_teams()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        'Lag-ID',
        'Lagnamn',
        'Stad',
        'Slogan',
        'E-post',
        'Pris',
        'Betalat',
        'Anmälningsdatum',
    ])

    for team in teams:
        writer.writerow([
            team.id,
            team.name,
            team.city,
            team.slogan,
            team.email,
            team.price,
            'Ja' if team.has_payed else 'Nej',
            team.submit_date,
        ])

    csv_data = output.getvalue()
    output.close()

    return Response(
        csv_data,
        mimetype='text/csv',
        headers={
            'Content-Disposition': 'attachment; filename=flumride_team_export.csv'
        }
    )

@app.route('/flumride/export/team-members/csv')
@login_required
def flumride_export_team_members_csv():
    members = TeamMember.query.order_by(TeamMember.team_id).all()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        'Lag',
        'Namn',
        'Personnummer',
        'Biljett',
        'Allergier',
        'Dryck',
        'SFS-medlem'
    ])

    for member in members:
        writer.writerow([
            member.team.name if member.team else '',
            member.name_of_member,
            member.person_number,
            app.config['FLUMRIDE']['ticket_types'][member.ticket_type]['name'],
            member.allergies,
            app.config['FLUMRIDE']['drink_options'][member.drink_option]['name'],
            'Ja' if member.sfs else 'Nej'
        ])

    csv_data = output.getvalue()
    output.close()

    return Response(
        csv_data,
        mimetype='text/csv',
        headers={
            'Content-Disposition': 'attachment; filename=flumride_team_members_export.csv'
        }
    )

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
        return redirect(url_for('flumride_teams', _anchor=str(team.id)))
    else:
        form = TeamForm(obj=team)
        return render_template("flumride/edit_team.html", form=form)

@app.route('/flumride/team/<id>/delete', methods=['POST'])
@login_required
def flumride_delete_team(id):
    team = Team.get(id)
    if not team:
        return redirect(url_for('flumride_teams'))

    for member in team.members:
        db.session.delete(member)

    db.session.delete(team)
    db.session.commit()

    return redirect(url_for('flumride_teams'))