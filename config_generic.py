import os
from dateutil import parser


WTF_CSRF_ENABLED = True

# SQLAlchemy
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')

FLUMRIDE = {
    'SUBMIT_OPEN': parser.parse("2017-03-23 19:00:00 +0100"),
    'SUBMIT_CLOSE': parser.parse("2017-04-25 03:00:00 +0100"),
    'YEAR': 'tvi-tausen-tjutåån',
    'START_DATE': '5:e maj',
    'END_DATE': '7:e maj',
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
            'description': 'Sovsal (fredag och lördag) inkl. frukost, sittning, flumrunda med spårrter och "lagom" mycket dônk (är detta året vi faktiskt ska dricka upp allt?), capsVM (inkl. öhl), lunch på lördag, ett fräckt märke, två kårkvällar (plus bonuskårkväll på torsdagen om man vill)',
            'max_nr': 70
        },
        {
            'name': 'Kundvagnspasset',
            'price': 299,
            'description': 'Allt i kånntainerpasset minus soval och frukost (däremot har vi gratis kaffe på kårhuset, BYOmugg)',
            'max_nr': 50
        },
        {
            'name': 'Spårrtpass',
            'price': 249,
            'description': 'Allt i kånntainerpasset minus soval, frukost och sittning',
            'max_nr': 1000
        }
    ],
    'payment': {
        'last_payment_date': '2017-04-27',
        'bank': 'Swedbank',
        'account_number': '8327-9,944 894 648-4'
    },
    'MAX_NR_OF_MEMBERS': 10,
    'MAX_NR_OF_NOT_SFS': 50,
    'FACEBOOK_EVENT_URL': 'https://www.facebook.com/events/1899427956960956/',
    'TRAILER_URL': 'https://www.youtube.com/embed/Jw0P2gZTxD4'
}

FACEBOOK_GRAPH_URL = 'https://graph.facebook.com/'
