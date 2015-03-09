import os
from datetime import datetime


WTF_CSRF_ENABLED = True

# SQLAlchemy
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')

FLUMRIDE = {
    'SUBMIT_OPEN': datetime.strptime("2015-03-26 20:22:23", "%Y-%m-%d %H:%M:%S"),
    'YEAR': 'tvi-tausen-fäimtåhn',
    'MAX_NR_OF_MEMBERS': 10,
    'MAX_NR_OF_SITTNING': 150,
    'MAX_NR_OF_NEED_BED': 100,
    'MAX_NR_OF_NOT_SFS': 15,
    'FACEBOOK_EVENT_URL': 'https://www.facebook.com/events/942839179066046/'
}
