import os


WTF_CSRF_ENABLED = True

# SQLAlchemy
SECRET_KEY = 'you-will-never-guess'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')
