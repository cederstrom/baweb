from flask.ext.wtf import Form
import wtforms
from wtforms import (BooleanField, FieldList, FormField, SelectField,
                     StringField, SubmitField)
from wtforms.validators import DataRequired, Email


class MemberForm(wtforms.Form):
    name_of_member = StringField('name_of_member', validators=[DataRequired()])
    person_number = StringField('person_number', validators=[DataRequired()])
    allergies = StringField('allergies')
    need_bed = BooleanField('need_bed')
    sfs = BooleanField('sfs')
    sittning = BooleanField('sittning')
    # ticket_type = SelectField(
    #    u'ticket_type',
    #    choices=[('flumpass', 'Flumpass - Standard'),
    #             ('sparrtpass', 'Spårrtpass - Endast spårrterna, ej kårkvällar sittning osv.')])


class TeamForm(Form):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    slogan = StringField('slogan', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    members  = FieldList(FormField(MemberForm), min_entries=1, max_entries=10)
    submit = SubmitField('Skicka')
