from flask_sqlalchemy import SQLAlchemy
from devfun import db
from werkzeug import generate_password_hash, check_password_hash
from sqlalchemy_utils import URLType

class User(db.Model):
    __tablename__ = "User"
    username = db.Column(db.String(80), unique=True, primary_key=True)
    email    = db.Column(db.String(120), unique=True)
    pwdhash  = db.Column(db.String(54))

    def __init__(self, username, email, password):
      self.username = username
      self.email = email
      self.set_user_password(password)

    def set_user_password(self, password):
      self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
      return check_password_hash(self.pwdhash, password)

    @property
    def is_authenticated(self):
      return True

    @property
    def is_active(self):
      return True

    @property
    def is_anonymous(self):
      return False

    def get_id(self):
      return self.username


class Post(db.Model):
    __tablename__ = "Post"
    id      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creator = db.Column(db.String(80), db.ForeignKey("User.username"), nullable=False)
    title   = db.Column(db.String(80), nullable=False)
    url     = db.Column(URLType, nullable=False)

    def __init__(self, creator, title, url):
        self.creator = creator
        self.title = title
        self.url = url


class Comment(db.Model):
    __tablename__ = "Comment"
    id      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creator = db.Column(db.String(80), db.ForeignKey("User.username"), nullable=False)
    post    = db.Column(db.Integer, db.ForeignKey("Post.id"), nullable=False)
    content = db.Column(db.String(500), nullable=False)

    def __init__(self, creator, post, content):
        self.creator = creator
        self.post = post
        self.content = content

