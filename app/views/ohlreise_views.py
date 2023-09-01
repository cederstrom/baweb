# -*- coding: utf-8 -*-
from flask import jsonify, render_template, redirect, url_for, request
from app import app, db, logic, mail_ohlreise
from app.decorators import login_required
from app.forms import BeerForm, DeleteForm
from app.models import Beer


@app.route('/ohlreise/info')
def beer():
    return render_template("ohlreise/info.html")

@app.route('/ohlreise/members', methods=['GET', 'POST'])
def ohlreise_members():
    form = DeleteForm()
    beer = Beer.query.order_by(Beer.name).all()
    return render_template("ohlreise/members.html", beer=beer, form=form)

@app.route('/ohlreise/member/<id>', methods=['GET', 'POST'])
@login_required
def ohlreise_edit_member(id):
    member = Beer.get(id)
    assert member

    if request.method == 'POST':
        form = BeerForm(request.form)
        form.populate_obj(member)
        db.session.add(member)
        db.session.commit()
        return redirect(url_for('ohlreise_members', _anchor=member.id))
    else:
        form = BeerForm(obj=member)
        return render_template("ohlreise/edit_member.html", form=form,
                               title='Editera medlem')

@app.route('/ohlreise/members/add-member', methods=['POST'])
@login_required
def ohlreise_add_member():

        if request.method == 'POST':
            member = Beer()
            form = BeerForm(request.form)
            form.populate_obj(member)
            db.session.add(member)
            db.session.commit()
            return redirect(url_for('ohlreise_members'))
        else:
            form = BeerForm()
            return render_template("ohlreise/edit_member.html", form=form,
                               title='Lägg till medlem')

@app.route('/ohlreise/member/<id>/delete', methods=['POST'])
@login_required
def ohlreise_delete_member(id):
    if request.method == 'POST':
        beer = Beer.query.get(id)
        if beer:
            db.session.delete(beer)
            db.session.commit()
            return redirect(url_for('ohlreise_members'))  # Redirect to the appropriate route
        else:
            flash('Gick inte att hitta resenäreren.', 'error')
    return render_template('ohlreise_members', form = form)

@app.route('/ohlreise/submit', methods=['GET', 'POST'])
def ohlreise_submit():
    if not logic.is_submit_ohlreise_open():
        milliseconds = logic.get_milliseconds_until_ohlreise_submit_opens()
        return render_template("ohlreise/countdown.html", milliseconds=milliseconds)

    remaining_tickets_for_type = [logic.get_number_of_tickets_for_this_type_left_beer(ind) for ind, ticket in enumerate(app.config['ÖHLREISE']['ticket_types'])]

    if sum(remaining_tickets_for_type) <= 0 or logic.has_submit_ohlreise_closed():
        return render_template("ohlreise/submit_temp_closed.html")

    form = BeerForm()

    if request.method == 'POST':
        form = BeerForm(request.form)

        if form.name.validate(form) and form.email.validate(form) and form.person_number.validate(form) and form.mobile_number.validate(form) and form.accept_terms.validate(form):
            beer = _create_response(request)
            mail_ohlreise.send(beer.email, beer.price, beer.name)
            return render_template("ohlreise/confirmation.html", beer=beer)
        else:
            remaining_tickets_for_type = [logic.get_number_of_tickets_for_this_type_left_beer(ind) for ind, ticket in enumerate(app.config['ÖHLREISE']['ticket_types'])]
            return render_template("ohlreise/submit.html", remaining_tickets_for_type=remaining_tickets_for_type, form=form)

    # Handle the GET case
    remaining_tickets_for_type = [logic.get_number_of_tickets_for_this_type_left_beer(ind) for ind, ticket in enumerate(app.config['ÖHLREISE']['ticket_types'])]
    return render_template("ohlreise/submit.html", remaining_tickets_for_type=remaining_tickets_for_type, form=form)

def _create_response(request):
    beer = Beer()
    form = BeerForm(request.form)
    form.validate()  # Manually validate the form
    form.populate_obj(beer)
    db.session.add(beer)
    db.session.commit()
    return beer
