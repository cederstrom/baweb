import os
from dateutil import parser


WTF_CSRF_ENABLED = True

# SQLAlchemy
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')

FLUMRIDE = {
    'SUBMIT_OPEN': parser.parse("2017-03-21 03:00:00 +0100"),
    'SUBMIT_CLOSE': parser.parse("2017-04-25 03:00:00 +0100"),
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
    'ticket_types': [
        {
            'name': 'Kånntainerpasset',
            'price': 399,
            'description': 'Sovsal, sittning, frukost, flumrundan, caps-vm, kårkväll fredag-lördag. Notera att 100kr/person i sovsals deposition tillkommer (som ni självklart får tillbaka om ni inte trashar stället)',
            'max_nr': 70
        },
        {
            'name': 'Kundvagnspasset',
            'price': 299,
            'description': 'Som ovan fast utan sovsal',
            'max_nr': 50
        },
        {
            'name': 'Spårrtpass',
            'price': 249,
            'description': 'flumrundan, caps-vm, kårkväll fredag-lördag',
            'max_nr': 50
        }
    ],
    'MAX_NR_OF_MEMBERS': 10,
    'MAX_NR_OF_NOT_SFS': 15,
    'FACEBOOK_EVENT_URL': 'https://www.facebook.com/events/1899427956960956/',
    'TRAILER_URL': 'https://www.youtube.com/embed/Jw0P2gZTxD4'
}

FACEBOOK_GRAPH_URL = 'https://graph.facebook.com/'
