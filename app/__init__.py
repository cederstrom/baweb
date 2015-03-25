from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager


app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager(app)
app.secret_key = app.config['SECRET_KEY']
app.register_blueprint(app.config['BLUEPRINT'], url_prefix="/login")

from app import views, models
