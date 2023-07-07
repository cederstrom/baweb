from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']
app.config['SESSION_COOKIE_SECURE'] = True

db = SQLAlchemy(app)
lm = LoginManager(app)
lm.init_app(app)
app.app_context().push()

from app import views, models
