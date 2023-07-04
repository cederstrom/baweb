from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']

# Initialize SQLAlchemy and Session
db = SQLAlchemy(app)
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_SQLALCHEMY'] = db
sess = Session(app)

# Initialize LoginManager
lm = LoginManager(app)

from app import views, models
