from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__, static_folder="static")
app.config.from_object('config')

db = SQLAlchemy(app)

lm = LoginManager()
lm.login_view = "/login"
lm.init_app(app)

from devfun import views, models
