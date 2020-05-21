from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, TextAreaField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

class LocationForm(FlaskForm):
    locationFrom = StringField('From', validators=[DataRequired()])
    locationTo = StringField('To', validators=[DataRequired()])
    submit = SubmitField('Search')

class AlertForm(FlaskForm):
    submit = SubmitField('Search')
    daily_input = StringField('Enter Number')
    seven_day = StringField('Enter Number')
    weekly_change = StringField('Enter Number')
    per_1000 = StringField('Enter Number')
    daily_input_radio = RadioField(
        'daily', choices=[('above', 'above'), ('below', 'below')])
    seven_day_radio = RadioField(
        'daily', choices=[('above', 'above'), ('below', 'below')])
    weekly_change_radio = RadioField(
        'daily', choices=[('above', 'above'), ('below', 'below')])
    per_1000_radio = RadioField(
        'daily', choices=[('above', 'above'), ('below', 'below')])
    email_input = StringField('Email')
    phone_area_code = IntegerField('AreaCode')
    phone_input = IntegerField('PhoneNumber')
