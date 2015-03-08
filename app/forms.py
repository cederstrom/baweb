from flask.ext.wtf import Form
import wtforms
from wtforms import FormField, SubmitField
from .models import Team, TeamMember
from wtforms_alchemy import ModelForm, ModelFieldList


class MemberForm(ModelForm, wtforms.Form):
    class Meta:
        model = TeamMember


class TeamForm(ModelForm, Form):
    class Meta:
        model = Team

    members = ModelFieldList(FormField(MemberForm),
                             min_entries=1, max_entries=10)
    submit = SubmitField('Skicka')
