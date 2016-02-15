from flask.ext.wtf import Form
from wtforms import BooleanField, TextField, PasswordField
from wtforms.validators import DataRequired, Length, Required, EqualTo
from .models import User

class RegistrationForm(Form):
    username = TextField('Username', [Length(min=4, max=25)])
    email = TextField('Email Address', [Length(min=6, max=35)])
    password = PasswordField('New Password', [
        Required(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None


class LoginForm(Form):
    username = TextField('Username', [Length(min=4, max=25)])
    password = PasswordField('New Password', [Required()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if user is None:
            self.username.errors.append('Unknown username')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        self.user = user
        return True
