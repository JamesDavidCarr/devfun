from flask.ext.wtf import Form
from wtforms import Form, BooleanField, TextField, PasswordField
from wtforms.validators import DataRequired, Length, Required, EqualTo

class LoginForm(Form):
    username = TextField('Username', [Length(min=4, max=25)])
    email = TextField('Email Address', [Length(min=6, max=35)])
    password = PasswordField('New Password', [
        Required(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
