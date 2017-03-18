from flask.ext.wtf import Form
import wtforms
from wtforms import FormField, SubmitField, StringField, BooleanField
from wtforms.validators import DataRequired, Required
from .models import Team, TeamMember
from wtforms_alchemy import ModelForm, ModelFieldList
from app import app, logic

class MemberForm(ModelForm, wtforms.Form):
    class Meta:
        model = TeamMember
    tickets = []
    for index,ticket in enumerate(app.config['FLUMRIDE']['ticket_types']):
        if (logic.get_number_of_tickets_for_this_type_left(index) > 0):
            tickets.append( (index, ticket['name']) )
    ticket_type = wtforms.SelectField('', choices=tickets, coerce=int)


class TeamForm(ModelForm, Form):
    class Meta:
        model = Team

    members = ModelFieldList(FormField(MemberForm),
                             min_entries=1, max_entries=10)
    accept_terms = BooleanField('accept_terms', default=False, validators=[Required()])
    submit = SubmitField('Skicka anmälan!')


class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
