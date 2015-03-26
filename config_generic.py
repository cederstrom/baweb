import os
from dateutil import parser


WTF_CSRF_ENABLED = True

# SQLAlchemy
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')

FLUMRIDE = {
    'SUBMIT_OPEN': parser.parse("2015-03-26 21:37:00 +0100"),
    'YEAR': 'tvi-tausen-fäimtåhn',
    'MAX_NR_OF_MEMBERS': 10,
    'MAX_NR_OF_SITTNING': 140,
    'MAX_NR_OF_NEED_BED': 75,
    'MAX_NR_OF_NOT_SFS': 27,
    'FACEBOOK_EVENT_URL': 'https://www.facebook.com/events/942839179066046/',
    'TICKET_PRICE': 299,
    'TICKET_PRICE_WITH_SOVSAL': 399
}
