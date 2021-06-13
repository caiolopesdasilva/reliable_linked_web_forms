from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,SelectField
from . import dataset


class SignUpForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    test = SelectField(u'Programming Language', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    submit = SubmitField('Sign Up')
