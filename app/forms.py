from flask.ext.wtf import Form
from wtforms import (BooleanField, FieldList, FormField, SelectField,
                     StringField, SubmitField)
from wtforms.validators import DataRequired
from .models import TeamMember


class ModelFieldList(FieldList):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop("model", None)
        super(ModelFieldList, self).__init__(*args, **kwargs)
        if not self.model:
            raise ValueError("ModelFieldList requires model to be set")


class MemberForm(Form):
    name_of_member = StringField('name_of_member', validators=[DataRequired()])
    person_number = StringField('person_number', validators=[DataRequired()])
    allergies = StringField('allergies', validators=[DataRequired()])
    need_bed = BooleanField('need_bed', default=False)
    sfs = BooleanField('sfs', default=False)
    sittning = BooleanField('sittning', default=True)
    ticket_type = SelectField(
        u'ticket_type',
        choices=[('flumpass', 'Flumpass - Standard'),
                 ('sparrtpass', 'Spårrtpass - Endast spårrterna, ej kårkvällar sittning osv.')])


class TeamForm(Form):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    slogan = StringField('slogan', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    members  = FieldList(FormField(MemberForm), min_entries=1, max_entries=10)
    submit = SubmitField('Skicka')
