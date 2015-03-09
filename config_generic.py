import os


WTF_CSRF_ENABLED = True

# SQLAlchemy
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')

FLUMRIDE = {
    'YEAR': 'tvi-tausen-fäimtåhn',
    'MAX_NR_OF_MEMBERS': 10,
    'FACEBOOK_EVENT_URL': 'https://www.facebook.com/events/942839179066046/'
}
