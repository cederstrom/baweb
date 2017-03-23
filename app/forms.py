# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
import wtforms
from wtforms import FormField, SubmitField, StringField, BooleanField, RadioField
from wtforms.validators import DataRequired, Required, ValidationError
from .models import Team, TeamMember
from wtforms_alchemy import ModelForm, ModelFieldList
from app import app, logic

class MemberForm(ModelForm, wtforms.Form):
    class Meta:
        model = TeamMember
    tickets = []
    for index,ticket in enumerate(app.config['FLUMRIDE']['ticket_types']):
        if (logic.get_number_of_tickets_for_this_type_left(index) > 0):
            tickets.append( (index, ticket['name'] +' - ' +str(ticket['price']) + 'kr') )
    ticket_type = RadioField('Välj biljett:', choices=tickets, coerce=int)

class TeamForm(ModelForm, Form):
    class Meta:
        model = Team

    members = ModelFieldList(FormField(MemberForm),
                             min_entries=1, max_entries=10)
    accept_terms = BooleanField('accept_terms', default=False, validators=[Required()])
    submit = SubmitField('Skicka anmälan!')

    def validate_members(self, members):

        remaining_tickets_for_type = [logic.get_number_of_tickets_for_this_type_left(ind) for ind, ticket in enumerate(app.config['FLUMRIDE']['ticket_types'])]
        team_tickets = [x.data['ticket_type'] for x in members]
        remaining_tickets_after_transaction = [left - team_tickets.count(index) for index, left in enumerate(remaining_tickets_for_type)]
        error = False
        for member in members:
            if member.data['ticket_type'] == None:
                #Don't do an .append() here since we dont want the default [not a valid choice] error to appear
                member.ticket_type.errors = ['Du glömde ange biljettyp för denna medlemen, vi har därför valt denna åt dig istället (men om du vill byta så gör det!)']
                error = True
                continue
            if remaining_tickets_after_transaction[member.data['ticket_type']] < 0:
                member.ticket_type.errors.append('Du har anget fler av denna biljettyp än vad som finns kvar')
                error = True
        #Verify all person_numbers are unique
        person_numbers = [x.data['person_number'] for x in members]
        duplicate_person_numbers = [x for n, x in enumerate(person_numbers) if x in person_numbers[:n]]
        if duplicate_person_numbers:
            for member in members:
                if member.data['person_number'] in duplicate_person_numbers:
                    member.person_number.errors.append('Du har med samma personnummer flera gånger')
                    error = True
        if error:
            raise ValidationError("error in input")


class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
