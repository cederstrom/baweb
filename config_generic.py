import os
from dateutil import parser


WTF_CSRF_ENABLED = True

# SQLAlchemy
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')

FLUMRIDE = {
    'SUBMIT_OPEN': parser.parse("2017-03-21 03:00:00 +0100"),
    'YEAR': 'tvi-tausen-tjutåån',
# EXAMPLE ON HOW TO FILL SCHEDULE DATA
#    [
#       {
#           'day': 'Fredag',
#           'data': [
#           'Brutalare från alla världens hörn anländer till Karlskrona ungefär samtidigt som alla tävlande.',
#           '12:00 - 18:00: Incheckning sker på kåren i Karlskrona. Här delas flumpass, partykit™ och lösa faddrar ut till alla anmälda.',
#           '18:00 - 20:00: VM i caps på kåren som efterföljs av tokröj tills samtliga personer har stupat (d.v.s. spik kl 21:00).'
#           ]
#       },
#       {
#           'day': 'Lördag',
#           'data': ['stuff', 'stuff2']
#       }
    'schedule': [],
    'MAX_NR_OF_MEMBERS': 10,
    'MAX_NR_OF_SITTNING': 146,
    'MAX_NR_OF_NEED_BED': 75,
    'MAX_NR_OF_NOT_SFS': 15,
    'FACEBOOK_EVENT_URL': 'https://www.facebook.com/events/1899427956960956/',
    'TICKET_PRICE': 349,
    'TICKET_PRICE_WITH_SOVSAL': 499
}

FACEBOOK_GRAPH_URL = 'https://graph.facebook.com/'
