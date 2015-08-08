from datetime import date

from flask import request
from flask_wtf import Form
from wtforms import (
    StringField,
    HiddenField,
    BooleanField,
    DateField,
    SubmitField,
    SelectField,
    RadioField,
    TextAreaField,
    IntegerField
)

from wtforms.validators import DataRequired, ValidationError, NumberRange, Email

class projectSettings(Form):
    project_name = StringField('Project Name', validators=[DataRequired()])
    collaboration_tool = SelectField(u'Collaboration Tool', choices=[('trello', 'Trello')])
    collaboration_project_name = SelectField(u'Collaboration Project Name', choices=[])
    start_sprint = IntegerField('Sprint Start No', validators=[NumberRange(min=1)])
    start_year = IntegerField('Sprint Start Year', validators=[NumberRange(min=2014)])
    start_month = IntegerField('Sprint Start Month', validators=[NumberRange(min=1, max=12)])
    start_day = IntegerField('Sprint Start Day', validators=[NumberRange(min=1, max=31)])
