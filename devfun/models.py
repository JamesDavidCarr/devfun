from flask_sqlalchemy import SQLAlchemy
from devfun import db
from werkzeug import generate_password_hash, check_password_hash

class User(db.Model):
  __tablename__ = "User"
  username = db.Column(db.String(80), unique=True, primary_key=True)
  email = db.Column(db.String(120), unique=True)
  pwdhash = db.Column(db.String(54))

  def __init__(self, username, email, password):
    self.username = username
    self.email = email
    self.set_user_password(password)

  def set_user_password(self, password):
    self.pwdhash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)
