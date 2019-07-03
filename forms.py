from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,PasswordField,IntegerField
from wtforms.validators import EqualTo, DataRequired


class Register(FlaskForm):
    firstname = StringField('First Name', [DataRequired()])
    lastname = StringField('Last Name',[DataRequired()])
    username = StringField('Username', [DataRequired()])
    password = PasswordField('Password',[DataRequired(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm')
    submit = SubmitField("Register")

class Login(FlaskForm):
    username = StringField('Username', [DataRequired()])
    password = PasswordField('Password',[DataRequired()])
    submit = SubmitField("Login")

class Contribution(FlaskForm):
    username = StringField('Username', [DataRequired()])
    item = StringField('Items')
    quantity = IntegerField('Quantity')
    submit = SubmitField("Submit")

