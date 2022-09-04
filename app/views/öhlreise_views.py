# -*- coding: utf-8 -*-
from flask import jsonify, render_template, redirect, url_for, request
from app import app, db, logic, mail_öhlreise
from app.decorators import login_required
from app.forms import BeerForm
from app.models import Beer


@app.route('/öhlreise/info')
def beer():
    return render_template("öhlreise/info.html")

@app.route('/öhlreise/members', methods=['GET', 'POST'])
def öhlreise_members():
    beer = Beer.query.order_by(Beer.name).all()
    return render_template("öhlreise/members.html", beer=beer)

@app.route('/öhlreise/member/<id>', methods=['GET', 'POST'])
@login_required
def öhlreise_edit_member(id):
    member = Beer.get(id)
    assert member

    if request.method == 'POST':
        form = BeerForm(request.form)
        form.populate_obj(member)
        db.session.add(member)
        db.session.commit()
        return redirect(url_for('öhlreise_members', _anchor=member.id))
    else:
        form = BeerForm(obj=member)
        return render_template("öhlreise/edit_member.html", form=form,
                               title='Editera medlem')

@app.route('/öhlreise/members/add-member', methods=['POST'])
@login_required
def öhlreise_add_member():

        if request.method == 'POST':
            member = Beer()
            form = BeerForm(request.form)
            form.populate_obj(member)
            db.session.add(member)
            db.session.commit()
            return redirect(url_for('öhlreise_members'))
        else:
            form = BeerForm()
            return render_template("öhlreise/edit_member.html", form=form,
                               title='Lägg till medlem')

@app.route('/öhlreise/member/<id>/delete', methods=['POST'])
@login_required
def öhlreise_delete_member(id):
    Beer.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('öhlreise_members'))

@app.route('/öhlreise/submit', methods=['GET', 'POST'])
def öhlreise_submit():
    if not logic.is_submit_öhlreise_open():
        milliseconds = logic.get_milliseconds_until_öhlreise_submit_opens()
        return render_template("öhlreise/countdown.html",
                               milliseconds=milliseconds)
    remaining_tickets_for_type = [logic.get_number_of_tickets_for_this_type_left_beer(ind) for ind, ticket in enumerate(app.config['ÖHLREISE']['ticket_types'])]

    if sum(remaining_tickets_for_type) <= 0 or logic.has_submit_öhlreise_closed():
        return render_template("öhlreise/submit_temp_closed.html")

    form = BeerForm()
    if form.validate_on_submit():
        beer = _create_response(request)
        mail_öhlreise.send(beer.email, beer.price, beer.name)
        return render_template("öhlreise/confirmation.html", beer=beer)
    else:
        remaining_tickets_for_type = [logic.get_number_of_tickets_for_this_type_left_beer(ind) for ind, ticket in enumerate(app.config['ÖHLREISE']['ticket_types'])]
        return render_template("öhlreise/submit.html", remaining_tickets_for_type=remaining_tickets_for_type, form=form)

def _create_response(request):
    beer = Beer()
    form = BeerForm(request.form)
    form.populate_obj(beer)
    db.session.add(beer)
    db.session.commit()
    return beer
