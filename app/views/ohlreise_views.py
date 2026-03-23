# -*- coding: utf-8 -*-
import csv
import io
from flask import Response

from flask import render_template, redirect, url_for, request, flash
from app import app, db, logic, mail_ohlreise
from app.decorators import login_required
from app.forms import BeerForm, DeleteForm, AdminBeerEditForm
from app.models import Beer


@app.route('/ohlreise/info')
def beer():
    return render_template("ohlreise/info.html")

@app.route('/ohlreise/members', methods=['GET'])
def ohlreise_members():
    beers, has_payed_arg = _get_filtered_beers()
    beers = beers.order_by(Beer.name).all()

    return render_template(
        "ohlreise/members.html",
        beer=beers,
        has_payed=has_payed_arg
    )

@app.route('/ohlreise/member/<id>', methods=['GET', 'POST'])
@login_required
def ohlreise_edit_member(id):
    member = Beer.get(id)
    assert member

    if request.method == 'POST':
        form = AdminBeerEditForm(request.form)
        form.Meta.csrf = False

        if form.validate():
            form.populate_obj(member)
            db.session.add(member)
            db.session.commit()
            return redirect(url_for('ohlreise_members', _anchor=str(member.id)))

        app.logger.warning("AdminBeerEditForm errors: %r", form.errors)
        return render_template(
            "ohlreise/edit_member.html",
            form=form,
            title='Editera medlem'
        )

    form = AdminBeerEditForm(obj=member)
    return render_template(
        "ohlreise/edit_member.html",
        form=form,
        title='Editera medlem'
    )

@app.route('/ohlreise/members/add-member', methods=['GET', 'POST'])
@login_required
def ohlreise_add_member():
    if request.method == 'POST':
        form = BeerForm(request.form)

        if form.validate():
            member = Beer()
            form.populate_obj(member)
            db.session.add(member)
            db.session.commit()
            return redirect(url_for('ohlreise_members'))

        return render_template(
            "ohlreise/edit_member.html",
            form=form,
            title='Lägg till medlem'
        )

    form = BeerForm()
    return render_template(
        "ohlreise/edit_member.html",
        form=form,
        title='Lägg till medlem'
    )

@app.route('/ohlreise/member/<id>/delete', methods=['POST'])
@login_required
def ohlreise_delete_member(id):
    member = Beer.query.get(id)

    if not member:
        flash('Gick inte att hitta resenären.', 'error')
        return redirect(url_for('ohlreise_members'))

    db.session.delete(member)
    db.session.commit()
    flash('Resenären togs bort.', 'success')
    return redirect(url_for('ohlreise_members'))

@app.route('/ohlreise/submit', methods=['GET', 'POST'])
def ohlreise_submit():
    if not logic.is_submit_ohlreise_open():
        milliseconds = logic.get_milliseconds_until_ohlreise_submit_opens()
        return render_template("ohlreise/countdown.html", milliseconds=milliseconds)

    remaining_tickets_for_type = [
        logic.get_number_of_tickets_for_this_type_left_beer(ind)
        for ind, ticket in enumerate(app.config['ÖHLREISE']['ticket_types'])
    ]

    if sum(remaining_tickets_for_type) <= 0 or logic.has_submit_ohlreise_closed():
        return render_template("ohlreise/submit_temp_closed.html")

    form = BeerForm(request.form)
    form.Meta.csrf = False
    error_message = "None"

    if request.method == 'POST':
        person_number = form.data.get('person_number')

        if form.validate():
            duplicate_person_number = (
                Beer.query.filter_by(person_number=person_number).first()
                if person_number else None
            )

            if duplicate_person_number:
                form.person_number.errors = list(form.person_number.errors) + [
                    'Det finns redan en användare med detta personnummer.'
                ]
                error_message = "Det finns redan en användare med detta personnummer."
            else:
                beer = Beer()
                form.populate_obj(beer)
                db.session.add(beer)
                db.session.commit()

                try:
                    mail_ohlreise.send(beer.email, beer.price, beer.name)
                except Exception:
                    app.logger.exception(
                        "Failed to send Ohlreise confirmation email"
                    )

                return render_template("ohlreise/confirmation.html", beer=beer)

        else:
            app.logger.warning("Beer form validation errors: %r", form.errors)
            error_message = "Gör om, gör rätt."

        return render_template(
            "ohlreise/submit.html",
            remaining_tickets_for_type=remaining_tickets_for_type,
            form=form,
            error_message=error_message
        )

    return render_template(
        "ohlreise/submit.html",
        remaining_tickets_for_type=remaining_tickets_for_type,
        form=form,
        error_message=error_message
    )

@app.route('/ohlreise/members/delete', methods=['POST'])
@login_required
def ohlreise_remove_all_members():
    members = Beer.query.fetchall()

    if not members:
        flash('Gick inte att hitta några resenärer.', 'error')
        return redirect(url_for('ohlreise_members'))

    db.session.delete(members)
    db.session.commit()
    flash('Resenärerna togs bort.', 'success')
    return redirect(url_for('ohlreise_members'))

def _get_filtered_beers():
    beers = db.session.query(Beer)
    has_payed_arg = request.args.get('has_payed')

    if has_payed_arg is not None and has_payed_arg != '-':
        has_payed = has_payed_arg == 'True'
        beers = beers.filter_by(has_payed=has_payed)

    return beers, has_payed_arg


@app.route('/ohlreise/export/members/csv')
@login_required
def ohlreise_export_csv():
    beers = db.session.query(Beer).order_by(Beer.name).all()
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        'Namn',
        'Kårnamn',
        'Personnummer',
        'E-post',
        'Mobilnummer',
        'Betalat',
    ])

    for beer in beers:
        writer.writerow([
            beer.name,
            beer.nickname,
            beer.person_number,
            beer.email,
            '%s' % beer.mobile_number if beer.mobile_number else '',
            'Ja' if beer.has_payed else 'Nej',
        ])

    csv_data = output.getvalue()
    output.close()

    return Response(
        csv_data,
        mimetype='text/csv',
        headers={
            'Content-Disposition': 'attachment; filename=ohlreise_members_export.csv'
        }
    )
